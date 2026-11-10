#!/usr/bin/env python3
"""Generate project cards v5 for the GitHub profile README (en/zh).

v5 geometry (all elements strictly inside the 460x110 canvas):
- icon tile 48x48 at (16,21); icon 24x24 centered exactly on tile center
- name baseline y=40, desc single line baseline y=62
- chips y=76 h=19 -> bottom 95 (15px bottom margin, nothing clipped)
- right arrow vertically centered at x=420
- per-project accent colors kept from the legacy design
"""

import os
from xml.sax.saxutils import escape as xml_escape

OUT = "/Users/zzihan/Desktop/Crucio/z-Zihan/assets/cards"
os.makedirs(OUT, exist_ok=True)

FONT_STACK = "-apple-system, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif"

W, H = 460, 110
TILE = dict(x=16, y=21, s=48, rx=12)
ICON_T = (TILE["x"] + TILE["s"] / 2 - 12, TILE["y"] + TILE["s"] / 2 - 12)  # center 24px icon
NAME_Y = 40
DESC_Y = 62
CHIP_Y, CHIP_H, CHIP_FONT = 76, 19, 9.5
TEXT_X = 84
ARROW_T = (420, 41)

SVG_TMPL = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">\n'
    '  <title id="title">{name}</title>\n'
    '  <desc id="desc">{desc_attr}</desc>\n'
    '  <defs>\n'
    '    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">\n'
    '      <stop class="bg-a" offset="0"/>\n'
    '      <stop class="bg-b" offset="1"/>\n'
    '    </linearGradient>\n'
    '    <linearGradient id="tileGrad" x1="0" y1="0" x2="1" y2="1">\n'
    '      <stop class="tile-a" offset="0"/>\n'
    '      <stop class="tile-b" offset="1"/>\n'
    '    </linearGradient>\n'
    '    <linearGradient id="iconGrad" x1="0" y1="0" x2="1" y2="1">\n'
    '      <stop class="ic-a" offset="0"/>\n'
    '      <stop class="ic-b" offset="1"/>\n'
    '    </linearGradient>\n'
    '    <filter id="blobBlur" x="-60%" y="-60%" width="220%" height="220%">\n'
    '      <feGaussianBlur stdDeviation="16"/>\n'
    '    </filter>\n'
    '    <style>\n'
    '      .bg-a {{ stop-color: #f8fafc; }}\n'
    '      .bg-b {{ stop-color: #eef2f8; }}\n'
    '      .tile-a {{ stop-color: {tile_a}; }}\n'
    '      .tile-b {{ stop-color: {tile_b}; }}\n'
    '      .ic-a {{ stop-color: {ic_a}; }}\n'
    '      .ic-b {{ stop-color: {ic_b}; }}\n'
    '      .card {{ fill: url(#cardGrad); stroke: #d9e1ec; }}\n'
    '      .blob {{ fill: url(#iconGrad); opacity: 0.07; }}\n'
    '      .tile {{ fill: url(#tileGrad); }}\n'
    '      .icon {{ fill: none; stroke: url(#iconGrad); stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }}\n'
    '      .ext-link {{ fill: none; stroke: {ic_b}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; opacity: 0.6; }}\n'
    '      .name {{ fill: #0f172a; font: 700 17px ' + FONT_STACK + '; }}\n'
    '      .desc {{ fill: #57606a; font: 400 12.5px ' + FONT_STACK + '; }}\n'
    '      .chip-bg {{ fill: {chip_bg}; }}\n'
    '      .chip-text {{ fill: {ic_a}; font: 600 {CHIP_FONT}px ' + FONT_STACK + '; }}\n'
    '      @media (prefers-color-scheme: dark) {{\n'
    '        .bg-a {{ stop-color: #161b22; }}\n'
    '        .bg-b {{ stop-color: #1a2029; }}\n'
    '        .tile-a {{ stop-color: {tile_a_dark}; }}\n'
    '        .tile-b {{ stop-color: {tile_b_dark}; }}\n'
    '        .ic-a {{ stop-color: {ic_b}; }}\n'
    '        .ic-b {{ stop-color: {ic_b_dark}; }}\n'
    '        .card {{ stroke: #30363d; }}\n'
    '        .blob {{ opacity: 0.10; }}\n'
    '        .ext-link {{ stroke: {ic_b_dark}; opacity: 0.65; }}\n'
    '        .name {{ fill: #e6edf3; }}\n'
    '        .desc {{ fill: #8b949e; }}\n'
    '        .chip-bg {{ fill: {chip_bg_dark}; }}\n'
    '        .chip-text {{ fill: {ic_b_dark}; }}\n'
    '      }}\n'
    '    </style>\n'
    '  </defs>\n'
    '  <rect class="card" x="1" y="1" width="{Wm2}" height="{Hm2}" rx="16"/>\n'
    '  <circle class="blob" cx="410" cy="96" r="40" filter="url(#blobBlur)"/>\n'
    '  <rect class="tile" x="{tile_x}" y="{tile_y}" width="{tile_s}" height="{tile_s}" rx="{tile_rx}"/>\n'
    '  <g class="icon" transform="translate({icon_tx},{icon_ty})">{icon}</g>\n'
    '  <g class="ext-link" transform="translate({arrow_tx},{arrow_ty})"><path d="M5 11L11 5M5.8 5H11v5.2"/></g>\n'
    '  <text class="name" x="{TEXT_X}" y="{NAME_Y}">{name}</text>\n'
    '  <text class="desc" x="{TEXT_X}" y="{DESC_Y}">{desc}</text>\n'
    '{chips}\n'
    '</svg>'
)

CHIP_TMPL = ('  <rect class="chip-bg" x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="9.5"/>\n'
             '  <text class="chip-text" x="{tx:.1f}" y="{ty}">{label}</text>')


def chip_w(label: str) -> float:
    return sum(9.5 if ord(c) > 0x2E7F else 5.8 for c in label) + 14


def build_chips(labels):
    parts, x = [], float(TEXT_X)
    for label in labels:
        w = chip_w(label)
        parts.append(CHIP_TMPL.format(x=x, y=CHIP_Y, w=w, h=CHIP_H, tx=x + 7, ty=CHIP_Y + 14, label=xml_escape(label)))
        x += w + 7
    return "\n".join(parts)


C = dict  # shorthand

P = {
    "evir": dict(
        colors=C(tile_a="#e3f8f2", tile_b="#c7f1e4", ic_a="#0d9488", ic_b="#2dd4bf",
                 ic_b_dark="#5eead4", tile_a_dark="#16302c", tile_b_dark="#163c36",
                 chip_bg="#e3f8f2", chip_bg_dark="#16302c"),
        icon='<rect x="3.2" y="5" width="17.6" height="14" rx="3"/><path d="M7 10.4l2.6 2.1-2.6 2.1"/><path d="M12.6 14.5h4.2"/>',
    ),
    "chorus": dict(
        colors=C(tile_a="#efe7fd", tile_b="#ddccfa", ic_a="#7c3aed", ic_b="#a78bfa",
                 ic_b_dark="#d8b4fe", tile_a_dark="#241f38", tile_b_dark="#2f2748",
                 chip_bg="#f0e9fe", chip_bg_dark="#241f38"),
        icon='<circle cx="12" cy="4.8" r="2.3"/><circle cx="4.7" cy="18.1" r="2.3"/><circle cx="19.3" cy="18.1" r="2.3"/><path d="M10.5 6.7L6.2 16.1M13.5 6.7l4.3 9.4M6.9 18.1h10.2"/>',
    ),
    "awesome-skills": dict(
        colors=C(tile_a="#fce7f3", tile_b="#fbcfe8", ic_a="#db2777", ic_b="#f472b6",
                 ic_b_dark="#f9a8d4", tile_a_dark="#36192b", tile_b_dark="#3f1e33",
                 chip_bg="#fce7f3", chip_bg_dark="#36192b"),
        icon='<path d="M13.2 2.6L5.6 13.4h5.2l-1 8 8.4-11.2h-5.6z"/>',
    ),
    "llm-101": dict(
        colors=C(tile_a="#dbeafe", tile_b="#bfdbfe", ic_a="#2563eb", ic_b="#60a5fa",
                 ic_b_dark="#93c5fd", tile_a_dark="#1c2a44", tile_b_dark="#1e3352",
                 chip_bg="#dbeafe", chip_bg_dark="#1c2a44"),
        icon='<circle cx="12" cy="12" r="2.3"/><circle cx="5" cy="5.3" r="1.7"/><circle cx="19" cy="5.3" r="1.7"/><circle cx="5" cy="18.7" r="1.7"/><circle cx="19" cy="18.7" r="1.7"/><path d="M9.9 10.1L6.3 6.7M14.1 10.1l3.6-3.4M9.9 13.9l-3.6 3.4M14.1 13.9l3.6 3.4"/>',
    ),
    "build-meta-injector": dict(
        colors=C(tile_a="#fef3c7", tile_b="#fde68a", ic_a="#d97706", ic_b="#fbbf24",
                 ic_b_dark="#fcd34d", tile_a_dark="#33240e", tile_b_dark="#3d2b10",
                 chip_bg="#fef3c7", chip_bg_dark="#33240e"),
        icon='<path d="M12 3.2l7.6 4.3v8.6L12 20.4l-7.6-4.3V7.5z"/><path d="M12 11.8V3.2M12 11.8l7.6-4.3M12 11.8l-7.6-4.3"/>',
    ),
    "my-personal-site": dict(
        colors=C(tile_a="#e0e7ff", tile_b="#c7d2fe", ic_a="#4f46e5", ic_b="#818cf8",
                 ic_b_dark="#a5b4fc", tile_a_dark="#1e2142", tile_b_dark="#232850",
                 chip_bg="#e0e7ff", chip_bg_dark="#1e2142"),
        icon='<path d="M12 3.2l8 3.6v5.4c0 4.9-3.4 8.1-8 9.6-4.6-1.5-8-4.7-8-9.6V6.8z"/><path d="M8.6 11.6l2.3 2.3 4.5-4.5"/>',
    ),
    "study-mode": dict(
        colors=C(tile_a="#e0f2fe", tile_b="#bae6fd", ic_a="#0284c7", ic_b="#38bdf8",
                 ic_b_dark="#7dd3fc", tile_a_dark="#12283a", tile_b_dark="#153349",
                 chip_bg="#e0f2fe", chip_bg_dark="#12283a"),
        icon='<rect x="3.5" y="5" width="17" height="12.5" rx="2.4"/><path d="M3.5 8.8h17"/><path d="M6.4 6.9h.01M9 6.9h.01M11.6 6.9h.01"/><path d="M9.4 21h5.2M12 17.5V21"/>',
    ),
}

COPY = {
    "en": {
        "evir": ("Evir", "Local-first desktop agent on your own models.",
                 ["TypeScript", "React", "Tauri"]),
        "chorus": ("Chorus", "Agent workspace across CLIs, devices, and teams.",
                   ["TypeScript", "agents", "local-first"]),
        "awesome-skills": ("awesome-skills", "Curated agent skills — auto-published to ClawHub.",
                           ["OpenClaw", "skills", "CI/CD"]),
        "llm-101": ("LLM-101", "Zero-to-one AI knowledge map: LLM, RAG, Agent, MCP.",
                    ["AI", "course", "open source"]),
        "build-meta-injector": ("build-meta-injector", "Inject build/version/Git metadata into HTML.",
                                ["Vite", "Webpack", "plugin"]),
        "my-personal-site": ("my-personal-site", "Personal blog & portfolio, 52 deep-dives.",
                             ["React 19", "Supabase", "PWA"]),
        "study-mode": ("study-mode", "Browser extension for calm, focused study time.",
                       ["Extension", "MV3", "TypeScript"]),
    },
    "zh": {
        "evir": ("Evir", "由你自己的模型驱动的本地优先桌面 AI Agent。",
                 ["TypeScript", "React", "Tauri"]),
        "chorus": ("Chorus", "AI Agent 的本地优先协作工作区，跨 CLI 与设备。",
                   ["TypeScript", "Agent", "本地优先"]),
        "awesome-skills": ("awesome-skills", "开发技能与工程实践精选，CI 自动发布到 ClawHub。",
                           ["OpenClaw", "skills", "CI/CD"]),
        "llm-101": ("LLM-101", "从 0 开始的 AI 知识地图：LLM → RAG → Agent → MCP。",
                    ["AI", "课程", "开源"]),
        "build-meta-injector": ("build-meta-injector", "把构建时间、版本与 Git 元数据注入 HTML。",
                                ["Vite", "Webpack", "插件"]),
        "my-personal-site": ("my-personal-site", "个人博客与作品集，52 篇精选长文。",
                             ["React 19", "Supabase", "PWA"]),
        "study-mode": ("study-mode", "浏览器扩展：把摸鱼标签页变成专注学习空间。",
                       ["扩展", "MV3", "TypeScript"]),
    },
}


def main():
    for key, spec in P.items():
        for lang in ("en", "zh"):
            name, desc, chips = COPY[lang][key]
            svg = SVG_TMPL.format(
                W=W, H=H, Wm2=W-2, Hm2=H-2,
                tile_x=TILE["x"], tile_y=TILE["y"], tile_s=TILE["s"], tile_rx=TILE["rx"],
                icon_tx=ICON_T[0], icon_ty=ICON_T[1],
                arrow_tx=ARROW_T[0], arrow_ty=ARROW_T[1],
                TEXT_X=TEXT_X, NAME_Y=NAME_Y, DESC_Y=DESC_Y, CHIP_FONT=CHIP_FONT,
                name=xml_escape(name),
                desc_attr=xml_escape(desc),
                desc=xml_escape(desc),
                icon=spec["icon"],
                chips=build_chips(chips),
                **spec["colors"],
            )
            path = os.path.join(OUT, f"{key}-{lang}.svg")
            with open(path, "w") as f:
                f.write(svg)
            print("wrote", path)


if __name__ == "__main__":
    main()
