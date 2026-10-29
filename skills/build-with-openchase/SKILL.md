---
name: build-with-openchase
description: Write code that calls the OpenChase API (api.openchase.ai). Use when the user is adding real-time social or publication search to an app, script or pipeline, or mentions OpenChase, OPENCHASE_KEY, or endpoints like /v1/search.
---

# Building with the OpenChase API

1. Read `references/endpoints.md` for inputs and outputs. For every
   endpoint with examples and sample responses, fetch
   `https://openchase.ai/llms-full.txt`; the OpenAPI spec is at
   `https://api.openchase.ai/v1/openapi.json`.
2. Authenticate with `Authorization: Bearer $OPENCHASE_KEY` (an
   `oc_live_...` key from https://openchase.ai/connect, Keys tab). Read the
   key from the environment or an ignored `.env` file; never put it in source
   code or a committed config file. Every search spends a credit (none if
   nothing is found), so test with a few calls, not a loop.
3. Search first (`POST /v1/search`), then open only what's needed:
   `POST /v1/search-links` with the `search_id` for the top posts per
   platform, or `POST /v1/fetch` with result ids. Page with
   `GET /v1/search/{search_id}?page=N`.
4. Read `X-OC-Credits-Used` and `X-OC-Credits-Left`. Handle:
   - `402` (`no_credits`, `key_budget_reached`): stop and tell the user;
   - `429`: wait for `Retry-After`, then retry with backoff;
   - `404 search_expired`: run the search again (searches last 15 minutes).
5. Every error has a `message` written for people: show it as is.
6. Working examples: `examples/openchase_client.py` and
   `examples/openchase_client.mjs`.
