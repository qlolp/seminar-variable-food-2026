# -*- coding: utf-8 -*-
"""Экспорт .pptd/.page слайдов в PDF 16:9 через WeasyPrint."""
from __future__ import annotations

import html as htmlmod
import re
from pathlib import Path

import yaml

ROOT = Path("/Users/evgenii/Documents/презентация вариативное меню")
DECK = ROOT / "02_презентация" / "презентация_34_слайда"
OUT_HTML = ROOT / "проект" / "output" / "_slides.html"
OUT_PDF = ROOT / "02_презентация" / "Презентация_Не_просто_накормить.pdf"
FONTS = ROOT / "проект" / "output" / "fonts"

THEME = {
    "primary": "#B85C3D",
    "accent": "#D97757",
    "text": "#141413",
    "muted": "#8A8578",
    "bg": "#F7F5F0",
    "soft": "#EFEBE3",
    "softgreen": "#EFEBE3",
    "line": "#E5E2D8",
    "ink": "#1C1B19",
}
STYLES = {
    "kicker": "font-size:11px;color:#B85C3D;font-family:'Noto Sans',sans-serif;letter-spacing:2px;font-weight:700;",
    "h1": "font-size:28px;font-weight:700;color:#141413;font-family:'PT Serif',serif;line-height:1.15;",
    "body": "font-size:15px;color:#141413;font-family:'Noto Sans',sans-serif;line-height:1.4;",
    "small": "font-size:11px;color:#8A8578;font-family:'Noto Sans',sans-serif;line-height:1.3;",
    "big": "font-size:44px;font-weight:700;color:#B85C3D;font-family:'PT Serif',serif;",
    "q": "font-size:30px;font-weight:700;color:#B85C3D;font-family:'PT Serif',serif;line-height:1.25;",
}


def col(v):
    if not isinstance(v, str):
        return v or "#141413"
    if v.startswith("$"):
        return THEME.get(v[1:], "#141413")
    return v


def esc(s):
    return htmlmod.escape(str(s), quote=True)


def text_css(content, theme_styles):
    if not content:
        return STYLES["body"]
    if content.get("style"):
        key = str(content["style"]).lstrip("$")
        base = theme_styles.get(key, STYLES.get(key, STYLES["body"]))
    else:
        parts = ["font-family:'Noto Sans',sans-serif", "color:#141413"]
        if content.get("fontSize"):
            parts.append(f"font-size:{content['fontSize']}px")
        if content.get("fontFamily"):
            fam = content["fontFamily"]
            if "Serif" in fam or fam == "PT Serif":
                parts.append("font-family:'PT Serif',serif")
            else:
                parts.append("font-family:'Noto Sans',sans-serif")
        if content.get("color"):
            parts.append(f"color:{col(content['color'])}")
        if content.get("bold"):
            parts.append("font-weight:700")
        if content.get("letterSpacing"):
            parts.append(f"letter-spacing:{content['letterSpacing']}px")
        if content.get("lineHeight"):
            parts.append(f"line-height:{content['lineHeight']}")
        align = content.get("align")
        if align:
            a = align if isinstance(align, list) else [align]
            horiz = a[0] if a else "left"
            vert = a[1] if len(a) > 1 else "top"
            if vert in ("middle", "center") or horiz == "center":
                parts.append("display:flex")
                parts.append(
                    "justify-content:"
                    + ("center" if horiz == "center" else "flex-end" if horiz == "right" else "flex-start")
                )
                parts.append("align-items:" + ("center" if vert in ("middle", "center") else "flex-start"))
                if horiz == "center":
                    parts.append("text-align:center")
            elif horiz == "right":
                parts.append("text-align:right")
            elif horiz == "center":
                parts.append("text-align:center")
        base = ";".join(parts) + ";"
    return base


def render_text(el):
    b = el["bounds"]
    c = el.get("content") or {}
    raw = c.get("text") or ""
    css = text_css(c, STYLES)
    if any(tag in raw for tag in ("<p", "<strong", "<span", "<br", "<em", "<b>")):
        inner = raw.replace("<br>", "<br/>")
        inner = re.sub(r"\$([a-z]+)", lambda m: THEME.get(m.group(1), m.group(0)), inner)
    else:
        inner = esc(raw).replace("\n", "<br/>")
    return (
        f'<div class="el" style="left:{b[0]}px;top:{b[1]}px;width:{b[2]}px;height:{b[3]}px;{css}">{inner}</div>'
    )


def render_shape(el):
    b = el["bounds"]
    fill = (el.get("fill") or {}).get("color")
    border = el.get("border") or {}
    name = el.get("shapeName") or "rect"
    radius = el.get("cornerRadius")
    parts = [
        f"left:{b[0]}px",
        f"top:{b[1]}px",
        f"width:{b[2]}px",
        f"height:{b[3]}px",
        "box-sizing:border-box",
    ]
    if fill:
        parts.append(f"background:{col(fill)}")
    else:
        parts.append("background:transparent")
    if name in ("ellipse", "oval", "circle"):
        parts.append("border-radius:50%")
    elif radius:
        parts.append(f"border-radius:{radius}px")
    if border:
        bw = border.get("width") or 1
        bc = col(border.get("color") or THEME["muted"])
        style = str(border.get("style") or "solid")
        if style in ("dash", "dashed"):
            parts.append(f"border:{bw}px dashed {bc}")
        else:
            parts.append(f"border:{bw}px solid {bc}")
    return f'<div class="el shape" style="{";".join(parts)};"></div>'


def render_line(el):
    b = el["bounds"]
    border = el.get("border") or {}
    c = col(border.get("color") or THEME["muted"])
    w = border.get("width") or 2
    points = el.get("points")
    arrows = el.get("arrow") or [None, None]
    mid = f"m{int(b[0])}-{int(b[1])}-{int(b[2])}-{int(b[3])}"
    if points:
        vb = el.get("viewBox") or [b[2], b[3]]
        marker_defs = (
            f'<defs><marker id="{mid}" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker></defs>'
        )
        start = f' marker-start="url(#{mid})"' if arrows[0] == "arrow" else ""
        end = f' marker-end="url(#{mid})"' if arrows[1] == "arrow" else ""
        return (
            f'<div class="el line" style="left:{b[0]}px;top:{b[1]}px;width:{b[2]}px;height:{b[3]}px;overflow:visible;">'
            f'<svg width="{b[2]}" height="{b[3]}" viewBox="0 0 {vb[0]} {vb[1]}" overflow="visible">'
            f"{marker_defs}"
            f'<polyline points="{esc(points)}" fill="none" stroke="{c}" stroke-width="{w}" '
            f'stroke-linecap="round"{start}{end}/></svg></div>'
        )
    return (
        f'<div class="el" style="left:{b[0]}px;top:{b[1] + b[3] // 2}px;width:{b[2]}px;height:{w}px;'
        f'background:{c};"></div>'
    )


def render_table(el):
    b = el["bounds"]
    rows = el.get("rows") or []
    html = [
        f'<div class="el" style="left:{b[0]}px;top:{b[1]}px;width:{b[2]}px;height:{b[3]}px;">',
        '<table class="sl-t">',
    ]
    for i, row in enumerate(rows):
        html.append("<tr>")
        for cell in row:
            tag = "th" if i == 0 else "td"
            html.append(f"<{tag}>{esc(cell.get('text', ''))}</{tag}>")
        html.append("</tr>")
    html.append("</table></div>")
    return "".join(html)


def render_chart(el):
    b = el["bounds"]
    data = el.get("data") or {}
    rows = data.get("rows") or []
    series = (el.get("series") or [{}])[0]
    fill = col(series.get("fill") or THEME["accent"])
    ymax = (el.get("yAxis") or {}).get("max") or 100
    parsed = []
    for row in rows:
        name = row[0]
        val = row[1] if len(row) > 1 else 0
        try:
            num = float(val)
        except (TypeError, ValueError):
            num = 0
        parsed.append((name, val, num))
    data_max = max((n for _, _, n in parsed), default=1) or 1
    scale = float(ymax)
    if data_max < scale * 0.25:
        scale = data_max * 1.3
    bars = []
    for name, val, num in parsed:
        pct = max(2, min(100, num / scale * 100))
        bars.append(
            f'<div class="bar-row"><div class="bar-lab">{esc(name)}</div>'
            f'<div class="bar-track"><div class="bar" style="width:{pct}%;background:{fill}"></div></div>'
            f'<div class="bar-val">{val}</div></div>'
        )
    title = series.get("name") or ""
    return (
        f'<div class="el chart" style="left:{b[0]}px;top:{b[1]}px;width:{b[2]}px;height:{b[3]}px;">'
        f'<div class="chart-title">{esc(title)}</div>{"".join(bars)}</div>'
    )


RENDER = {
    "text": render_text,
    "shape": render_shape,
    "line": render_line,
    "table": render_table,
    "chart": render_chart,
}


def render_page(path: Path) -> str:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    bg = col(((data.get("background") or {}).get("color")) or THEME["bg"])
    bits = []
    for el in data.get("elements") or []:
        fn = RENDER.get(el.get("elementType"))
        if fn:
            bits.append(fn(el))
    return f'<section class="slide" style="background:{bg}">{"".join(bits)}</section>'


def main():
    deck = yaml.safe_load((DECK / "03_презентация.pptd").read_text(encoding="utf-8"))
    pages = deck["pages"]
    slides = []
    for rel in pages:
        slides.append(render_page(DECK / rel))
    css = f"""
@font-face {{ font-family:'PT Serif'; src:url('{FONTS.as_uri()}/PTSerif-Regular.ttf'); }}
@font-face {{ font-family:'PT Serif'; src:url('{FONTS.as_uri()}/PTSerif-Bold.ttf'); font-weight:700; }}
@font-face {{ font-family:'Noto Sans'; src:url('{FONTS.as_uri()}/NotoSans-variable.ttf'); font-weight:100 900; }}
@page {{ size: 960px 540px; margin: 0; }}
html, body {{ margin:0; padding:0; }}
.slide {{ width:960px; height:540px; position:relative; overflow:hidden; page-break-after:always; }}
.slide:last-child {{ page-break-after:auto; }}
.el {{ position:absolute; overflow:hidden; box-sizing:border-box; }}
.el.line {{ overflow:visible; }}
.el p {{ margin:0 0 0.3em; }}
.el p:last-child {{ margin-bottom:0; }}
.sl-t {{ width:100%; height:100%; border-collapse:collapse; font-family:'Noto Sans',sans-serif; font-size:14px; }}
.sl-t th, .sl-t td {{ border-bottom:1px solid {THEME['line']}; padding:8px 10px; text-align:left; vertical-align:middle; }}
.sl-t th {{ color:{THEME['primary']}; font-weight:700; }}
.chart {{ font-family:'Noto Sans',sans-serif; }}
.chart-title {{ font-size:12px; color:{THEME['muted']}; margin-bottom:10px; }}
.bar-row {{ display:flex; align-items:center; margin:10px 0; }}
.bar-lab {{ width:160px; text-align:right; padding-right:10px; font-size:13px; }}
.bar-track {{ flex:1; height:22px; background:{THEME['soft']}; border-radius:4px; overflow:hidden; }}
.bar {{ height:22px; border-radius:4px; }}
.bar-val {{ width:50px; padding-left:8px; font-weight:700; font-size:13px; }}
"""
    doc = (
        "<!DOCTYPE html><html lang='ru'><head><meta charset='utf-8'>"
        "<title>Не просто накормить — презентация</title><style>"
        + css
        + "</style></head><body>"
        + "".join(slides)
        + "</body></html>"
    )
    OUT_HTML.write_text(doc, encoding="utf-8")
    print(f"slides HTML: {len(pages)} pages → {OUT_HTML}")
    import os
    import subprocess

    env = dict(os.environ)
    env["LANG"] = "C.UTF-8"
    r = subprocess.run(["weasyprint", str(OUT_HTML), str(OUT_PDF)], env=env, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        raise SystemExit(1)
    from pypdf import PdfReader

    print(f"PDF {OUT_PDF}  {len(PdfReader(str(OUT_PDF)).pages)} стр.")


if __name__ == "__main__":
    main()
