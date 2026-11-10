#!/usr/bin/env python3
"""Generate project cards for the GitHub profile README (en/zh, light/dark aware).

Design v4 (2026-11-10 redesign):
- Wide flat layout 460x110 (aspect 4.19:1) — renders ~45% col width at ~110px tall,
  denser and calmer than the old 300x150 (aspect 2:1) cards.
- Accent per project, subtle corner blob, right-arrow affordance, 3 tech chips max.
- All <picture> friendly: theme switched via CSS media query inside the SVG.
"""

import os
from xml.sax.saxutils import escape as xml_escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "cards")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- common svg

FONT_STACK = "-apple-system, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif"

ARROW_ICON = '<g class="ext-link" transform="translate({x},{y})"><path d="M7 7H17M17 7V17M17 7L7 17"/></g>'

SVG_TMPL = """<svg xmlns="http://www.w3.org/2000/svg" width="460" height="110" viewBox="0 0 460 110" role="img" aria-labelledby="title desc">
  <title id="title">{name}</title>
  <desc id="desc">{desc_attr}</desc>
  <defs>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop class="bg-a" offset="0"/>
      <stop class="bg-b" offset="1"/>
    </linearGradient>
    <linearGradient id="tileGrad" x1="0" y1="0" x2="1" y2="1">
      <stop class="tile-a" offset="0"/>
      <stop class="tile-b" offset="1"/>
    </linearGradient>
    <linearGradient id="iconGrad" x1="0" y1="0" x2="1" y2="1">
      <stop class="ic-a" offset="0"/>
      <stop class="ic-b" offset="1"/>
    </linearGradient>
    <filter id="blobBlur" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <style>
      .bg-a {{ stop-color: #f8fafc; }}
      .bg-b {{ stop-color: #eef2f8; }}
      .tile-a {{ stop-color: {tile_a}; }}
      .tile-b {{ stop-color: {tile_b}; }}
      .ic-a {{ stop-color: {ic_a}; }}
      .ic-b {{ stop-color: {ic_b}; }}
      .card {{ fill: url(#cardGrad); stroke: #d9e1ec; }}
      .blob {{ fill: url(#iconGrad); opacity: 0.08; }}
      .tile {{ fill: url(#tileGrad); }}
      .icon {{ fill: none; stroke: url(#iconGrad); stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }}
      .ext-link {{ fill: none; stroke: {ic_b}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; opacity: 0.65; }}
      .name {{ fill: #0f172a; font: 700 17px {font_stack}; }}
      .desc {{ fill: #57606a; font: 400 12.5px {font_stack}; }}
      .divider {{ stroke: #e3e9f2; }}
      .chip-bg {{ fill: {chip_bg}; }}
      .chip-text {{ fill: {ic_a}; font: 600 10px {font_stack}; }}
      @media (prefers-color-scheme: dark) {{
        .bg-a {{ stop-color: #161b22; }}
        .bg-b {{ stop-color: #1a2029; }}
        .tile-a {{ stop-color: {tile_a_dark}; }}
        .tile-b {{ stop-color: {tile_b_dark}; }}
        .ic-a {{ stop-color: {ic_b}; }}
        .ic-b {{ stop-color: {ic_b_dark}; }}
        .card {{ stroke: #30363d; }}
        .blob {{ opacity: 0.11; }}
        .ext-link {{ stroke: {ic_b_dark}; opacity: 0.7; }}
        .name {{ fill: #e6edf3; }}
        .desc {{ fill: #8b949e; }}
        .divider {{ stroke: #242c38; }}
        .chip-bg {{ fill: {chip_bg_dark}; }}
        .chip-text {{ fill: {ic_b_dark}; }}
      }}
    </style>
  </defs>
  <rect class="card" x="1" y="1" width="458" height="108" rx="16"/>
  <circle class="blob" cx="416" cy="98" r="44" filter="url(#blobBlur)"/>
  <rect class="tile" x="16" y="25" width="52" height="52" rx="13"/>
  {icon}
  {arrow}
  <text class="name" x="88" y="42">{name}</text>
  <text class="desc" x="88" y="63">{desc1}</text>
  <text class="desc" x="88" y="80">{desc2}</text>
  <line class="divider" x1="88" y1="94" x2="404" y2="94"/>
{chips}
</svg>"""

CHIP_TMPL = '  <rect class="chip-bg" x="{x:.1f}" y="97" width="{w:.1f}" height="19" rx="9.5"/>\n'\
             '  <text class="chip-text" x="{tx:.1f}" y="110">{label}</text>'


def chip_w(label: str) -> float:
    # 10px semibold: CJK/fullwidth ~10.0, ascii ~6.1, plus 2*8 padding
    w = sum(10.0 if ord(c) > 0x2E7F else 6.1 for c in label)
    return w + 16


def build_chips(labels):
    parts = []
    x = 88.0
    for label in labels:
        w = chip_w(label)
        parts.append(CHIP_TMPL.format(x=x, w=w, tx=x + 8, label=xml_escape(label)))
        x += w + 8
    return "\n".join(parts)


def render(key: str, spec: dict):
    chips = build_chips(spec["chips"][:3])
    icon = (
        f'<g class="icon" transform="{spec["icon_transform"]}">{spec["icon"]}</g>'
        if spec.get("icon_transform")
        else f'<g class="icon">{spec["icon"]}</g>'
    )
    svg = SVG_TMPL.format(
        font_stack=FONT_STACK,
        name=spec["name"],
        desc_attr=spec["desc_attr"],
        desc1=spec["desc1"],
        desc2=spec["desc2"],
        icon=icon,
        arrow=ARROW_ICON.format(x=414, y=32),
        chips=chips,
        **spec["colors"],
    )
    for lang in ("en", "zh"):
        path = os.path.join(OUT, f"{key}-{lang}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path)

### ---------------------------------------------------------------- projects

P = {
    # ---- keep legacy brand colors/icons -----------------------------------
    "chorus": dict(
        name="Chorus",
        desc_attr="Local-first workspace for AI agents to communicate and collaborate across CLIs, devices, and teams.",
        desc1="Local-first workspace where AI agents communicate",
        desc2="and collaborate across CLIs, devices, and teams.",
        colors=dict(
            tile_a="#efe7fd", tile_b="#ddccfa", ic_a="#7c3aed", ic_b="#a78bfa",
            ic_b_dark="#d8b4fe", tile_a_dark="#241f38", tile_b_dark="#2f2748",
            chip_bg="#f0e9fe", chip_bg_dark="#241f38",
        ),
        icon='<circle cx="12" cy="4.8" r="2.3"/><circle cx="4.7" cy="18.1" r="2.3"/><circle cx="19.3" cy="18.1" r="2.3"/><path d="M10.5 6.7L6.2 16.1M13.5 6.7l4.3 9.4M6.9 18.1h10.2"/>',
        icon_transform="translate(26.5,27.5)",
        chips=["TypeScript", "Agent", "Local-first"],
    ),
    "evir": dict(
        name="Evir",
        desc_attr="Local-first desktop AI agent powered by your own models — files, terminal, tools.",
        desc1="Local-first desktop AI agent powered by",
        desc2="your own models — files, terminal, tools.",
        colors=dict(
            tile_a="#e3f8f2", tile_b="#c7f1e4", ic_a="#0d9488", ic_b="#2dd4bf",
            ic_b_dark="#5eead4", tile_a_dark="#16302c", tile_b_dark="#163c36",
            chip_bg="#e3f8f2", chip_bg_dark="#16302c",
        ),
        icon='<rect x="3.2" y="5" width="17.6" height="14" rx="3"/><path d="M7 10.4l2.6 2.1-2.6 2.1"/><path d="M12.6 14.5h4.2"/>',
        icon_transform="translate(26.5,27)",
        chips=["TypeScript", "React", "Tauri"],
    ),
    "llm-101": dict(
        name="LLM-101",
        desc_attr="A knowledge map from zero to AI: LLM, RAG, Agent, MCP and coding agents.",
        desc1="A zero-to-one knowledge map: LLM → RAG → Agent",
        desc2="→ MCP → coding agents, built for real beginners.",
        colors=dict(
            tile_a="#dbeafe", tile_b="#bfdbfe", ic_a="#2563eb", ic_b="#60a5fa",
            ic_b_dark="#93c5fd", tile_a_dark="#1c2a44", tile_b_dark="#1e3352",
            chip_bg="#dbeafe", chip_bg_dark="#1c2a44",
        ),
        icon='<circle cx="12" cy="12" r="2.3"/><circle cx="5" cy="5.3" r="1.7"/><circle cx="19" cy="5.3" r="1.7"/><circle cx="5" cy="18.7" r="1.7"/><circle cx="19" cy="18.7" r="1.7"/><path d="M9.9 10.1L6.3 6.7M14.1 10.1l3.6-3.4M9.9 13.9l-3.6 3.4M14.1 13.9l3.6 3.4"/>',
        icon_transform="translate(26.5,26.5)",
        chips=["AI", "课程 / Course", "中文"],
    ),
    "awesome-skills": dict(
        name="awesome-skills",
        desc_attr="A curated collection of daily development skills, frontend knowledge, and useful tools.",
        desc1="Curated agent skills, frontend knowledge and",
        desc2="engineering practices — published to ClawHub via CI.",
        colors=dict(
            tile_a="#fce7f3", tile_b="#fbcfe8", ic_a="#db2777", ic_b="#f472b6",
            ic_b_dark="#f9a8d4", tile_a_dark="#36192b", tile_b_dark="#3f1e33",
            chip_bg="#fce7f3", chip_bg_dark="#36192b",
        ),
        icon='<path d="M13.2 2.6L5.6 13.4h5.2l-1 8 8.4-11.2h-5.6z"/>',
        icon_transform="translate(26.5,26.5)",
        chips=["OpenClaw", "CI/CD", "ClawHub"],
    ),
    "build-meta-injector": dict(
        name="build-meta-injector",
        desc_attr="Inject build time, version, environment and Git metadata into HTML across Vite, Webpack, Rollup, Rspack and esbuild.",
        desc1="Inject build time, version & Git metadata into HTML.",
        desc2="Works with Vite, Webpack, Rollup, Rspack, esbuild.",
        colors=dict(
            tile_a="#fef3c7", tile_b="#fde68a", ic_a="#d97706", ic_b="#fbbf24",
            ic_b_dark="#fcd34d", tile_a_dark="#33240e", tile_b_dark="#3d2b10",
            chip_bg="#fef3c7", chip_bg_dark="#33240e",
        ),
        icon='<path d="M12 3.2l7.6 4.3v8.6L12 20.4l-7.6-4.3V7.5z"/><path d="M12 11.8V3.2M12 11.8l7.6-4.3M12 11.8l-7.6-4.3"/>',
        icon_transform="translate(26.5,26)",
        chips=["Vite", "Webpack", "Plugin"],
    ),
    # ---- new cards ----------------------------------------------------------
    "study-mode": dict(
        name="study-mode",
        desc_attr="A browser extension that turns distracting tabs into calm study mode.",
        desc1="Browser extension that turns distracting tabs into",
        desc2="a calm, focused study space. Manifest V3.",
        colors=dict(
            tile_a="#e0f2fe", tile_b="#bae6fd", ic_a="#0284c7", ic_b="#38bdf8",
            ic_b_dark="#7dd3fc", tile_a_dark="#12283a", tile_b_dark="#153349",
            chip_bg="#e0f2fe", chip_bg_dark="#12283a",
        ),
        icon='<rect x="3.5" y="5" width="17" height="12.5" rx="2.4"/><path d="M3.5 8.8h17"/><path d="M6.4 6.9h.01M9 6.9h.01M11.6 6.9h.01"/><path d="M9.4 21h5.2M12 17.5V21"/>',
        icon_transform="translate(26.5,26.8)",
        chips=["Extension", "MV3", "TypeScript"],
    ),
    "my-personal-site": dict(
        name="my-personal-site",
        desc_attr="Personal blog and portfolio — React 19, Vite, Supabase, deployed on Vercel Edge.",
        desc1="Personal blog & portfolio with 52 curated",
        desc2="deep-dives. React 19 · Supabase · Vercel Edge.",
        colors=dict(
            tile_a="#e0e7ff", tile_b="#c7d2fe", ic_a="#4f46e5", ic_b="#818cf8",
            ic_b_dark="#a5b4fc", tile_a_dark="#1e2142", tile_b_dark="#232850",
            chip_bg="#e0e7ff", chip_bg_dark="#1e2142",
        ),
        icon='<path d="M12 3.2l8 3.6v5.4c0 4.9-3.4 8.1-8 9.6-4.6-1.5-8-4.7-8-9.6V6.8z"/><path d="M8.6 11.6l2.3 2.3 4.5-4.5"/>',
        icon_transform="translate(26.5,26.5)",
        chips=["React 19", "Supabase", "PWA"],
    ),
}

### ---------------------------------------------------------------- zh copy

ZH = {
    "chorus": dict(
        name="Chorus",
        desc_attr="AI Agent 的本地优先协作工作区，跨 CLI、设备与团队沟通协作。",
        desc1="AI Agent 的本地优先协作工作区，",
        desc2="跨 CLI、设备与团队沟通与协作。",
        chips=["TypeScript", "Agent", "本地优先"],
    ),
    "evir": dict(
        name="Evir",
        desc_attr="由你自己的模型驱动的本地优先桌面 AI Agent——文件、终端、工具。",
        desc1="由你自己的模型驱动的本地优先桌面 Agent，",
        desc2="文件、终端、工具全掌控。",
        chips=["TypeScript", "React", "Tauri"],
    ),
    "llm-101": dict(
        name="LLM-101",
        desc_attr="从 0 开始的 AI 知识地图：LLM、RAG、Agent、MCP、Coding Agent。",
        desc1="从 0 开始的 AI 知识地图：",
        desc2="LLM → RAG → Agent → MCP → Coding Agent。",
        chips=["AI", "课程 / Course", "中文"],
    ),
    "awesome-skills": dict(
        name="awesome-skills",
        desc_attr="日常开发技能、前端知识与工程实践的精选合集，经 CI 自动发布到 ClawHub。",
        desc1="日常开发技能、前端知识与工程实践精选，",
        desc2="经 CI 自动发布到 ClawHub。",
        chips=["OpenClaw", "CI/CD", "ClawHub"],
    ),
    "build-meta-injector": dict(
        name="build-meta-injector",
        desc_attr="把构建时间、版本、环境与 Git 元数据注入 HTML，支持 Vite、Webpack、Rollup、Rspack、esbuild。",
        desc1="把构建时间、版本与 Git 元数据注入 HTML，",
        desc2="支持 Vite / Webpack / Rollup / Rspack / esbuild。",
        chips=["Vite", "Webpack", "Plugin"],
    ),
    "study-mode": dict(
        name="study-mode",
        desc_attr="浏览器扩展：把摸鱼的标签页变成专注的学习空间。",
        desc1="浏览器扩展：把摸鱼的标签页，",
        desc2="变成安静专注的学习空间。Manifest V3。",
        chips=["扩展", "MV3", "TypeScript"],
    ),
    "my-personal-site": dict(
        name="my-personal-site",
        desc_attr="个人博客与作品集，React 19 + Supabase，部署于 Vercel Edge。",
        desc1="个人博客与作品集，52 篇精选长文。",
        desc2="React 19 · Supabase · Vercel Edge。",
        chips=["React 19", "Supabase", "PWA"],
    ),
}

if __name__ == "__main__":
    for key, spec in P.items():
        merged_en = spec
        merged_zh = {**spec, **ZH[key]}
        # zh uses same visual identity; swap copy
        for lang, merged in (("en", merged_en), ("zh", merged_zh)):
            chips = build_chips(merged["chips"][:3])
            icon = (
                f'<g class="icon" transform="{merged["icon_transform"]}">{merged["icon"]}</g>'
            )
            svg = SVG_TMPL.format(
                font_stack=FONT_STACK,
                name=xml_escape(merged["name"]),
                desc_attr=xml_escape(merged["desc_attr"]),
                desc1=xml_escape(merged["desc1"]),
                desc2=xml_escape(merged["desc2"]),
                icon=icon,
                arrow=ARROW_ICON.format(x=414, y=32),
                chips=chips,
                **merged["colors"],
            )
            path = os.path.join(OUT, f"{key}-{lang}.svg")
            with open(path, "w") as f:
                f.write(svg)
            print("wrote", path)
