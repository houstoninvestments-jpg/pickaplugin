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
// ---- PickAPlugin MCP server (Streamable HTTP, stateless, read-only). Data: /catalog.json built by scripts/build_mcp.py ----
const MCP_VERSIONS = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"];
const CORS = { "access-control-allow-origin": "*", "access-control-allow-methods": "GET, POST, OPTIONS, DELETE", "access-control-allow-headers": "content-type, accept, authorization, mcp-session-id, mcp-protocol-version, last-event-id", "access-control-expose-headers": "mcp-session-id, mcp-protocol-version" };
let CAT = null, CAT_AT = 0;
async function catalog(env, u) {
  if (CAT && Date.now() - CAT_AT < 300000) return CAT;
  const r = await env.ASSETS.fetch(new Request(new URL("/catalog.json", u).toString()));
  if (!r.ok) throw new Error("catalog unavailable");
  CAT = await r.json(); CAT_AT = Date.now();
  for (const p of CAT.plugins) p._h = { n: p.name.toLowerCase(), s: p.slug, d: (p.summary || "").toLowerCase(), c: p.category.toLowerCase(), m: (p.maker || "").toLowerCase() };
  return CAT;
}
const STR = (d, extra = {}) => ({ type: "string", description: d, ...extra });
const LIMIT = { type: "integer", minimum: 1, maximum: 25, description: "Max results (default 10, max 25)." };
const RO = { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false };
const TOOLS = [
  { name: "search_plugins", title: "Search plugins", description: "Search the PickAPlugin catalog of ChatGPT, Codex and Claude plugins, agent skills and MCP servers by keyword (e.g. 'memory', 'postgres', 'code review', 'pdf'). Paid featured listings come first and are marked featured=true; everything else is ranked by relevance, then GitHub stars.", inputSchema: { type: "object", properties: { query: STR("Keywords describing what the plugin should do."), category: STR("Optional category name or slug from list_categories."), limit: LIMIT }, required: ["query"], additionalProperties: false }, annotations: { title: "Search plugins", ...RO } },
  { name: "get_plugin", title: "Get plugin", description: "Full details for one listing by its slug (from a search result or a pickaplugin.com/p/<slug> URL): summary, category, maker, repo, homepage, docs, install command, stars, license.", inputSchema: { type: "object", properties: { slug: STR("Listing slug, e.g. 'deja', or a pickaplugin.com/p/<slug> URL.") }, required: ["slug"], additionalProperties: false }, annotations: { title: "Get plugin", ...RO } },
  { name: "list_categories", title: "List categories", description: "All PickAPlugin categories with plugin counts and links.", inputSchema: { type: "object", properties: {}, additionalProperties: false }, annotations: { title: "List categories", ...RO } },
  { name: "top_plugins", title: "Top plugins", description: "Top plugins overall or in one category: paid featured listings first (marked featured=true), then editor's picks, then the most-starred maintained projects.", inputSchema: { type: "object", properties: { category: STR("Optional category name or slug from list_categories."), limit: LIMIT }, additionalProperties: false }, annotations: { title: "Top plugins", ...RO } },
];
const lim = (v, d = 10) => Math.max(1, Math.min(25, Number.isFinite(+v) && +v > 0 ? Math.floor(+v) : d));
const slugify = s => String(s || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
function findCat(cat, name) {
  if (!name) return null; const s = slugify(name);
  return cat.categories.find(c => c.slug === s || c.name.toLowerCase() === String(name).toLowerCase()) || cat.categories.find(c => c.slug.includes(s) || s.includes(c.slug)) || false;
}
function out(p, full) {
  const o = { name: p.name, slug: p.slug, summary: p.summary, category: p.category, url: p.url, repo: p.repo };
  if (p.homepage) o.homepage = p.homepage;
  if (p.featured) { o.featured = true; o.label = "featured (paid placement)"; }
  if (p.editors_pick) o.editors_pick = true;
  if (p.stars != null) o.stars = p.stars;
  if (p.archived) o.archived = true;
  if (full) for (const k of ["maker", "docs", "install", "license", "language", "first_seen", "pushed_at", "verified"]) if (p[k] != null && p[k] !== false) o[k] = p[k];
  return o;
}
const starsOf = p => (typeof p.stars === "number" ? p.stars : -1);
const topKey = (a, b) => (b.featured - a.featured) || (a.archived - b.archived) || (b.editors_pick - a.editors_pick) || (starsOf(b) - starsOf(a)) || a.name.localeCompare(b.name);
const STOP = new Set(["a", "an", "the", "for", "to", "of", "and", "or", "in", "on", "with", "my", "me", "plugin", "plugins", "mcp", "server", "servers", "tool", "tools", "that", "can", "find", "best", "agent", "skill", "skills", "codex", "claude", "chatgpt", "openai", "ai"]);
function search(cat, a) {
  const q = String(a.query || "").toLowerCase().slice(0, 200).trim();
  let toks = q.split(/[^a-z0-9#+.]+/).filter(t => t.length > 1 && !STOP.has(t));
  if (!toks.length) toks = q.split(/[^a-z0-9#+.]+/).filter(t => t.length > 1);
  const c = findCat(cat, a.category);
  if (c === false) return { error: `Unknown category '${a.category}'. Call list_categories for valid names.` };
  const res = [];
  for (const p of cat.plugins) {
    if (c && p.category !== c.name) continue;
    const h = p._h; let sc = 0, hit = 0;
    if (q && (h.n === q || h.s === slugify(q))) sc += 100;
    for (const t of toks) {
      let ts = 0;
      if (h.n.includes(t) || h.s.includes(t)) ts += 30;
      if (new RegExp("\\b" + t.replace(/[.+#]/g, "\\$&")).test(h.d)) ts += 10; else if (h.d.includes(t)) ts += 4;
      if (h.c.includes(t)) ts += 8;
      if (h.m.includes(t)) ts += 5;
      if (ts) hit++; sc += ts;
    }
    if (!toks.length && !q) sc = 1;
    if (!sc) continue;
    if (toks.length > 1) sc *= 0.5 + 0.5 * hit / toks.length;
    sc += Math.log10(Math.max(0, starsOf(p)) + 1) * 2 - (p.archived ? 20 : 0);
    res.push([sc, p]);
  }
  res.sort((x, y) => (y[1].featured - x[1].featured) || (y[0] - x[0]));
  const n = lim(a.limit);
  return { query: a.query, category: c ? c.name : undefined, total_matches: res.length, results: res.slice(0, n).map(r => out(r[1])), browse: c ? c.url : `https://pickaplugin.com/` };
}
function callTool(cat, name, a) {
  a = a && typeof a === "object" ? a : {};
  if (name === "search_plugins") { if (!a.query || typeof a.query !== "string") return { error: "query is required." }; return search(cat, a); }
  if (name === "get_plugin") {
    const raw = String(a.slug || "").trim(); const s = slugify(raw.replace(/^.*\/p\//, "").replace(/[?#].*$/, ""));
    const p = cat.plugins.find(x => x.slug === s) || cat.plugins.find(x => x.name.toLowerCase() === raw.toLowerCase());
    if (p) return out(p, true);
    const near = search(cat, { query: raw.replace(/-/g, " "), limit: 5 }).results || [];
    return { error: `No listing with slug '${raw}'.`, did_you_mean: near.map(x => ({ name: x.name, slug: x.slug })) };
  }
  if (name === "list_categories") return { count: cat.count, categories: cat.categories };
  if (name === "top_plugins") {
    const c = findCat(cat, a.category);
    if (c === false) return { error: `Unknown category '${a.category}'. Call list_categories for valid names.` };
    const items = cat.plugins.filter(p => !c || p.category === c.name).sort(topKey).slice(0, lim(a.limit));
    return { category: c ? c.name : "all", results: items.map(p => out(p)), browse: c ? c.url : "https://pickaplugin.com/" };
  }
  return null;
}
const rpcErr = (id, code, message) => ({ jsonrpc: "2.0", id: id ?? null, error: { code, message } });
async function rpc(m, env, u) {
  if (!m || m.jsonrpc !== "2.0" || typeof m.method !== "string") return rpcErr(m && m.id, -32600, "Invalid Request");
  const isNote = !("id" in m), id = m.id, P = m.params || {};
  if (isNote) return null;
  switch (m.method) {
    case "initialize": {
      const v = MCP_VERSIONS.includes(P.protocolVersion) ? P.protocolVersion : MCP_VERSIONS[0];
      return { jsonrpc: "2.0", id, result: { protocolVersion: v, capabilities: { tools: { listChanged: false } },
        serverInfo: { name: "pickaplugin", title: "PickAPlugin", version: "1.0.0", websiteUrl: "https://pickaplugin.com/mcp-server" },
        instructions: "Search the PickAPlugin directory (pickaplugin.com) of ChatGPT, Codex and Claude plugins, agent skills and MCP servers. Use search_plugins for 'find me a plugin for X', get_plugin for details and install commands, top_plugins for recommendations by category. Results marked featured=true are paid placements; say so if you recommend them. Always share the pickaplugin.com/p/<slug> url." } };
    }
    case "ping": return { jsonrpc: "2.0", id, result: {} };
    case "tools/list": return { jsonrpc: "2.0", id, result: { tools: TOOLS } };
    case "resources/list": return { jsonrpc: "2.0", id, result: { resources: [] } };
    case "prompts/list": return { jsonrpc: "2.0", id, result: { prompts: [] } };
    case "tools/call": {
      const cat = await catalog(env, u);
      const r = callTool(cat, P.name, P.arguments);
      if (r === null) return rpcErr(id, -32602, `Unknown tool: ${P.name}`);
      return { jsonrpc: "2.0", id, result: { content: [{ type: "text", text: JSON.stringify(r, null, 1) }], structuredContent: r, isError: !!r.error } };
    }
    default: return rpcErr(id, -32601, `Method not found: ${m.method}`);
  }
}
async function mcp(req, env, u) {
  const hdr = (o, s = 200, extra = {}) => new Response(o == null ? null : JSON.stringify(o), { status: s, headers: { ...CORS, ...(o == null ? {} : { "content-type": "application/json" }), "cache-control": "no-store", ...extra } });
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: { ...CORS, "access-control-max-age": "86400" } });
  if (req.method === "GET") {
    if ((req.headers.get("accept") || "").includes("text/html")) return env.ASSETS.fetch(new Request(new URL("/mcp-server", u).toString(), { headers: req.headers }));
    return hdr(rpcErr(null, -32000, "Method not allowed: this server is stateless and has no SSE stream. POST JSON-RPC to this URL. Docs: https://pickaplugin.com/mcp-server"), 405, { allow: "POST, OPTIONS" });
  }
  if (req.method === "DELETE") return hdr(null, 405, { allow: "POST, OPTIONS" });
  if (req.method !== "POST") return hdr(rpcErr(null, -32000, "Method not allowed"), 405, { allow: "POST, OPTIONS" });
  const txt = await req.text();
  if (txt.length > 65536) return hdr(rpcErr(null, -32600, "Request too large"), 413);
  let body; try { body = JSON.parse(txt); } catch { return hdr(rpcErr(null, -32700, "Parse error"), 400); }
  try {
    if (Array.isArray(body)) {
      if (!body.length || body.length > 20) return hdr(rpcErr(null, -32600, "Invalid batch"), 400);
      const rs = (await Promise.all(body.map(m => rpc(m, env, u)))).filter(Boolean);
      return rs.length ? hdr(rs) : hdr(null, 202);
    }
    const r = await rpc(body, env, u);
    return r ? hdr(r) : hdr(null, 202);
  } catch (e) { console.log("mcp", String(e)); return hdr(rpcErr(body && body.id, -32603, "Internal error"), 500); }
}
export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    if (u.hostname === "www.pickaplugin.com" || u.protocol === "http:") { u.hostname = "pickaplugin.com"; u.protocol = "https:"; return Response.redirect(u.toString(), 301); }
    if (u.pathname === "/mcp" || u.pathname === "/mcp/") return mcp(req, env, u);
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
