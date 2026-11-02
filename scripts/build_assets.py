#!/usr/bin/env python3
"""Build the static SVG assets for the profile README.

Run from the repository root:  python3 scripts/build_assets.py
Writes everything into assets/. The stats panels are rendered in their empty
state here; scripts/generate_stats.py fills them with real data.
"""
from __future__ import annotations

from html import escape

import generate_stats as g
from generate_stats import BG, DIM, LINE, MINT, MUTED, SURF, TEXT, svg_open, write


def titlebar(w: int, label: str, right: str | None = None) -> str:
    out = [
        f'<rect width="{w}" height="44" fill="{BG}"/>',
        f'<line x1="0" y1="44.5" x2="{w}" y2="44.5" stroke="{LINE}"/>',
    ]
    for i in range(3):
        out.append(f'<circle cx="{28 + i*20}" cy="22" r="5" fill="#1B2926"/>')
    out.append(f'<text x="96" y="27" class="m" font-size="14" fill="{MUTED}">{escape(label)}</text>')
    if right:
        out.append(f'<circle cx="{w-130}" cy="22" r="4" fill="{MINT}" class="pulse"/>')
        out.append(f'<text x="{w-28}" y="27" text-anchor="end" class="m" font-size="14" fill="{MINT}">{escape(right)}</text>')
    return "".join(out)


# --- hero -------------------------------------------------------------------
def node(x, y, label, hi=False, w=92, h=44):
    stroke = MINT if hi else "#26332F"
    fill = "#0C1D17" if hi else SURF
    colour = MINT if hi else TEXT
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}"/>'
        f'<text x="{x + w/2}" y="{y + 27}" text-anchor="middle" class="m" font-size="15" fill="{colour}">{escape(label)}</text>'
    )


def edge(x1, y1, x2, y2):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MINT}" stroke-opacity=".75" '
        f'stroke-width="1.5" class="flow" marker-end="url(#ah)"/>'
    )


def hero() -> str:
    W, H = 1200, 470
    o = [svg_open(
        W, H,
        "Javohir Nurmatjonov — Python Backend Engineer",
        "Dark terminal-style banner: the name Javohir Nurmatjonov, the title Python Backend Engineer and Team Lead, "
        "a tagline, and a small animated diagram of a client, API, Postgres, Redis, Celery worker and LLM.",
    )]
    o.append(
        f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
        f'<pattern id="gr" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" stroke="#0E1715" stroke-width="1"/></pattern>'
        f'<radialGradient id="glow" cx="0.8" cy="0.5" r="0.55"><stop offset="0" stop-color="{MINT}" stop-opacity="0.12"/>'
        f'<stop offset="1" stop-color="{MINT}" stop-opacity="0"/></radialGradient>'
        f'<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M1 1L9 5L1 9Z" fill="{MINT}"/></marker></defs>'
    )
    o.append('<g clip-path="url(#c)">')
    o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#gr)"/><rect width="{W}" height="{H}" fill="url(#glow)"/>')
    o.append(titlebar(W, "javoxirone@tashkent  ~/profile  —  zsh", "SYS.ONLINE"))

    # left column
    o.append(
        f'<text x="64" y="120" class="m" font-size="18" letter-spacing="3" fill="{MINT}">PYTHON BACKEND ENGINEER'
        f'<tspan fill="{DIM}">  /  </tspan><tspan fill="{MUTED}">TEAM LEAD</tspan></text>'
    )
    o.append(f'<text x="64" y="222" class="s" font-size="104" font-weight="800" fill="{TEXT}" textLength="410" lengthAdjust="spacingAndGlyphs">Javohir</text>')
    o.append(f'<text x="64" y="322" class="s" font-size="104" font-weight="800" fill="{TEXT}" textLength="620" lengthAdjust="spacingAndGlyphs">Nurmatjonov</text>')
    o.append(f'<rect x="700" y="250" width="22" height="72" fill="{MINT}" class="blink"/>')
    o.append(f'<line x1="64" y1="360.5" x2="700" y2="360.5" stroke="{LINE}"/>')
    o.append(
        f'<text x="64" y="404" class="m" font-size="25"><tspan fill="{MINT}">›</tspan>'
        f'<tspan fill="#C9D6D0"> Systems that stay up. Intelligence that earns its place.</tspan></text>'
    )
    o.append(f'<text x="64" y="445" class="m" font-size="16" fill="{MUTED}">Tashkent, Uzbekistan  ·  UTC+5  ·  CS @ Webster University</text>')

    # architecture panel
    o.append(f'<rect x="736.5" y="76.5" width="427" height="299" rx="12" fill="{SURF}" fill-opacity=".85" stroke="{LINE}"/>')
    o.append(f'<text x="760" y="104" class="m" font-size="12" letter-spacing="2" fill="{DIM}">ARCHITECTURE</text>')
    o.append(edge(852, 144, 906, 144))
    o.append(edge(1000, 144, 1054, 144))
    o.append(edge(954, 166, 954, 210))
    o.append(edge(1000, 234, 1054, 234))
    o.append(edge(1102, 212, 1102, 168))
    o.append(edge(1102, 256, 1102, 300))
    o.append(node(760, 122, "client"))
    o.append(node(908, 122, "api", hi=True))
    o.append(node(1056, 122, "postgres"))
    o.append(node(908, 212, "redis"))
    o.append(node(1056, 212, "celery"))
    o.append(node(1056, 302, "llm"))
    o.append(f'<text x="760" y="352" class="m" font-size="12" fill="{DIM}">request → queue → worker → store</text>')
    o.append("</g>")
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" stroke="{LINE}"/>')
    o.append("</svg>")
    return "".join(o)


# --- terminal ---------------------------------------------------------------
def terminal() -> str:
    W = 1000
    rows = [
        ("whoami", "Python Backend Engineer building production systems."),
        ("current_focus", "Backend architecture / PostgreSQL / AI engineering."),
        ("current_roles", "Smart Aurum / Techna."),
        ("education", "Computer Science @ Webster University."),
    ]
    top, pitch = 100, 100
    H = top + len(rows) * pitch + 70
    o = [svg_open(
        W, H, "Terminal introduction",
        "A terminal window running whoami, current_focus, current_roles and education.",
    )]
    o.append(f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>')
    o.append('<g clip-path="url(#c)">')
    o.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    o.append(titlebar(W, "zsh — javoxirone@tashkent"))
    for i, (cmd, out) in enumerate(rows):
        y = top + i * pitch
        o.append(
            f'<g class="in" style="animation-delay:{i * 0.7:.1f}s">'
            f'<text x="40" y="{y}" class="m" font-size="26"><tspan fill="{MINT}">$</tspan><tspan fill="{TEXT}"> {escape(cmd)}</tspan></text>'
            f'<text x="40" y="{y + 40}" class="m" font-size="26" fill="#9FB3AB">{escape(out)}</text></g>'
        )
    py = top + len(rows) * pitch
    o.append(f'<text x="40" y="{py}" class="m" font-size="26" fill="{MINT}">$</text>')
    o.append(f'<rect x="72" y="{py - 22}" width="15" height="28" fill="{MINT}" class="blink"/>')
    o.append("</g>")
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" stroke="{LINE}"/>')
    o.append("</svg>")
    return "".join(o)


# --- section headers --------------------------------------------------------
def section(idx: str, label: str, path: str) -> str:
    W, H = 1000, 64
    o = [svg_open(W, H, f"{label} section", f"Section heading: {label}")]
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{BG}" stroke="{LINE}"/>')
    o.append(f'<rect x="0" y="16" width="3" height="{H-32}" fill="{MINT}"/>')
    o.append(f'<text x="28" y="39" class="m" font-size="16" fill="{MINT}">{idx}</text>')
    o.append(f'<text x="68" y="42" class="s" font-size="30" font-weight="700" fill="{TEXT}">{escape(label)}</text>')
    o.append(f'<line x1="440" y1="32.5" x2="850" y2="32.5" stroke="{LINE}"/>')
    o.append(f'<circle cx="440" cy="32.5" r="3" fill="{MINT}"/>')
    o.append(f'<text x="{W-24}" y="37" text-anchor="end" class="m" font-size="14" fill="{DIM}">{escape(path)}</text>')
    o.append("</svg>")
    return "".join(o)


# --- experience cards -------------------------------------------------------
def experience(idx: str, name: str, suffix: str | None, role: str, period: str) -> str:
    W, H = 1000, 200
    full = name + (f" / {suffix}" if suffix else "")
    o = [svg_open(W, H, f"{full} — {role}, {period}", f"Experience card for {full}. Role: {role}. Period: {period}.")]
    o.append(f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>')
    o.append('<g clip-path="url(#c)">')
    o.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    o.append(f'<text x="{W-30}" y="182" text-anchor="end" class="s" font-size="140" font-weight="800" fill="#0F1917">{idx}</text>')
    o.append(f'<rect width="6" height="{H}" fill="{MINT}"/>')
    o.append(f'<text x="40" y="56" class="m" font-size="16" letter-spacing="2" fill="{MINT}">{idx}<tspan fill="{DIM}"> / CURRENT</tspan></text>')
    o.append(f'<circle cx="{W-198}" cy="50" r="4" fill="{MINT}" class="pulse"/>')
    o.append(f'<text x="{W-36}" y="56" text-anchor="end" class="m" font-size="18" fill="{TEXT}">{escape(period)}</text>')
    tail = f'<tspan fill="{DIM}" font-weight="400"> / {escape(suffix)}</tspan>' if suffix else ""
    o.append(f'<text x="40" y="128" class="s" font-size="56" font-weight="800" fill="{TEXT}">{escape(name)}{tail}</text>')
    o.append(f'<text x="40" y="170" class="m" font-size="22" fill="{MINT}">{escape(role)}</text>')
    o.append("</g>")
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" stroke="{LINE}"/>')
    o.append("</svg>")
    return "".join(o)


# --- toolkit "periodic table" ----------------------------------------------
TILES = [
    ("Py", "Python", "LANG"), ("Dj", "Django", "BACKEND"), ("Fa", "FastAPI", "BACKEND"), ("Sa", "SQLAlchemy", "BACKEND"),
    ("Pg", "PostgreSQL", "DATA"), ("Rd", "Redis", "DATA"), ("Pv", "pgvector", "DATA"),
    ("Dk", "Docker", "INFRA"), ("Lx", "Linux", "INFRA"), ("Nx", "Nginx", "INFRA"), ("Aw", "AWS", "INFRA"),
    ("Cf", "Cloudflare", "INFRA"), ("Ce", "Celery", "TOOLS"), ("Gt", "Git", "TOOLS"),
]


def toolkit() -> str:
    W, tw, th, gap, per_row = 1000, 124, 120, 22, 7
    rows = (len(TILES) + per_row - 1) // per_row
    H = rows * th + (rows - 1) * gap
    o = [svg_open(W, H, "Engineering toolkit", "Periodic-table style grid of tools: " + ", ".join(t[1] for t in TILES) + ".")]
    for i, (sym, name, tag) in enumerate(TILES):
        x = (i % per_row) * (tw + gap)
        y = (i // per_row) * (th + gap)
        hi = name in {"Python", "PostgreSQL"}
        o.append(f'<rect x="{x+.5}" y="{y+.5}" width="{tw-1}" height="{th-1}" rx="12" fill="{SURF}" stroke="{MINT if hi else LINE}" stroke-opacity="{1 if hi else 1}"/>')
        o.append(f'<text x="{x+12}" y="{y+24}" class="m" font-size="12" fill="{DIM}">{i+1:02d}</text>')
        o.append(f'<text x="{x+tw-12}" y="{y+24}" text-anchor="end" class="m" font-size="10" letter-spacing="1" fill="{DIM}">{tag}</text>')
        o.append(f'<text x="{x+tw/2}" y="{y+72}" text-anchor="middle" class="m" font-size="40" font-weight="700" fill="{MINT}">{sym}</text>')
        o.append(f'<text x="{x+tw/2}" y="{y+103}" text-anchor="middle" class="m" font-size="16" fill="{MUTED}">{escape(name)}</text>')
    o.append("</svg>")
    return "".join(o)


# --- contact buttons --------------------------------------------------------
def button(label: str, value: str, w: int) -> str:
    h = 64
    return (
        svg_open(w, h, f"{label}: {value}", f"Link button: {label} — {value}")
        + f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="10" fill="{SURF}" stroke="{LINE}"/>'
        + f'<rect x="0" y="14" width="3" height="{h-28}" fill="{MINT}"/>'
        + f'<text x="22" y="26" class="m" font-size="12" letter-spacing="2" fill="{MINT}">{escape(label.upper())}</text>'
        + f'<text x="22" y="47" class="m" font-size="18" fill="{TEXT}">{escape(value)}</text>'
        + "</svg>"
    )


def closing() -> str:
    W, H = 1000, 64
    return (
        svg_open(W, H, "End of profile", "Closing terminal prompt")
        + f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{BG}" stroke="{LINE}"/>'
        + f'<text x="28" y="39" class="m" font-size="18"><tspan fill="{MINT}">javoxirone@tashkent</tspan><tspan fill="{DIM}">:</tspan><tspan fill="{TEXT}">~</tspan><tspan fill="{DIM}">$</tspan></text>'
        + f'<rect x="276" y="21" width="11" height="22" fill="{MINT}" class="blink"/>'
        + "</svg>"
    )


def main() -> None:
    write("hero.svg", hero())
    write("terminal.svg", terminal())
    write("section-experience.svg", section("01", "Experience", "~/career"))
    write("section-toolkit.svg", section("02", "Toolkit", "~/stack"))
    write("section-activity.svg", section("03", "Activity", "~/github"))
    write("section-contact.svg", section("04", "Contact", "~/reach"))
    write("exp-smart-aurum.svg", experience("01", "Smart Aurum", "DaisyAI", "Backend Engineer / Team Lead", "2026 — PRESENT"))
    write("exp-techna.svg", experience("02", "Techna", None, "Python Backend Engineer", "2026 — PRESENT"))
    write("toolkit.svg", toolkit())
    write("btn-web.svg", button("Website", "nurmatjonov.uz", 200))
    write("btn-linkedin.svg", button("LinkedIn", "javohir-nurmatjonov", 250))
    write("btn-telegram.svg", button("Telegram", "@javoxirone", 170))
    write("btn-email.svg", button("Email", "javoxirone@gmail.com", 270))
    write("end.svg", closing())
    write("stats.svg", g.render_stats(None))
    write("contributions.svg", g.render_contributions(None))


if __name__ == "__main__":
    main()
