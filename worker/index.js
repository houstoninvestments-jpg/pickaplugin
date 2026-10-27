import { EmailMessage } from "cloudflare:email";
const H = { "content-type": "application/json", "cache-control": "no-store" };
const json = (o, s = 200) => new Response(JSON.stringify(o, null, 1), { status: s, headers: H });
const EM = /^[^\s@<>"]{1,64}@[^\s@<>"]{1,190}\.[a-z]{2,}$/i;
async function hmac(key, msg) {
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return [...new Uint8Array(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(msg)))].map(b => b.toString(16).padStart(2, "0")).join("").slice(0, 32);
}
async function turnstileOk(env, f, ip, req) {
  if (!env.TURNSTILE_SECRET) return true;
  if (env.ADMIN_TOKEN && req && req.headers.get("x-admin-token") === env.ADMIN_TOKEN) return true; // owner-only test path
  const t = f.get("cf-turnstile-response"); if (!t) return false;
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: t, remoteip: ip || "" }) });
  return (await r.json()).success === true;
}
async function notify(env, subject, text) {
  if (!env.NOTIFY) return;
  try {
    const raw = ["From: PickAPlugin forms <hello@pickaplugin.com>", "To: houstoninvestments@gmail.com", "Subject: " + subject.replace(/[\r\n]/g, " "),
      "Message-ID: <" + crypto.randomUUID() + "@pickaplugin.com>", "Date: " + new Date().toUTCString(), "MIME-Version: 1.0", "Content-Type: text/plain; charset=utf-8", "", text].join("\r\n");
    await env.NOTIFY.send(new EmailMessage("hello@pickaplugin.com", "houstoninvestments@gmail.com", raw));
  } catch (e) { console.log("notify failed", String(e)); }
}
const page = (u, path, q) => Response.redirect(new URL(path + (q ? "?" + q : ""), u).toString(), 303);
async function handle(req, env, u) {
  const p = u.pathname, ip = req.headers.get("cf-connecting-ip");
  if (p === "/api/claim" && req.method === "POST") {
    const f = await req.formData();
    if (f.get("website")) return page(u, "/claimed");  // honeypot: pretend success
    const email = String(f.get("email") || "").trim().slice(0, 254), gh = String(f.get("github") || "").trim().replace(/^@/, "").slice(0, 60),
      slug = String(f.get("slug") || "").replace(/[^a-z0-9-]/g, "").slice(0, 100), fix = String(f.get("corrections") || "").slice(0, 2000);
    if (!EM.test(email) || !/^[A-Za-z0-9-]{1,39}$/.test(gh) || !slug) return page(u, "/form-error", "w=claim&s=" + slug);
    if (!(await turnstileOk(env, f, ip, req))) return page(u, "/form-error", "w=captcha&s=" + slug);
    const at = new Date().toISOString(), rec = { type: "claim", at, email, github: gh, slug, corrections: fix, country: req.cf?.country || "" };
    await env.LEADS.put(`claim:${at}:${crypto.randomUUID().slice(0, 8)}`, JSON.stringify(rec));
    await notify(env, `[PickAPlugin] Listing claim: ${slug} by @${gh}`, `${JSON.stringify(rec, null, 1)}\n\nPage: https://pickaplugin.com/p/${slug}\nRepo owner check: confirm @${gh} owns/maintains the repo before replying.`);
    return page(u, "/claimed", "s=" + slug);
  }
  if (p === "/api/subscribe" && req.method === "POST") {
    const f = await req.formData();
    if (f.get("website")) return page(u, "/subscribed");
    const email = String(f.get("email") || "").trim().toLowerCase().slice(0, 254);
    if (!EM.test(email)) return page(u, "/form-error", "w=sub");
    if (!(await turnstileOk(env, f, ip, req))) return page(u, "/form-error", "w=captcha");
    const key = "sub:" + email;
    if (!(await env.LEADS.get(key))) {
      await env.LEADS.put(key, JSON.stringify({ type: "subscriber", at: new Date().toISOString(), email, from: String(f.get("from") || "").slice(0, 200) }));
      await notify(env, "[PickAPlugin] New newsletter subscriber", email);
    }
    return page(u, "/subscribed");
  }
  if (p === "/unsubscribe") {
    const email = (u.searchParams.get("e") || "").toLowerCase(), t = u.searchParams.get("t") || "";
    if (email && t === await hmac(env.ADMIN_TOKEN, "unsub:" + email)) { await env.LEADS.delete("sub:" + email); return page(u, "/unsubscribed"); }
    return page(u, "/form-error", "w=unsub");
  }
  if (p === "/api/admin") {
    if (!env.ADMIN_TOKEN || u.searchParams.get("token") !== env.ADMIN_TOKEN) return json({ error: "not found" }, 404);
    const del = u.searchParams.get("delete");
    if (del) { await env.LEADS.delete(del); return json({ deleted: del }); }
    const out = { claims: [], subscribers: [] }; let cursor;
    do {
      const l = await env.LEADS.list({ cursor }); cursor = l.list_complete ? null : l.cursor;
      for (const k of l.keys) {
        const raw = await env.LEADS.get(k.name); if (!raw) continue; const v = JSON.parse(raw); v.key = k.name;
        if (v.type === "subscriber") { v.unsubscribe = `https://pickaplugin.com/unsubscribe?e=${encodeURIComponent(v.email)}&t=${await hmac(env.ADMIN_TOKEN, "unsub:" + v.email)}`; out.subscribers.push(v); }
        else out.claims.push(v);
      }
    } while (cursor);
    return json(out);
  }
  return null;
}
export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    if (u.hostname === "www.pickaplugin.com" || u.protocol === "http:") { u.hostname = "pickaplugin.com"; u.protocol = "https:"; return Response.redirect(u.toString(), 301); }
    if (u.pathname.startsWith("/api/") || u.pathname === "/unsubscribe") {
      try { const r = await handle(req, env, u); if (r) return r; } catch (e) { console.log(String(e)); return json({ error: "server error" }, 500); }
      return json({ error: "not found" }, 404);
    }
    const res = await env.ASSETS.fetch(req);
    const m = u.pathname.match(/^\/(language|license)\/([^\/]+?)\/?$/);
    if (res.status === 404 && m) {
      // collection page below the gate (or alias spelling): fold the alias, else send to the hub
      const raw = decodeURIComponent(m[2]).toLowerCase().replace(/\.html$/, "");
      const al = { "c#": "csharp", "c++": "cpp", "js": "javascript", "ts": "typescript", "golang": "go" };
      const norm = (al[raw] || raw).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
      const to = norm && norm !== m[2] ? `/${m[1]}/${norm}` : `/${m[1]}s`;
      return Response.redirect(`https://pickaplugin.com${to}`, 308);
    }
    return res;
  }
};
