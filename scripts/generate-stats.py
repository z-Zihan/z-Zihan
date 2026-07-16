#!/usr/bin/env python3
"""Generate vibe-coding SVGs with live GitHub stats."""

import json
import math
import os
import urllib.request
from datetime import datetime

USERNAME = "z-Zihan"
BASE_URL = f"https://api.github.com/users/{USERNAME}"
ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(ASSETS, exist_ok=True)


def api(url: str) -> dict:
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "z-Zihan-stats-bot",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def lang_color(name: str) -> str:
    colors = {
        "Python": "#3776AB",
        "JavaScript": "#F7DF1E",
        "TypeScript": "#3178C6",
        "Vue": "#4FC08D",
        "CSS": "#1572B6",
        "HTML": "#E34F26",
        "Shell": "#89E051",
        "Dockerfile": "#2496ED",
    }
    return colors.get(name, "#8b949e")


def svg_lang_gradient_stops(langs: list[tuple[str, float]]) -> str:
    """Build a horizontal gradient from language colors."""
    total = sum(pct for _, pct in langs)
    stops = []
    offset = 0
    for name, pct in langs:
        frac = pct / total
        color = lang_color(name)
        stops.append(f"""<stop offset="{offset:.1%}" stop-color="{color}"/>""")
        stops.append(f"""<stop offset="{(offset+frac):.1%}" stop-color="{color}"/>""")
        offset += frac
    return "\n      ".join(stops)


def generate_svg(theme: str) -> None:
    """Generate a single theme SVG."""
    try:
        user = api(BASE_URL)
        repos = api(f"{BASE_URL}/repos?per_page=50&type=owner&sort=updated")
        stars = sum(r.get("stargazers_count", 0) for r in repos)
        followers = user.get("followers", 0)
        created = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
        years = (datetime.utcnow() - created.replace(tzinfo=None)).days // 365
    except Exception as e:
        print(f"⚠️ API error: {e}")
        stars, followers, years = 6, 3, 7

    # Aggregate languages
    lang_totals: dict[str, int] = {}
    for r in repos:
        lang = r.get("language")
        if lang:
            lang_totals[lang] = lang_totals.get(lang, 0) + 1
    total = sum(lang_totals.values()) or 1
    top_langs = sorted(lang_totals.items(), key=lambda x: -x[1])[:5]

    # Language bar data: each row is (name, count, pct, pct_str)
    lang_rows = [(n, c, c / total, f"{c/total:.0%}") for n, c in top_langs]

    dark = theme == "dark"
    bg = "#0d1117" if dark else "#ffffff"
    bg2 = "#161b22" if dark else "#f6f8fa"
    text = "#e6edf3" if dark else "#24292f"
    muted = "#7d8590" if dark else "#656d76"
    border = "#30363d" if dark else "#d0d7de"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    # Read README to get the vibe-coding block without duplicating
    readme_path = os.path.join(repo_root, "README.md")

    # Build lang bars
    bars = ""
    y = 172
    for name, count, pct, pct_str in lang_rows:
        bar_w = max(int(200 * pct), 4)
        bars += f"""
  <text x="30" y="{y}" font-family="system-ui, sans-serif" font-size="12" fill="{text}">{name}</text>
  <rect x="100" y="{y-8}" width="{bar_w}" height="10" rx="5" fill="{lang_color(name)}">
    <animate attributeName="width" values="0;{bar_w}" dur="1s" begin="1.1s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
  </rect>
  <text x="{108 + bar_w}" y="{y}" font-family="system-ui, sans-serif" font-size="11" fill="{muted}">{pct_str}</text>"""
        y += 22

    # Height based on number of language rows
    svg_height = max(210, 170 + len(lang_rows) * 22)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="{svg_height}" viewBox="0 0 840 {svg_height}" fill="none">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{bg2}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8b5cf6"/>
      <stop offset="50%" stop-color="#ec4899"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="840" height="{svg_height}" rx="16" fill="url(#bgGrad)" stroke="{border}" stroke-width="1"/>

  <text x="30" y="42" font-family="system-ui, sans-serif" font-size="18" font-weight="700" fill="{text}">⚡ Vibe Coding Stats</text>
  <rect x="30" y="50" width="0" height="3" rx="1.5" fill="url(#accent)">
    <animate attributeName="width" values="0;120" dur="1s" fill="freeze"/>
  </rect>

  <text x="30" y="85" font-family="system-ui, sans-serif" font-size="13" fill="{muted}">⭐ Total Stars</text>
  <text x="30" y="110" font-family="system-ui, sans-serif" font-size="28" font-weight="700" fill="{text}" filter="url(#glow)">{stars}</text>

  <text x="180" y="85" font-family="system-ui, sans-serif" font-size="13" fill="{muted}">👥 Followers</text>
  <text x="180" y="110" font-family="system-ui, sans-serif" font-size="28" font-weight="700" fill="{text}" filter="url(#glow)">{followers}</text>

  <text x="340" y="85" font-family="system-ui, sans-serif" font-size="13" fill="{muted}">📦 Repos</text>
  <text x="340" y="110" font-family="system-ui, sans-serif" font-size="28" font-weight="700" fill="{text}" filter="url(#glow)">{len(repos)}</text>

  <text x="500" y="85" font-family="system-ui, sans-serif" font-size="13" fill="{muted}">📅 GitHub Since</text>
  <text x="500" y="110" font-family="system-ui, sans-serif" font-size="24" font-weight="700" fill="{text}" filter="url(#glow)">{years} years</text>

  <text x="640" y="85" font-family="system-ui, sans-serif" font-size="13" fill="{muted}">🕐 Updated</text>
  <text x="640" y="110" font-family="system-ui, sans-serif" font-size="13" fill="{muted}">{datetime.utcnow().strftime("%Y-%m-%d")}</text>

  <line x1="30" y1="132" x2="810" y2="132" stroke="{border}" stroke-width="1"/>

  <text x="30" y="158" font-family="system-ui, sans-serif" font-size="13" fill="{muted}">🔧 Languages</text>
{bars}

  <circle cx="815" cy="30" r="4" fill="#06b6d4">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="788" y="42" font-family="system-ui, sans-serif" font-size="10" fill="{muted}" text-anchor="end">LIVE</text>

  <rect x="0" y="{svg_height-4}" width="840" height="4" rx="2" fill="url(#accent)" opacity="0.6">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="3s" repeatCount="indefinite"/>
  </rect>
</svg>"""

    out = os.path.join(ASSETS, f"vibe-coding-{theme}.svg")
    with open(out, "w") as f:
        f.write(svg)
    size_kb = len(svg) / 1024
    print(f"✅ {out} ({size_kb:.1f} KB) — ⭐{stars} 👥{followers} 📦{len(repos)}")


if __name__ == "__main__":
    generate_svg("dark")
    generate_svg("light")
    print("🎉 Done!")
