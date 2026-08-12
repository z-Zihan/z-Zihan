#!/usr/bin/env python3
"""Generate the theme-aware profile header and public GitHub build signal."""

import json
import os
import urllib.request
from datetime import datetime, timezone
from html import escape

USERNAME = "z-Zihan"
BASE_URL = f"https://api.github.com/users/{USERNAME}"
ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(ASSETS, exist_ok=True)


def api(url: str):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "z-Zihan-profile-bot",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())


def theme_tokens(theme: str) -> dict[str, str]:
    if theme == "dark":
        return {
            "bg": "#0b1020",
            "surface": "#111a2e",
            "surface_2": "#16213a",
            "text": "#f4f7ff",
            "muted": "#9aa8c2",
            "border": "#263553",
            "grid": "#253451",
            "blue": "#60a5fa",
            "cyan": "#22d3ee",
            "green": "#4ade80",
        }
    return {
        "bg": "#f7f9fc",
        "surface": "#ffffff",
        "surface_2": "#edf3fb",
        "text": "#111827",
        "muted": "#526178",
        "border": "#d7e0ec",
        "grid": "#dce5f0",
        "blue": "#2563eb",
        "cyan": "#0e7490",
        "green": "#16a34a",
    }


def write_asset(name: str, theme: str, svg: str) -> None:
    path = os.path.join(ASSETS, f"{name}-{theme}.svg")
    with open(path, "w", encoding="utf-8") as file:
        file.write(svg)
    print(f"generated {path} ({len(svg) / 1024:.1f} KB)")


def generate_header(theme: str) -> None:
    t = theme_tokens(theme)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="300" viewBox="0 0 920 300" role="img" aria-labelledby="title desc">
  <title id="title">Zihan — frontend engineer and AI product builder</title>
  <desc id="desc">Building local-first AI products and the interfaces that make them useful.</desc>
  <defs>
    <linearGradient id="wash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg']}"/>
      <stop offset="1" stop-color="{t['surface_2']}"/>
    </linearGradient>
    <linearGradient id="signal" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['blue']}"/>
      <stop offset="1" stop-color="{t['cyan']}"/>
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{t['grid']}" stroke-width="1" opacity=".48"/>
    </pattern>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>
  <rect x="1" y="1" width="918" height="298" rx="22" fill="url(#wash)" stroke="{t['border']}" stroke-width="2"/>
  <rect x="1" y="1" width="918" height="298" rx="22" fill="url(#grid)"/>
  <circle cx="795" cy="82" r="86" fill="{t['blue']}" opacity=".08" filter="url(#glow)"/>

  <g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">
    <rect x="48" y="42" width="300" height="28" rx="14" fill="{t['surface']}" stroke="{t['border']}"/>
    <circle cx="65" cy="56" r="4" fill="{t['green']}"/>
    <text x="78" y="61" font-size="12" font-weight="700" letter-spacing="1.2" fill="{t['muted']}">FRONTEND ENGINEER · AI BUILDER</text>
  </g>

  <text x="46" y="148" font-family="system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="76" font-weight="800" letter-spacing="-4" fill="{t['text']}">ZIHAN</text>
  <rect x="48" y="166" width="82" height="5" rx="2.5" fill="url(#signal)"/>
  <text x="48" y="204" font-family="system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="20" font-weight="650" fill="{t['text']}">Building local-first AI products</text>
  <text x="48" y="232" font-family="system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="20" fill="{t['muted']}">and the interfaces that make them useful.</text>

  <g transform="translate(614 46)" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">
    <rect width="258" height="206" rx="16" fill="{t['surface']}" stroke="{t['border']}" stroke-width="1.5"/>
    <circle cx="20" cy="20" r="4" fill="#ef4444"/>
    <circle cx="34" cy="20" r="4" fill="#f59e0b"/>
    <circle cx="48" cy="20" r="4" fill="{t['green']}"/>
    <path d="M0 39H258" stroke="{t['border']}"/>
    <text x="20" y="68" font-size="12" fill="{t['muted']}">$ current_focus</text>
    <text x="20" y="94" font-size="13" font-weight="700" fill="{t['blue']}">local-first AI</text>
    <text x="20" y="117" font-size="13" font-weight="700" fill="{t['cyan']}">agent collaboration</text>
    <text x="20" y="140" font-size="13" font-weight="700" fill="{t['text']}">interface systems</text>
    <path d="M20 165H238" stroke="{t['border']}"/>
    <circle cx="29" cy="184" r="5" fill="{t['green']}"/>
    <text x="43" y="189" font-size="11" fill="{t['muted']}">building in public</text>
  </g>
</svg>"""
    write_asset("profile-header", theme, svg)


def generate_mobile_header(theme: str) -> None:
    t = theme_tokens(theme)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="420" viewBox="0 0 680 420" role="img" aria-labelledby="title desc">
  <title id="title">Zihan — frontend engineer and AI product builder</title>
  <desc id="desc">Building local-first AI products and the interfaces that make them useful.</desc>
  <defs>
    <linearGradient id="wash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg']}"/>
      <stop offset="1" stop-color="{t['surface_2']}"/>
    </linearGradient>
    <linearGradient id="signal" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['blue']}"/>
      <stop offset="1" stop-color="{t['cyan']}"/>
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{t['grid']}" stroke-width="1" opacity=".48"/>
    </pattern>
  </defs>
  <rect x="1" y="1" width="678" height="418" rx="22" fill="url(#wash)" stroke="{t['border']}" stroke-width="2"/>
  <rect x="1" y="1" width="678" height="418" rx="22" fill="url(#grid)"/>
  <g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">
    <rect x="42" y="38" width="338" height="34" rx="17" fill="{t['surface']}" stroke="{t['border']}"/>
    <circle cx="61" cy="55" r="5" fill="{t['green']}"/>
    <text x="76" y="61" font-size="14" font-weight="700" letter-spacing="1.2" fill="{t['muted']}">FRONTEND ENGINEER · AI BUILDER</text>
  </g>
  <text x="40" y="174" font-family="system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="86" font-weight="800" letter-spacing="-4" fill="{t['text']}">ZIHAN</text>
  <rect x="42" y="194" width="96" height="6" rx="3" fill="url(#signal)"/>
  <text x="42" y="244" font-family="system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="25" font-weight="650" fill="{t['text']}">Building local-first AI products</text>
  <text x="42" y="280" font-family="system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif" font-size="25" fill="{t['muted']}">and interfaces that make them useful.</text>
  <g transform="translate(42 326)" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="14" font-weight="700">
    <rect width="176" height="46" rx="12" fill="{t['surface']}" stroke="{t['border']}"/>
    <circle cx="19" cy="23" r="5" fill="{t['blue']}"/>
    <text x="32" y="28" fill="{t['text']}">LOCAL-FIRST</text>
    <rect x="188" width="178" height="46" rx="12" fill="{t['surface']}" stroke="{t['border']}"/>
    <circle cx="207" cy="23" r="5" fill="{t['cyan']}"/>
    <text x="220" y="28" fill="{t['text']}">AGENT SYSTEMS</text>
    <rect x="378" width="210" height="46" rx="12" fill="{t['surface']}" stroke="{t['border']}"/>
    <circle cx="397" cy="23" r="5" fill="{t['green']}"/>
    <text x="410" y="28" fill="{t['text']}">BUILDING IN PUBLIC</text>
  </g>
</svg>"""
    write_asset("profile-header-mobile", theme, svg)


def load_stats() -> dict[str, str]:
    try:
        user = api(BASE_URL)
        repos = api(f"{BASE_URL}/repos?per_page=100&type=owner&sort=updated")
        created = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
        updated = max(
            datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
            for repo in repos
            if repo.get("pushed_at")
        )
        now = datetime.now(timezone.utc)
        days_ago = (now - updated).days
        if days_ago == 0:
            last_signal = "today"
        elif days_ago == 1:
            last_signal = "yesterday"
        elif days_ago < 30:
            last_signal = f"{days_ago}d ago"
        else:
            last_signal = f"{days_ago // 30}mo ago"
        return {
            "repos": str(user.get("public_repos", len(repos))),
            "stars": str(sum(repo.get("stargazers_count", 0) for repo in repos)),
            "since": str(created.year),
            "last_signal": last_signal,
        }
    except Exception as error:
        print(f"GitHub API unavailable: {error}")
        return {"repos": "5", "stars": "10", "since": "2019", "last_signal": "recently"}


def generate_build_signal(theme: str, stats: dict[str, str]) -> None:
    t = theme_tokens(theme)
    values = [
        ("PUBLIC BUILDS", stats["repos"]),
        ("STARS EARNED", stats["stars"]),
        ("ON GITHUB SINCE", stats["since"]),
        ("LAST SIGNAL", stats["last_signal"]),
    ]
    cards = []
    for index, (label, value) in enumerate(values):
        x = 30 + index * 218
        value_size = 28 if len(value) <= 7 else 22
        cards.append(
            f'''<g transform="translate({x} 54)">
    <rect width="198" height="78" rx="12" fill="{t['surface']}" stroke="{t['border']}"/>
    <rect x="14" y="14" width="4" height="50" rx="2" fill="url(#signal)"/>
    <text x="32" y="31" font-size="10" font-weight="700" letter-spacing="1.1" fill="{t['muted']}">{escape(label)}</text>
    <text x="32" y="61" font-size="{value_size}" font-weight="760" fill="{t['text']}">{escape(value)}</text>
  </g>'''
        )
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d UTC")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="920" height="168" viewBox="0 0 920 168" role="img" aria-labelledby="title desc">
  <title id="title">Live GitHub build signal</title>
  <desc id="desc">Public repository, star, account age, and recent activity statistics.</desc>
  <defs>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg']}"/>
      <stop offset="1" stop-color="{t['surface_2']}"/>
    </linearGradient>
    <linearGradient id="signal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t['blue']}"/>
      <stop offset="1" stop-color="{t['cyan']}"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="918" height="166" rx="16" fill="url(#panel)" stroke="{t['border']}" stroke-width="2"/>
  <g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">
    <circle cx="31" cy="29" r="5" fill="{t['green']}"/>
    <text x="44" y="34" font-size="12" font-weight="700" letter-spacing="1.2" fill="{t['text']}">BUILD SIGNAL</text>
    <text x="889" y="34" text-anchor="end" font-size="10" fill="{t['muted']}">UPDATED {updated}</text>
    {''.join(cards)}
  </g>
</svg>"""
    write_asset("build-signal", theme, svg)


def generate_mobile_build_signal(theme: str, stats: dict[str, str]) -> None:
    t = theme_tokens(theme)
    values = [
        ("PUBLIC BUILDS", stats["repos"]),
        ("STARS EARNED", stats["stars"]),
        ("ON GITHUB SINCE", stats["since"]),
        ("LAST SIGNAL", stats["last_signal"]),
    ]
    cards = []
    for index, (label, value) in enumerate(values):
        column = index % 2
        row = index // 2
        x = 32 + column * 316
        y = 62 + row * 116
        cards.append(
            f'''<g transform="translate({x} {y})">
    <rect width="300" height="98" rx="14" fill="{t['surface']}" stroke="{t['border']}"/>
    <rect x="16" y="17" width="5" height="64" rx="2.5" fill="url(#signal)"/>
    <text x="40" y="40" font-size="13" font-weight="700" letter-spacing="1.1" fill="{t['muted']}">{escape(label)}</text>
    <text x="40" y="75" font-size="31" font-weight="760" fill="{t['text']}">{escape(value)}</text>
  </g>'''
        )
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="316" viewBox="0 0 680 316" role="img" aria-labelledby="title desc">
  <title id="title">Live GitHub build signal</title>
  <desc id="desc">Public repository, star, account age, and recent activity statistics.</desc>
  <defs>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg']}"/>
      <stop offset="1" stop-color="{t['surface_2']}"/>
    </linearGradient>
    <linearGradient id="signal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t['blue']}"/>
      <stop offset="1" stop-color="{t['cyan']}"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="678" height="314" rx="18" fill="url(#panel)" stroke="{t['border']}" stroke-width="2"/>
  <g font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">
    <circle cx="33" cy="31" r="6" fill="{t['green']}"/>
    <text x="48" y="37" font-size="14" font-weight="700" letter-spacing="1.2" fill="{t['text']}">BUILD SIGNAL</text>
    <text x="648" y="37" text-anchor="end" font-size="11" fill="{t['muted']}">{updated}</text>
    {''.join(cards)}
  </g>
</svg>"""
    write_asset("build-signal-mobile", theme, svg)


if __name__ == "__main__":
    live_stats = load_stats()
    for selected_theme in ("light", "dark"):
        generate_header(selected_theme)
        generate_mobile_header(selected_theme)
        generate_build_signal(selected_theme, live_stats)
        generate_mobile_build_signal(selected_theme, live_stats)
    print(f"profile assets ready: {live_stats}")
