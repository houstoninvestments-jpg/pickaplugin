import { EmailMessage } from "cloudflare:email";
import { DurableObject } from "cloudflare:workers";
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
async function resend(env, to, subject, html, text) {
  if (!env.RESEND_KEY) return null;
  try {
    const r = await fetch("https://api.resend.com/emails", { method: "POST", headers: { authorization: "Bearer " + env.RESEND_KEY, "content-type": "application/json" },
      body: JSON.stringify({ from: "PickAPlugin <hello@pickaplugin.com>", to: [to], subject, html, text, reply_to: "hello@pickaplugin.com" }) });
    if (!r.ok) { console.log("resend", r.status, await r.text()); return null; }
    return (await r.json()).id || null;
  } catch (e) { console.log("resend failed", String(e)); return null; }
}
// ---- views / clicks sent to makers (Durable Object, SQLite). Only salted hashed IPs, kept 2 days, for once-per-day dedupe. ----
const month = () => new Date().toISOString().slice(0, 7);
export class Stats extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env); this.sql = ctx.storage.sql;
    this.sql.exec("CREATE TABLE IF NOT EXISTS seen(day TEXT, h TEXT, slug TEXT, kind TEXT, PRIMARY KEY(day,h,slug,kind))");
    this.sql.exec("CREATE TABLE IF NOT EXISTS counts(month TEXT, slug TEXT, kind TEXT, n INTEGER, PRIMARY KEY(month,slug,kind))");
  }
  get(slug) {
    const o = { month: month(), views: 0, clicks: 0 };
    for (const r of this.sql.exec("SELECT kind, n FROM counts WHERE month=? AND slug=?", o.month, slug)) o[r.kind === "view" ? "views" : "clicks"] = r.n;
    return o;
  }
  hit(kind, slug, h) {
    if (h && (kind === "view" || kind === "click")) {
      const day = new Date().toISOString().slice(0, 10);
      const ins = this.sql.exec("INSERT OR IGNORE INTO seen VALUES(?,?,?,?) RETURNING 1", day, h, slug, kind).toArray();
      if (ins.length) this.sql.exec("INSERT INTO counts VALUES(?,?,?,1) ON CONFLICT(month,slug,kind) DO UPDATE SET n=n+1", day.slice(0, 7), slug, kind);
      if (Math.random() < 0.02) this.sql.exec("DELETE FROM seen WHERE day < ?", new Date(Date.now() - 2 * 864e5).toISOString().slice(0, 10));
    }
    return this.get(slug);
  }
  total(kind) { const r = this.sql.exec("SELECT COALESCE(SUM(n),0) AS n, COUNT(*) AS c FROM counts WHERE month=? AND kind=?", month(), kind).one(); return { month: month(), total: r.n, plugins: r.c }; }
  all(m) { return { month: m, rows: this.sql.exec("SELECT slug, kind, n FROM counts WHERE month=? ORDER BY n DESC", m).toArray() }; }
}
const statsStub = env => env.STATS.get(env.STATS.idFromName("v1"));
const BOT = /bot|crawl|spider|slurp|scrap|fetch|curl|wget|python|httpx|aiohttp|go-http|java\/|okhttp|axios|undici|node|deno|headless|phantom|puppeteer|playwright|selenium|lighthouse|pagespeed|gtmetrix|preview|facebookexternalhit|embedly|whatsapp|telegram|discord|slack|skype|monitor|uptime|pingdom|feed|rss|archiv|semrush|ahrefs|mj12|dataforseo|bytespider|gpt|claude|anthropic|perplexity|cohere|meta-external|petal|yandex|baidu|bing|google|yahoo|validator|checker|scan|http-client|libwww|winhttp|postman|insomnia/i;
// Default automation fingerprints seen on /go/ in Nov 2026 (Playwright/Puppeteer iPhone preset; Catalina is a common scraper UA).
const FAKE_UA = /iPhone OS 13_2_3|Android 6\.0; Nexus 5 Build\/MRA58N|Intel Mac OS X 10_15_7/;
const CLOUD_ASN = new Set([16509,14618,7224,8987,15169,396982,8075,14061,24940,213230,16276,63949,20473,31898,45102,132203,13335,136907,60068,212238,51167,20473,9009,20860,12876,16247,40676,55286,394380,399629,398101,397423,57523]);
const CLOUD_ORG = /amazon|aws|google cloud|gcp|microsoft|azure|digitalocean|hetzner|ovh|linode|akamai|vultr|alibaba|tencent|choopa|datacamp|m247|leaseweb|hivelocity|colocrossing|psychz|quadranet|ovhcloud|oracle cloud|clouvider|scaleway|contabo|kamatera|hostwinds/i;
function sameSiteReferer(req) {
  const ref = req.headers.get("referer") || "";
  try { const h = new URL(ref).hostname; return h === "pickaplugin.com" || h === "www.pickaplugin.com"; } catch { return false; }
}
function human(req, forClick) {
  const ua = req.headers.get("user-agent") || "";
  if (ua.length < 40 || !/^Mozilla\/5\.0 /.test(ua) || BOT.test(ua) || FAKE_UA.test(ua)) return false;
  if (req.cf && req.cf.verifiedBotCategory) return false;
  const score = req.cf && req.cf.botManagement && req.cf.botManagement.score;
  if (typeof score === "number" && score < 30) return false;
  const asn = Number((req.cf && req.cf.asn) || 0);
  if (CLOUD_ASN.has(asn) || CLOUD_ORG.test((req.cf && req.cf.asOrganization) || "")) return false;
  const pur = (req.headers.get("sec-purpose") || req.headers.get("purpose") || "").toLowerCase();
  if (pur.includes("prefetch") || pur.includes("prerender")) return false;
  if (!req.headers.get("accept-language")) return false;
  if (forClick) {
    // Real clicks come from a listing page. Crawlers often spoof a browser UA and follow every /go/ link.
    if (!sameSiteReferer(req)) return false;
    const site = (req.headers.get("sec-fetch-site") || "").toLowerCase();
    if (site && site !== "same-origin" && site !== "same-site") return false;
  }
  return true;
}
async function visitor(req, env, forClick) {
  const ip = req.headers.get("cf-connecting-ip"); if (!ip || !human(req, forClick)) return null;
  return hmac(env.ADMIN_TOKEN || "pap", "ip:" + new Date().toISOString().slice(0, 10) + ":" + ip);  // salted, daily-rotating, never stored raw
}
const fmtN = n => n.toLocaleString("en-US");
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
    // double opt-in: store as pending, email a confirm link; only status "confirmed" gets the newsletter
    const f = await req.formData();
    if (f.get("website")) return page(u, "/subscribed");
    const email = String(f.get("email") || "").trim().toLowerCase().slice(0, 254);
    if (!EM.test(email)) return page(u, "/form-error", "w=sub");
    if (!(await turnstileOk(env, f, ip, req))) return page(u, "/form-error", "w=captcha");
    const key = "sub:" + email, raw = await env.LEADS.get(key), old = raw ? JSON.parse(raw) : null;
    if (old && old.status === "confirmed") return page(u, "/subscribed");
    if (old && old.confirm_sent_at && Date.now() - Date.parse(old.confirm_sent_at) < 15 * 60000) return page(u, "/subscribed");
    const rec = { type: "subscriber", status: "pending", at: (old && old.at) || new Date().toISOString(), email, from: String(f.get("from") || (old && old.from) || "").slice(0, 200), confirm_sends: ((old && old.confirm_sends) || 0) + 1 };
    if (rec.confirm_sends > 3) return page(u, "/subscribed");
    const link = `https://pickaplugin.com/confirm?e=${encodeURIComponent(email)}&t=${await hmac(env.ADMIN_TOKEN, "confirm:" + email)}`;
    const unsub = `https://pickaplugin.com/unsubscribe?e=${encodeURIComponent(email)}&t=${await hmac(env.ADMIN_TOKEN, "unsub:" + email)}`;
    const id = await resend(env, email, "Confirm your PickAPlugin subscription",
      `<div style="font:16px/1.5 Georgia,serif;color:#14171f;max-width:560px"><p>Hi,</p><p>Someone (hopefully you) asked to get the PickAPlugin weekly email: new MCP servers and plugins, once a week.</p><p><a href="${link}" style="display:inline-block;background:#14171f;color:#f4efe1;padding:10px 16px;text-decoration:none">Yes, subscribe me</a></p><p>If that wasn't you, ignore this email and you won't hear from us again.</p><p style="color:#5b5a52;font-size:13px">PickAPlugin · pickaplugin.com · <a href="${unsub}" style="color:#5b5a52">unsubscribe</a></p></div>`,
      `Someone (hopefully you) asked to get the PickAPlugin weekly email: new MCP servers and plugins, once a week.\n\nConfirm here: ${link}\n\nIf that wasn't you, ignore this email and you won't hear from us again.\n\nPickAPlugin · https://pickaplugin.com`);
    if (id) { rec.confirm_sent_at = new Date().toISOString(); rec.confirm_id = id; }
    await env.LEADS.put(key, JSON.stringify(rec));
    return page(u, id ? "/subscribed" : "/form-error", id ? "" : "w=mail");
  }
  if (p === "/api/confirm" && req.method === "POST") {
    const f = await req.formData();
    const email = String(f.get("e") || "").toLowerCase(), t = String(f.get("t") || "");
    if (!email || t !== await hmac(env.ADMIN_TOKEN, "confirm:" + email)) return page(u, "/form-error", "w=confirm");
    const key = "sub:" + email, raw = await env.LEADS.get(key);
    if (!raw) return page(u, "/form-error", "w=confirm");
    const rec = JSON.parse(raw);
    if (rec.status !== "confirmed") {
      rec.status = "confirmed"; rec.confirmed_at = new Date().toISOString();
      await env.LEADS.put(key, JSON.stringify(rec));
      // No per-confirm email to Aaron; subscriber counts go in the Tuesday newsletter report.
    }
    return page(u, "/confirmed");
  }
  if (p === "/unsubscribe") {
    const email = (u.searchParams.get("e") || "").toLowerCase(), t = u.searchParams.get("t") || "";
    if (email && t === await hmac(env.ADMIN_TOKEN, "unsub:" + email)) {
      await env.LEADS.delete("sub:" + email);
      if (req.method === "POST") return new Response("unsubscribed", { status: 200 }); // RFC 8058 one-click
      return page(u, "/unsubscribed");
    }
    return page(u, "/form-error", "w=unsub");
  }
  if (p === "/api/admin") {
    if (!env.ADMIN_TOKEN || u.searchParams.get("token") !== env.ADMIN_TOKEN) return json({ error: "not found" }, 404);
    const del = u.searchParams.get("delete");
    if (del) { await env.LEADS.delete(del); return json({ deleted: del }); }
    if (u.searchParams.get("stats")) return json(await statsStub(env).all(u.searchParams.get("month") || month()));
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
async function goOut(req, env, u, slug) {
  let p = null;
  try { p = (await catalog(env, u)).plugins.find(x => x.slug === slug); } catch (e) { console.log("go", String(e)); }
  if (!p) return Response.redirect("https://pickaplugin.com/p/" + slug, 302);
  const to = u.searchParams.get("to"), dest = (to === "home" && p.homepage) || (to === "docs" && p.docs) || p.repo;
  if (!/^https?:\/\//.test(dest || "")) return Response.redirect("https://pickaplugin.com/p/" + slug, 302);
  if (env.STATS && req.method === "GET") {
    try { const h = await visitor(req, env, true); if (h) await statsStub(env).hit("click", slug, h); } catch (e) { console.log("stats click", String(e)); }
  }
  return new Response(null, { status: 302, headers: { location: dest, "cache-control": "no-store", "x-robots-tag": "noindex, nofollow", "referrer-policy": "origin" } });
}
async function withViews(req, env, res, slug) {
  let c = null;
  try { const h = await visitor(req, env); c = await statsStub(env).hit(h ? "view" : "none", slug, h); } catch (e) { console.log("stats view", String(e)); }
  const out = new Response(res.body, res); out.headers.set("cache-control", "no-store");
  // Public view/click counts are hidden (2026-11-21): Nov totals were inflated by crawlers
  // spoofing browser UAs. Counts still accrue in the Durable Object for /api/admin?stats=1.
  return out;
}
async function withTotal(env, res) {
  let t = null; try { t = await statsStub(env).total("click"); } catch (e) { console.log("stats total", String(e)); }
  const out = new Response(res.body, res); out.headers.set("cache-control", "no-store");
  // Same as listing pages: do not publish the site-wide click total until counts are trustworthy.
  return out;
}
export default {
  async fetch(req, env) {
    const u = new URL(req.url);
    if (u.hostname === "www.pickaplugin.com" || u.protocol === "http:") { u.hostname = "pickaplugin.com"; u.protocol = "https:"; return Response.redirect(u.toString(), 301); }
    // Thin-page consolidations (2026-11-21). Keep these in run_worker_first (wrangler.toml + upload_buckets.py).
    const path = u.pathname.replace(/\.html$/i, "").replace(/\/+$/, "") || "/";
    const thin = [
      [/^\/best\/([a-z0-9-]+)$/, (s) => "/c/" + s],
      [/^\/alternatives\/([a-z0-9-]+)$/, (s) => "/p/" + s],
      [/^\/compare\/([a-z0-9-]+)$/, () => "/compare"],
      [/^\/best-for\/([a-z0-9-]+)$/, () => "/compare"],
      [/^\/tools\/mcp-config-converter\/([a-z0-9-]+)$/, () => "/tools/mcp-config-converter"],
    ];
    for (const [re, to] of thin) {
      const m = path.match(re);
      if (m) return Response.redirect("https://pickaplugin.com" + to(m[1]), 301);
    }
    if (u.pathname === "/mcp" || u.pathname === "/mcp/") return mcp(req, env, u);
    const go = u.pathname.match(/^\/go\/([a-z0-9-]+)\/?$/);
    if (go) return goOut(req, env, u, go[1]);
    if (u.pathname.startsWith("/api/") || u.pathname === "/unsubscribe") {
      try { const r = await handle(req, env, u); if (r) return r; } catch (e) { console.log(String(e)); return json({ error: "server error" }, 500); }
      return json({ error: "not found" }, 404);
    }
    const res = await env.ASSETS.fetch(req);
    const ps = u.pathname.match(/^\/p\/([a-z0-9-]+?)(?:\.html)?\/?$/);
    if (ps && res.status === 200 && req.method === "GET" && env.STATS) return withViews(req, env, res, ps[1]);
    if (/^\/advertise(\.html|\/)?$/.test(u.pathname) && res.status === 200 && env.STATS) return withTotal(env, res);
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
