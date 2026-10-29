// A small OpenChase API client for Node 18+ (built-in fetch).
//   node --env-file=.env openchase_client.mjs "openai"   (.env: OPENCHASE_KEY=oc_live_...)
// Each run spends 2 credits (a search and its top links).
const BASE_URL = process.env.OPENCHASE_API_URL ?? "https://api.openchase.ai";

export async function call(method, path, body, retries = 3) {
  for (let attempt = 0; ; attempt++) {
    const res = await fetch(BASE_URL + path, {
      method,
      headers: { Authorization: `Bearer ${process.env.OPENCHASE_KEY}`, "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await res.json();
    if (res.ok) return data;
    if (res.status === 429 && attempt < retries) {
      await new Promise((r) => setTimeout(r, 1000 * Number(res.headers.get("Retry-After") ?? 2 ** attempt)));
      continue;
    }
    throw new Error(`${res.status} ${data.error}: ${data.message}`);
  }
}

export const search = (q, platforms = ["x", "reddit"], countries = ["us"], window = "24h") =>
  call("POST", "/v1/search", { q, platforms, countries, window });

export const topLinks = (searchId, perPlatform = 5) =>
  call("POST", "/v1/search-links", { search_id: searchId, per_platform: perPlatform });

if (import.meta.url === `file://${process.argv[1]}`) {
  const found = await search(process.argv[2] ?? "openai");
  console.log(`${found.total} results, credits`, found.credits);
  for (const r of found.results.slice(0, 10)) console.log(`- [${r.platform}] ${r.title}`);
  const links = await topLinks(found.search_id);
  for (const [platform, block] of Object.entries(links.platforms)) for (const r of block.results) console.log(`  ${platform}: ${r.url}`);
}
