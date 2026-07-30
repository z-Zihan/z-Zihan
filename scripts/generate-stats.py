#!/usr/bin/env python3
"""Generate vibe-coding SVGs with live GitHub stats — Glassmorphism redesign."""

import json
import os
import urllib.request
from datetime import datetime, timezone

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


def generate_svg(theme: str) -> None:
    try:
        user = api(BASE_URL)
        repos = api(f"{BASE_URL}/repos?per_page=50&type=owner&sort=updated")
        stars = sum(r.get("stargazers_count", 0) for r in repos)
        followers = user.get("followers", 0)
        repo_count = user.get("public_repos", len(repos))
        created = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        years = (now - created).days // 365

        updated = datetime.fromisoformat(user["updated_at"].replace("Z", "+00:00"))
        days_ago = (now - updated).days
        if days_ago == 0:
            last_active = "today"
        elif days_ago == 1:
            last_active = "yesterday"
        elif days_ago < 30:
            last_active = f"{days_ago}d ago"
        elif days_ago < 365:
            last_active = f"{days_ago // 30}m ago"
        else:
            last_active = f"{days_ago // 365}y ago"
    except Exception as e:
        print(f"⚠️ API error: {e}")
        stars, followers, repo_count, years, last_active = 6, 6, 2, 7, "recently"

    dark = theme == "dark"
    bg = "#0d1117" if dark else "#ffffff"
    text = "#e6edf3" if dark else "#24292f"
    muted = "#7d8590" if dark else "#656d76"
    border = "#30363d" if dark else "#d0d7de"
    card_bg = "#161b22" if dark else "#f6f8fa"
    card_border = "#21262d" if dark else "#d0d7de"

    stats = [
        ("⭐", "Total Stars", str(stars)),
        ("👥", "Followers", str(followers)),
        ("📦", "Public Repos", str(repo_count)),
        ("📅", "GitHub Since", f"{years}y"),
        ("🕐", "Last Active", last_active),
    ]

    W = 840
    H = 165
    card_w = 140
    card_h = 72
    card_gap = 14
    total_w = len(stats) * card_w + (len(stats) - 1) * card_gap
    start_x = (W - total_w) / 2
    card_y = 58

    cards_svg = ""
    for i, (icon, label, value) in enumerate(stats):
        x = start_x + i * (card_w + card_gap)
        cx = x + card_w / 2

        cards_svg += f"""
  <rect x="{x:.0f}" y="{card_y}" width="{card_w}" height="{card_h}" rx="10"
        fill="{card_bg}" stroke="{card_border}" stroke-width="1"/>"""
        cards_svg += f"""
  <rect x="{x + 10:.0f}" y="{card_y}" width="{card_w - 20}" height="2" rx="1"
        fill="url(#accent)" opacity="0.45"/>"""
        cards_svg += f"""
  <text x="{cx:.0f}" y="{card_y + 24}" font-family="system-ui,-apple-system,sans-serif"
        font-size="11" fill="{muted}" text-anchor="middle">{icon} {label}</text>"""
        v_size = 26 if len(value) <= 3 else 20 if len(value) <= 6 else 16
        cards_svg += f"""
  <text x="{cx:.0f}" y="{card_y + 52}" font-family="system-ui,-apple-system,sans-serif"
        font-size="{v_size}" font-weight="700" fill="{text}" text-anchor="middle">{value}</text>"""

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{card_bg}"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8b5cf6"/>
      <stop offset="50%" stop-color="#ec4899"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" rx="12" fill="url(#bgGrad)" stroke="{border}" stroke-width="1"/>

  <text x="30" y="34" font-family="system-ui,-apple-system,sans-serif" font-size="14"
        font-weight="700" fill="{text}">⚡ Vibe Coding Stats</text>
  <rect x="30" y="40" width="70" height="2.5" rx="1.25" fill="url(#accent)"/>
{cards_svg}

  <rect x="30" y="{H - 12}" width="{W - 60}" height="1" rx="0.5" fill="url(#accent)" opacity="0.3"/>
  <text x="{W - 28}" y="{H - 16}" font-family="system-ui,-apple-system,sans-serif" font-size="9"
        fill="{muted}" text-anchor="end">Updated {date_str}</text>
</svg>"""

    out = os.path.join(ASSETS, f"vibe-coding-{theme}.svg")
    with open(out, "w") as f:
        f.write(svg)
    size_kb = len(svg) / 1024
    print(f"✅ {out} ({size_kb:.1f} KB) — ⭐{stars} 👥{followers} 📦{repo_count}")


if __name__ == "__main__":
    generate_svg("dark")
    generate_svg("light")
    print("🎉 Done!")
