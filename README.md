# OpenChase plugin

See what publications and people are posting right now on X, Reddit,
YouTube, Instagram, TikTok and more, from your AI assistant or your own code.

- **MCP server:** `https://mcp.openchase.ai/mcp`
- **Skills:** `openchase-search` (searching well) and `build-with-openchase`
  (writing code against the API)
- **API:** `https://api.openchase.ai`. Docs: https://openchase.ai/docs, all of
  them as one Markdown file for AI assistants at
  https://openchase.ai/llms-full.txt, and the OpenAPI spec at
  `https://api.openchase.ai/v1/openapi.json`

## Install

| Tool | How |
|---|---|
| Claude Code | Install this plugin from its marketplace, or just the server: `claude mcp add --transport http openchase https://mcp.openchase.ai/mcp`, then `/mcp` → openchase → Authenticate |
| Cursor, VS Code, GitHub Copilot, Codex, Kiro | Load this folder as an Agent Plugin, or add `https://mcp.openchase.ai/mcp` as a remote MCP server |
| Anything else | Add the MCP URL above. Clients that only run local servers: `npx -y mcp-remote https://mcp.openchase.ai/mcp` |

Sign in when asked (your browser opens; approve once). Or send an API key as
`Authorization: Bearer oc_live_...`: create one at https://openchase.ai/connect
(Keys tab). New accounts get 10 free credits. Credits cost ₹180 per 1,000 in
India (GST included) and $2 per 1,000 elsewhere (local tax included), and
never expire.

Once connected, try: "What are people saying about OpenAI today?"

## Layout

- `plugin.json`, `mcp.json`: Agent Plugins 1.0.0
- `.claude-plugin/plugin.json`, `.mcp.json`: Claude Code
- `skills/`: the two skills, shared by every client

## License

The skills and examples are MIT licensed. "OpenChase" and the OpenChase logo
are trademarks of CuriousCats and are not covered by the license.

Privacy: https://openchase.ai/privacy.html · Support: comms@curiouscats.ai
