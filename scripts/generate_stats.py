#!/usr/bin/env python3
"""Generate assets/stats.svg and assets/contributions.svg for the profile README.

Standard library only. Reads public data for LOGIN through the GitHub GraphQL API
and renders two SVG panels in the same visual language as the rest of the profile.

Usage:
    GITHUB_TOKEN=... python3 scripts/generate_stats.py          # fetch + render
    python3 scripts/generate_stats.py --placeholder              # render empty state

Nothing here invents numbers: every value comes from the API response.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from collections import defaultdict
from datetime import date
from html import escape
from pathlib import Path

LOGIN = os.environ.get("PROFILE_LOGIN") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "javoxirone"
OUT = Path(__file__).resolve().parent.parent / "assets"

# --- design tokens (Terminal Noir) -----------------------------------------
BG = "#06090A"
SURF = "#0B1011"
LINE = "#1B2624"
TEXT = "#E8F0EC"
MUTED = "#7C8C86"
DIM = "#46544F"
MINT = "#3DFFA8"
EMPTY = "#0F1715"
MONO = "'JetBrains Mono','SF Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
SANS = "Inter,'Helvetica Neue',Helvetica,Arial,'Liberation Sans','DejaVu Sans',sans-serif"

BASE_CSS = """
.m{font-family:MONO_FONT}
.s{font-family:SANS_FONT}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes flow{to{stroke-dashoffset:-20}}
@keyframes in{from{opacity:0;transform:translateX(-8px)}}
.blink{animation:blink 1.1s steps(1) infinite}
.pulse{animation:pulse 2s ease-in-out infinite}
.flow{stroke-dasharray:4 6;animation:flow 1.1s linear infinite}
.in{animation:in .5s ease-out backwards}
@media (prefers-reduced-motion:reduce){.blink,.pulse,.flow,.in{animation:none}}
""".replace("MONO_FONT", MONO).replace("SANS_FONT", SANS)


def svg_open(w: int, h: int, title: str, desc: str, css: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-labelledby="t d" fill="none">'
        f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>'
        f"<style>{BASE_CSS}{css}</style>"
    )


# --- data -------------------------------------------------------------------
QUERY = """
query($login:String!){
  user(login:$login){
    followers{totalCount}
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{firstDay contributionDays{contributionCount}}
      }
    }
    repositories(first:100, ownerAffiliation:OWNER, isFork:false, privacy:PUBLIC){
      totalCount
      nodes{
        stargazerCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}){edges{size node{name}}}
      }
    }
  }
}
"""


def fetch(token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-stats-generator",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def summarise(user: dict) -> dict:
    cal = user["contributionsCollection"]["contributionCalendar"]
    repos = user["repositories"]["nodes"]
    sizes: dict[str, int] = defaultdict(int)
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            sizes[edge["node"]["name"]] += edge["size"]
    total = sum(sizes.values()) or 1
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:5]
    return {
        "contributions": cal["totalContributions"],
        "week_starts": [w["firstDay"] for w in cal["weeks"]],
        "weeks": [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]],
        "repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos),
        "followers": user["followers"]["totalCount"],
        "languages": [(name, 100 * size / total) for name, size in top],
    }


# --- renderers --------------------------------------------------------------
def render_stats(data: dict | None) -> str:
    w, h = 1000, 330
    o = [svg_open(w, h, "GitHub stats", "Public GitHub statistics and top languages for " + LOGIN)]
    o.append(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="{SURF}" stroke="{LINE}"/>')
    o.append(f'<rect x="0" y="0" width="{w}" height="44" rx="14" fill="{BG}"/><rect x="0" y="30" width="{w}" height="14" fill="{BG}"/>')
    o.append(f'<line x1="0" y1="44.5" x2="{w}" y2="44.5" stroke="{LINE}"/>')
    o.append(f'<text x="28" y="28" class="m" font-size="14" fill="{MUTED}">$ gh stats --user {escape(LOGIN)}</text>')

    metrics = [
        ("contributions / 12 mo", data["contributions"] if data else None),
        ("public repositories", data["repos"] if data else None),
        ("stars earned", data["stars"] if data else None),
        ("followers", data["followers"] if data else None),
    ]
    for i, (label, value) in enumerate(metrics):
        x = 40 + (i % 2) * 230
        y = 118 + (i // 2) * 100
        shown = f"{value:,}" if value is not None else "—"
        colour = MINT if i == 0 else TEXT
        o.append(f'<text x="{x}" y="{y}" class="m" font-size="46" font-weight="700" fill="{colour}">{shown}</text>')
        o.append(f'<text x="{x}" y="{y+26}" class="m" font-size="14" fill="{MUTED}">{label}</text>')

    o.append(f'<line x1="500.5" y1="72" x2="500.5" y2="{h-52}" stroke="{LINE}"/>')
    o.append(f'<text x="540" y="84" class="m" font-size="14" fill="{MUTED}">top languages</text>')
    langs = data["languages"] if data else []
    for i in range(5):
        y = 118 + i * 38
        name, pct = langs[i] if i < len(langs) else ("—", 0.0)
        o.append(f'<text x="540" y="{y}" class="m" font-size="17" fill="{TEXT}">{escape(name)}</text>')
        o.append(f'<rect x="700" y="{y-12}" width="200" height="10" rx="5" fill="{EMPTY}"/>')
        if pct:
            o.append(f'<rect x="700" y="{y-12}" width="{max(6, 2*pct):.1f}" height="10" rx="5" fill="{MINT}" fill-opacity="{[1,.78,.6,.45,.32][i]}"/>')
            o.append(f'<text x="960" y="{y}" text-anchor="end" class="m" font-size="15" fill="{MUTED}">{pct:.1f}%</text>')

    note = "public repositories only · refreshed daily" if data else "awaiting first sync · populated by the profile-stats workflow"
    o.append(f'<text x="40" y="{h-22}" class="m" font-size="12" fill="{DIM}">{note}</text>')
    o.append("</svg>")
    return "".join(o)


def render_contributions(data: dict | None) -> str:
    step, cell = 17, 14
    cols = len(data["weeks"]) if data else 53
    w = 80 + cols * step
    w = max(w, 1000)
    h = 262
    x0, y0 = 40, 98
    o = [svg_open(w, h, "Contribution graph", "Public contribution calendar for the last twelve months for " + LOGIN)]
    o.append(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="{SURF}" stroke="{LINE}"/>')
    o.append(f'<rect x="0" y="0" width="{w}" height="44" rx="14" fill="{BG}"/><rect x="0" y="30" width="{w}" height="14" fill="{BG}"/>')
    o.append(f'<line x1="0" y1="44.5" x2="{w}" y2="44.5" stroke="{LINE}"/>')
    o.append(f'<text x="28" y="28" class="m" font-size="14" fill="{MUTED}">$ git log --since="12 months ago" --calendar</text>')
    total = f"{data['contributions']:,} contributions" if data else "— contributions"
    o.append(f'<text x="{w-28}" y="28" text-anchor="end" class="m" font-size="14" fill="{MINT}">{total}</text>')

    weeks = data["weeks"] if data else [[0] * 7 for _ in range(53)]
    peak = max((c for wk in weeks for c in wk), default=0)
    opacities = {1: 0.28, 2: 0.5, 3: 0.75, 4: 1.0}
    last_month = None
    last_label_col = -99
    for ci, wk in enumerate(weeks):
        x = x0 + ci * step
        if data:
            month = date.fromisoformat(data["week_starts"][ci]).strftime("%b")
            if month != last_month and ci < cols - 2 and ci - last_label_col >= 3:
                o.append(f'<text x="{x}" y="{y0-12}" class="m" font-size="12" fill="{DIM}">{month}</text>')
                last_label_col = ci
            last_month = month
        for ri, count in enumerate(wk):
            y = y0 + ri * step
            if count == 0 or peak == 0:
                o.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{EMPTY}"/>')
            else:
                ratio = count / peak
                level = 1 if ratio <= 0.25 else 2 if ratio <= 0.5 else 3 if ratio <= 0.75 else 4
                o.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{MINT}" fill-opacity="{opacities[level]}"/>')

    ly = h - 22
    o.append(f'<text x="{x0}" y="{ly}" class="m" font-size="12" fill="{DIM}">{"public activity only" if data else "awaiting first sync"}</text>')
    lx = w - 40 - 5 * 19 - 40
    o.append(f'<text x="{lx}" y="{ly}" text-anchor="end" class="m" font-size="12" fill="{DIM}">less</text>')
    for i, level in enumerate([0, 1, 2, 3, 4]):
        fill = EMPTY if level == 0 else MINT
        op = "" if level == 0 else f' fill-opacity="{opacities[level]}"'
        o.append(f'<rect x="{lx + 10 + i*19}" y="{ly-11}" width="14" height="14" rx="3" fill="{fill}"{op}/>')
    o.append(f'<text x="{lx + 10 + 5*19 + 4}" y="{ly}" class="m" font-size="12" fill="{DIM}">more</text>')
    o.append("</svg>")
    return "".join(o)


def write(name: str, content: str) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote assets/{name}")


def main() -> int:
    if "--placeholder" in sys.argv:
        data = None
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("GITHUB_TOKEN is not set", file=sys.stderr)
            return 1
        data = summarise(fetch(token))
    write("stats.svg", render_stats(data))
    write("contributions.svg", render_contributions(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
