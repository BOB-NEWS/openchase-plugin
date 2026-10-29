"""A small OpenChase API client using only the standard library.

    export OPENCHASE_KEY="oc_live_..."   # from https://openchase.ai/connect (Keys tab)
    python openchase_client.py "openai"

Each run spends 2 credits (a search and its top links).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.getenv("OPENCHASE_API_URL", "https://api.openchase.ai")


class OpenChaseError(Exception):
    def __init__(self, status, code, message):
        super().__init__(f"{status} {code}: {message}")
        self.status, self.code, self.message = status, code, message


def call(method, path, body=None, retries=3):
    key = os.environ["OPENCHASE_KEY"]
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE_URL + path, data=data, method=method,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            payload = json.loads(e.read() or b"{}")
            if e.code == 429 and attempt < retries:
                time.sleep(float(e.headers.get("Retry-After") or 2 ** attempt))
                continue
            raise OpenChaseError(e.code, payload.get("error"), payload.get("message"))


def search(q, platforms=("x", "reddit"), countries=("us",), window="24h"):
    return call("POST", "/v1/search", {"q": q, "platforms": list(platforms), "countries": list(countries), "window": window})


def top_links(search_id, per_platform=5):
    return call("POST", "/v1/search-links", {"search_id": search_id, "per_platform": per_platform})


if __name__ == "__main__":
    found = search(sys.argv[1] if len(sys.argv) > 1 else "openai")
    print(f"{found['total']} results, credits {found['credits']}")
    for r in found["results"][:10]:
        print(f"- [{r['platform']}] {r['title']}")
    links = top_links(found["search_id"])
    for platform, block in links["platforms"].items():
        for r in block["results"]:
            print(f"  {platform}: {r['url']}")
