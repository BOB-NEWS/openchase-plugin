# OpenChase API endpoints

Base URL `https://api.openchase.ai`. Every call sends
`Authorization: Bearer <key>` except `/v1/platforms`, `/v1/countries` and
`/v1/openapi.json`. One credit is one search, one more page, or one
search-links call; credits cost ₹180 per 1,000 in India (GST included; $2 per
1,000 elsewhere, coming soon) and never expire. Calls that fail or find
nothing are free.

Full docs with examples and sample responses: https://openchase.ai/llms-full.txt

| Endpoint | Credits | Inputs | Returns |
|---|---|---|---|
| `POST /v1/search` | 1 | `q` (required, up to 200 characters), `platforms` (default `["x","youtube","instagram"]`), `countries` (default `["us"]`), `window` (`24h`, `7d`, `30d`, `any`), `limit` (1–100) | `search_id`, `counts`, `stories`, `page`, `total`, `has_more`, `results[]` without links |
| `GET /v1/search/{search_id}?page=N` | 1 per page | `page` (2, 3, ...), `limit` | Same shape as search |
| `POST /v1/search-links` | 1 | `search_id` or `q` (with `q`: `countries`, `window`), `platforms`, `per_platform` (1–10), `page` | `platforms.{name}.results[]` with `url`, `author`, `image` |
| `POST /v1/fetch` | 0 | `ids` (1–50) | `results[]` with links, `not_found[]` |
| `POST /v1/fetch-markdown` **(new)** | 1 if read, else 0 | `id` (one result id, required), `max_characters` (1,000–100,000, default 20,000) | `{"result": {...markdown}}` on success, `{"failed": {"id", "reason"}}` (`not_found`, `blocked`, `timeout`) if the page couldn't be read |
| `GET /v1/account` | 0 | | account id, name, credits |
| `GET /v1/balance` | 0 | | `credits`, `free`, `bonus`, `paid` |
| `GET /v1/usage` | 0 | `from`, `to`, `group` (`day`, `endpoint`, `key`), `key_id` | `usage[]` |
| `GET /v1/platforms` | 0 | | platform names |
| `GET /v1/countries` | 0 | `q` | `code`, `name`, `flag` |

`fetch-markdown` takes one id per call, not a list — for several pages, call it
several times. Some platforms (X, Instagram, TikTok, LinkedIn, Facebook) sit
behind a login wall, so it mostly returns a caption rather than full article
text there; publications, Substack and Medium come back as clean text.

Not available yet (return 501, never charged): the `signal` filter,
`POST /v1/answer`.

Result fields: `id`, `platform`, `title`, `source`, `published`, `countries`,
`story` (which top story it belongs to, or null). Paid responses also carry
`credits: {"used", "left"}`.

Limits: 120 requests a minute per key, 10 searches running at once per
account; a `429` has `Retry-After`. A `search_id` lasts 15 minutes; result ids
(`p_...`) an hour. Every response has `X-OC-Request-Id`.
