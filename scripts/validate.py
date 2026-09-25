#!/usr/bin/env python3
"""Validate Test Flight submission files.

Usage:
  python scripts/validate.py                      # validate every file in submissions/
  python scripts/validate.py --changed a.yml b    # also enforce PR rules on changed paths
  python scripts/validate.py --no-network         # skip the GitHub repo reachability check

Exit code 0 means everything passed.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SUB_DIR = ROOT / "submissions"
ET = timezone(timedelta(hours=-4))  # EDT on Sep 27 2026
PR_DEADLINE = datetime(2026, 9, 27, 13, 0, tzinfo=ET)
CODE_FREEZE = datetime(2026, 9, 27, 14, 0, tzinfo=ET)

REQUIRED = ["team_name", "slug", "members", "repo", "description", "customer",
            "prior_work"]
OPTIONAL = ["live_url"]
MEMBER_FIELDS = {"name", "github"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
GH_USER_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
REPO_RE = re.compile(r"^https://github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9._-]+?)(?:\.git)?/?$")
URL_RE = re.compile(r"^https?://\S+$")


def blank(v):
    return v is None or (isinstance(v, str) and not v.strip())


def check_repo_public(owner, name):
    url = f"https://api.github.com/repos/{owner}/{name}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "repo is not reachable (private, misspelled or deleted). Make it public."
        return f"WARN could not check repo (GitHub returned {e.code}); a staffer will look"
    except Exception:  # network trouble should not block a team
        return None
    if data.get("private"):
        return "repo is private. Make it public."
    # GitHub's "size" field lags for new repos, so ask for a commit instead
    req = urllib.request.Request(f"{url}/commits?per_page=1", headers=req.headers)
    try:
        with urllib.request.urlopen(req, timeout=15):
            pass
    except urllib.error.HTTPError as e:
        if e.code == 409:  # GitHub's answer for a repo with no commits
            return "repo is empty. Push at least one commit."
    except Exception:
        pass
    return None


def validate_file(path, network=True):
    errs = []
    fname = path.name
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        mark = getattr(e, "problem_mark", None)
        where = f" near line {mark.line + 1}" if mark else ""
        return [f"YAML could not be parsed{where}. Check for tabs or a colon inside an unquoted value."], None
    if not isinstance(data, dict):
        return ["file is empty or not a set of key: value fields"], None

    for k in REQUIRED:
        if k not in data or blank(data[k]):
            errs.append(f"{k} is required")
    unknown = set(data) - set(REQUIRED) - set(OPTIONAL)
    if unknown:
        errs.append(f"unknown field(s): {', '.join(sorted(unknown))}")

    slug = str(data.get("slug") or "")
    if slug and not SLUG_RE.match(slug):
        errs.append("slug must be lowercase letters, numbers and hyphens, e.g. ledgerline")
    if slug and fname != f"{slug}.yml":
        errs.append(f"slug does not match file name (file is {fname}, expected {slug}.yml)")

    members = data.get("members") or []
    if not isinstance(members, list) or not (1 <= len(members) <= 6):
        errs.append("members must list 1 to 6 people")
        members = members if isinstance(members, list) else []
    for i, m in enumerate(members, 1):
        if not isinstance(m, dict):
            errs.append(f"member {i} must have name and github")
            continue
        for f in ("name", "github"):
            if blank(m.get(f)):
                errs.append(f"member {i} is missing {f}")
        extra = set(m) - MEMBER_FIELDS
        if extra:
            errs.append(f"member {i} has extra fields {sorted(extra)}; only name and github "
                        "(this repo is public, so leave out emails and phone numbers)")
        gh = str(m.get("github") or "").lstrip("@").strip()
        if gh and not GH_USER_RE.match(gh):
            errs.append(f"member {i} github should be a handle, not a URL: {m['github']}")

    repo = str(data.get("repo") or "").strip()
    rm = REPO_RE.match(repo)
    if repo and not rm:
        errs.append("repo must look like https://github.com/owner/name")
    elif rm and network:
        e = check_repo_public(rm.group(1), rm.group(2))
        if e:
            errs.append(e)

    desc = str(data.get("description") or "").strip()
    if len(desc) > 280:
        errs.append(f"description is too long ({len(desc)} characters, max 280)")

    v = data.get("live_url")
    if not blank(v) and not URL_RE.match(str(v).strip()):
        errs.append("live_url must be a full link starting with https://")

    return errs, data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changed", nargs="*", default=None,
                    help="paths changed in the PR, relative to repo root")
    ap.add_argument("--no-network", action="store_true")
    args = ap.parse_args()

    failures = {}
    if args.changed is not None:
        # only files directly in submissions/ count; a subfolder counts as outside it
        subs = [p for p in args.changed
                if p.startswith("submissions/") and "/" not in p[len("submissions/"):]]
        other = [p for p in args.changed if p not in subs]
        if other:
            failures["PR"] = [f"PR changes files outside submissions/: {', '.join(other)}"]
        if len(subs) != 1:
            failures.setdefault("PR", []).append(
                f"PR should add or edit exactly one submission file (found {len(subs)})")
        for p in subs:
            if not (ROOT / p).exists():
                failures.setdefault("PR", []).append(
                    f"PR should add or edit exactly one submission file, not delete one ({p})")
        if any(p.endswith("_TEMPLATE.yml") for p in subs):
            failures.setdefault("PR", []).append(
                "don't edit _TEMPLATE.yml; copy it to submissions/<your-slug>.yml")
        targets = {Path(ROOT / p).name for p in subs}
    else:
        targets = None

    files = sorted(p for p in SUB_DIR.glob("*") if p.is_file()
                   and p.name not in ("_TEMPLATE.yml", ".gitkeep"))
    parsed = {}
    for p in files:
        if p.suffix != ".yml":
            if targets is None or p.name in targets:
                failures.setdefault(p.name, []).append("submission files must end in .yml")
            continue
        check_net = not args.no_network and (targets is None or p.name in targets)
        parsed[p.name] = validate_file(p, network=check_net)

    # index teams and GitHub handles across every file, then report clashes on each file
    team_idx, gh_idx = {}, {}
    for name, (_, data) in parsed.items():
        if not data:
            continue
        tn = str(data.get("team_name") or "").strip().lower()
        if tn:
            team_idx.setdefault(tn, []).append(name)
        for m in data.get("members") or []:
            if isinstance(m, dict):
                g = str(m.get("github") or "").lstrip("@").strip().lower()
                if g:
                    gh_idx.setdefault(g, set()).add(name)

    warnings = {}
    for name, (errs, data) in parsed.items():
        if targets is not None and name not in targets:
            continue
        errs = list(errs)
        if data:
            tn = str(data.get("team_name") or "").strip().lower()
            others = [o for o in team_idx.get(tn, []) if o != name]
            if others:
                errs.append(f"team name already used by {', '.join(others)}")
            for g, owners in gh_idx.items():
                if name in owners and len(owners) > 1:
                    o = sorted(owners - {name})
                    errs.append(f"duplicate member: github {g} is also on {', '.join(o)}")
        hard = [e for e in errs if not e.startswith("WARN ")]
        soft = [e[5:] for e in errs if e.startswith("WARN ")]
        if hard:
            failures.setdefault(name, []).extend(hard)
        if soft:
            warnings[name] = soft

    for name, ws in warnings.items():
        for w in ws:
            print(f"WARNING {name}: {w}")

    now = datetime.now(ET)
    if targets is not None and now > PR_DEADLINE:
        note = "after the 1:00 PM PR deadline" if now <= CODE_FREEZE else "after the 2:00 PM code freeze"
        print(f"NOTE: this PR was checked {note}. Staff will decide whether it can still be slotted.")

    if failures:
        print("Submission check failed. Fix the items below and the check will rerun.\n")
        for f, errs in failures.items():
            print(f"{f}:")
            for e in errs:
                print(f"  - {e}")
        sys.exit(1)
    print(f"All good. {len(files)} submission file(s) checked.")


if __name__ == "__main__":
    main()
