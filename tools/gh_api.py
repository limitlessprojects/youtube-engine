#!/usr/bin/env python3
"""gh_api.py — GitHub API calls on boxes without the `gh` CLI.

The token is NEVER read from a file, an argument or the environment by this tool: it is
requested from git's own credential helper (`git credential fill`) at call time and used
only in the Authorization header. It is never printed or written anywhere.

Usage:
  tools/gh_api.py whoami                                  # login + token scopes
  tools/gh_api.py secrets                                 # names of the repo's Actions secrets
  tools/gh_api.py runs [workflow.yml] [n]                 # recent workflow runs
  tools/gh_api.py run <run_id>                            # one run: status + per-step conclusions
  tools/gh_api.py dispatch <workflow.yml> key=value ...   # workflow_dispatch on main
  tools/gh_api.py get <api-path>                          # raw GET, e.g. /repos/OWNER/REPO
"""
import json, subprocess, sys, urllib.request, urllib.error

REPO = "limitlessprojects/youtube-engine"
API = "https://api.github.com"


def _token() -> str:
    r = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                       capture_output=True, text=True, timeout=20,
                       env={**__import__("os").environ, "GIT_TERMINAL_PROMPT": "0"})
    for ln in r.stdout.splitlines():
        if ln.startswith("password="):
            return ln[9:]
    sys.exit("no github.com credential in git's helper (see AGENTS.md §4)")


def call(method: str, path: str, body=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + _token(),
                                          "Accept": "application/vnd.github+json",
                                          "X-GitHub-Api-Version": "2022-11-28",
                                          "User-Agent": "youtube-engine-tools"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read()
            return r.status, dict(r.headers), (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), {"error": e.read().decode("utf-8", "ignore")[:500]}


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 2
    cmd = a[0]
    if cmd == "whoami":
        st, h, d = call("GET", "/user")
        print(st, d.get("login"), "| scopes:", h.get("X-OAuth-Scopes") or h.get("x-oauth-scopes"))
    elif cmd == "secrets":
        st, _, d = call("GET", f"/repos/{REPO}/actions/secrets")
        print(st, [(s["name"], s["updated_at"]) for s in d.get("secrets", [])] or d)
    elif cmd == "runs":
        wf = a[1] if len(a) > 1 else None
        n = int(a[2]) if len(a) > 2 else 6
        path = f"/repos/{REPO}/actions/" + (f"workflows/{wf}/runs" if wf else "runs") + f"?per_page={n}"
        st, _, d = call("GET", path)
        for r in d.get("workflow_runs", []):
            print(r["id"], r["name"], r["event"], r["status"], r["conclusion"], r["created_at"], r["head_sha"][:7])
        if st != 200: print(st, d)
    elif cmd == "run":
        st, _, d = call("GET", f"/repos/{REPO}/actions/runs/{a[1]}")
        print(st, d.get("status"), d.get("conclusion"), d.get("html_url"))
        st, _, j = call("GET", f"/repos/{REPO}/actions/runs/{a[1]}/jobs")
        for job in j.get("jobs", []):
            for s in job.get("steps", []):
                print("  ", s["status"], s.get("conclusion"), "-", s["name"])
    elif cmd == "dispatch":
        inputs = dict(kv.split("=", 1) for kv in a[2:])
        st, _, d = call("POST", f"/repos/{REPO}/actions/workflows/{a[1]}/dispatches", {"ref": "main", "inputs": inputs})
        print(st, "dispatched" if st == 204 else d)
        return 0 if st == 204 else 1
    elif cmd == "get":
        st, _, d = call("GET", a[1]); print(st, json.dumps(d, indent=1)[:3000])
    else:
        print(__doc__); return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
