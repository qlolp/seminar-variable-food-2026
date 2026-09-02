#!/usr/bin/env python3
"""Lint LLM-wiki: каркас, frontmatter, wikilinks. Не список печатных файлов."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "LICENSE",
    "AGENTS.md",
    "CLAUDE.md",
    "HOW_TO_ADD.md",
    "wiki/index.md",
    "wiki/log.md",
    "wiki/overview.md",
    "wiki/gaps.md",
    "raw/sources/ne-prosto-nakormit/README.md",
    "raw/sources/related/README.md",
    "raw/sources/ne-prosto-nakormit/doklad/Не_просто_накормить_доклад.md",
    "raw/sources/ne-prosto-nakormit/doklad/Не_просто_накормить_доклад_редакция.pdf",
]

FORBIDDEN = [
    "НАЧНИТЕ_ЗДЕСЬ.md",
    "ПРОЧТИ_МЕНЯ.md",
    "CHANGELOG.md",
    "requirements.txt",
    "семинар_пакет_2026.zip",
    "проект",
    "07_редакция_доклада_v2",
    "выступление_26.08",
    "пакет_26.08",
    ".cursor",
    "raw/sources/ne-prosto-nakormit/viktorina",
    "raw/sources/ne-prosto-nakormit/listovki",
    "raw/sources/ne-prosto-nakormit/prezentaciya",
    "raw/sources/ne-prosto-nakormit/doklad/Не_просто_накормить_доклад_стиль_claude.pdf",
    "raw/sources/ne-prosto-nakormit/doklad/Не_просто_накормить_КРАТКАЯ_версия.pdf",
    "raw/sources/ne-prosto-nakormit/seminar-paket/21_если_инспектор_не_принял.pdf",
    "raw/sources/ne-prosto-nakormit/seminar-paket/Калькулятор_стоимости_вариативности.xlsx",
    "raw/sources/ne-prosto-nakormit/seminar-paket/Вариативное_питание_опыт_реализации.pdf",
    "raw/sources/ne-prosto-nakormit/seminar-paket/Памятка_что_унести_в_регион.pdf",
]

ALLOWED_TYPES = {
    "concept",
    "entity",
    "source",
    "synthesis",
    "index",
    "log",
    "gap",
    "query",
}
ALLOWED_CONF = {"high", "medium", "low"}
PRINT_SUFFIXES = {".pdf", ".pptx", ".xlsx", ".xls"}
KITCHEN_SNIPPETS = ("проект/chapters/",)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]+`")
WIKI_RE = re.compile(r"\[\[wiki/([^\]]+)\]\]")
FM_RE = re.compile(r"^---\n(.*?)\n---", re.S)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_frontmatter(text: str) -> dict | None:
    match = FM_RE.match(text)
    if not match:
        return None
    data: dict = {}
    current_list_key: str | None = None
    for line in match.group(1).splitlines():
        if current_list_key and re.match(r"^-\s+", line):
            data[current_list_key].append(line.split("-", 1)[1].strip().strip("\"'"))
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, _, raw_val = line.partition(":")
        key = key.strip()
        val = raw_val.strip()
        if val == "":
            data[key] = []
            current_list_key = key
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = (
                []
                if not inner
                else [item.strip().strip("\"'") for item in inner.split(",")]
            )
        else:
            data[key] = val.strip("\"'")
    return data


def wiki_pages() -> set[str]:
    pages = set()
    for path in (ROOT / "wiki").rglob("*.md"):
        rel = path.relative_to(ROOT / "wiki").as_posix()
        if rel.endswith(".md"):
            pages.add(rel[:-3])
    return pages


def catalog_markdown() -> list[Path]:
    files = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CLAUDE.md",
        ROOT / "HOW_TO_ADD.md",
    ]
    files.extend(sorted((ROOT / "wiki").rglob("*.md")))
    files.extend(sorted((ROOT / "raw").rglob("README.md")))
    seen: set[Path] = set()
    out: list[Path] = []
    for path in files:
        if path.is_file() and path not in seen:
            seen.add(path)
            out.append(path)
    return out


def local_targets(raw: str) -> list[str]:
    target = raw.strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return []
    target = target.split()[0]
    target = target.split("#", 1)[0]
    return [target] if target else []


def skip_frontmatter(path: Path) -> bool:
    return path.name == "README.md" or path.parent == ROOT / "wiki" / "queries"


def collect_broken_links(path: Path, text: str) -> list[str]:
    broken: list[str] = []
    stripped = INLINE_CODE_RE.sub("", CODE_FENCE_RE.sub("", text))
    for match in LINK_RE.finditer(stripped):
        for target in local_targets(match.group(1)):
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                broken.append(f"{path.relative_to(ROOT)} → {target} (вне репозитория)")
                continue
            if not resolved.exists():
                broken.append(f"{path.relative_to(ROOT)} → {target}")
    return broken


def check_frontmatter(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT).as_posix()
    data = parse_frontmatter(text)
    if data is None:
        return [f"Нет frontmatter: {rel}"]
    for key in ("title", "type", "tags", "sources", "updated", "confidence"):
        if key not in data:
            errors.append(f"{rel}: нет поля frontmatter `{key}`")
    kind = data.get("type")
    if kind and kind not in ALLOWED_TYPES:
        errors.append(f"{rel}: type `{kind}` не из списка {sorted(ALLOWED_TYPES)}")
    conf = data.get("confidence")
    if conf and conf not in ALLOWED_CONF:
        errors.append(f"{rel}: confidence `{conf}` не high|medium|low")
    updated = data.get("updated")
    if updated and not DATE_RE.match(str(updated)):
        errors.append(f"{rel}: updated `{updated}` не ISO-дата")
    tags = data.get("tags")
    if tags is not None and not isinstance(tags, list):
        errors.append(f"{rel}: tags должен быть списком")
    sources = data.get("sources", [])
    if sources is not None and not isinstance(sources, list):
        errors.append(f"{rel}: sources должен быть списком")
        return errors
    for src in sources or []:
        src_path = ROOT / src
        if not src_path.exists():
            errors.append(f"{rel}: sources → нет файла `{src}`")
    return errors


def check_print_theater() -> list[str]:
    errors: list[str] = []
    paket = ROOT / "raw/sources/ne-prosto-nakormit/seminar-paket"
    if paket.is_dir():
        md = list(paket.glob("*.md"))
        if len(md) < 16:
            errors.append(
                f"seminar-paket: ожидались markdown-бланки (нашлось {len(md)} .md)"
            )
        leftover = [
            p.relative_to(ROOT).as_posix()
            for p in paket.iterdir()
            if p.is_file() and p.suffix.lower() in PRINT_SUFFIXES
        ]
        if leftover:
            errors.append(
                "Печать в seminar-paket (нужен markdown, не бинарник):\n"
                + "\n".join(f"  {p}" for p in leftover)
            )
    doklad = ROOT / "raw/sources/ne-prosto-nakormit/doklad"
    pdfs = sorted(
        p.name for p in doklad.glob("*.pdf")
    ) if doklad.is_dir() else []
    allowed = {"Не_просто_накормить_доклад_редакция.pdf"}
    extra = [name for name in pdfs if name not in allowed]
    if extra:
        errors.append("Лишние PDF в doklad/:\n" + "\n".join(f"  {p}" for p in extra))
    return errors


def main() -> int:
    errors: list[str] = []

    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    leftover = [p for p in FORBIDDEN if (ROOT / p).exists()]
    if missing:
        errors.append("Нет обязательных файлов wiki:\n" + "\n".join(f"  {p}" for p in missing))
    if leftover:
        errors.append(
            "Вернулась кухня или печатная раздатка:\n"
            + "\n".join(f"  {p}" for p in leftover)
        )

    numbered = [p.name for p in ROOT.iterdir() if p.is_dir() and p.name[:1].isdigit()]
    if numbered:
        errors.append("Нумерованные каталоги должны жить в raw/: " + ", ".join(numbered))

    errors.extend(check_print_theater())

    kitchen: list[str] = []
    broken: list[str] = []
    for path in catalog_markdown():
        text = path.read_text(encoding="utf-8")
        for snippet in KITCHEN_SNIPPETS:
            if snippet in text:
                kitchen.append(f"{path.relative_to(ROOT)}: `{snippet}`")
        broken.extend(collect_broken_links(path, text))
        rel = path.relative_to(ROOT)
        if path.is_relative_to(ROOT / "wiki") and not skip_frontmatter(path):
            errors.extend(check_frontmatter(path, text))
    if kitchen:
        errors.append("Кухонные пути в текстах:\n" + "\n".join(f"  {p}" for p in kitchen))
    if broken:
        errors.append("Битые ссылки:\n" + "\n".join(f"  {p}" for p in broken))

    pages = wiki_pages()
    dangling_wiki: list[str] = []
    for path in (ROOT / "wiki").rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for slug in WIKI_RE.findall(text):
            slug = slug.strip()
            if slug not in pages:
                dangling_wiki.append(f"{path.relative_to(ROOT)} → [[wiki/{slug}]]")
    if dangling_wiki:
        errors.append("Битые wikilinks:\n" + "\n".join(f"  {p}" for p in dangling_wiki))

    index = (ROOT / "wiki/index.md").read_text(encoding="utf-8")
    catalogued = set(WIKI_RE.findall(index))
    content_pages = {
        p
        for p in pages
        if p not in {"index", "log", "queries/README"} and not p.startswith("queries/")
    }
    for must in ("overview", "gaps"):
        if must not in catalogued:
            errors.append(f"wiki/index.md не содержит [[wiki/{must}]]")
    unlisted = sorted(
        p
        for p in content_pages
        if p not in catalogued and p not in {"overview", "gaps"}
    )
    if unlisted:
        errors.append("Страницы wiki нет в index.md:\n" + "\n".join(f"  {p}" for p in unlisted))

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "wiki/index.md" not in agents:
        errors.append("AGENTS.md должен указывать на wiki/index.md")

    if errors:
        print("\n\n".join(errors))
        return 1
    wiki_count = len(list((ROOT / "wiki").rglob("*.md")))
    print(
        f"OK: wiki-каркас на месте, {wiki_count} wiki md, "
        "frontmatter и wikilinks живые, печатная раздатка не требуется."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
