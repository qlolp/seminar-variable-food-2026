#!/usr/bin/env python3
"""Проверка LLM-wiki: каркас, сырьё, ссылки. raw/ не переписывается."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw/sources/ne-prosto-nakormit"

REQUIRED = [
    "README.md",
    "LICENSE",
    "AGENTS.md",
    "CLAUDE.md",
    "wiki/index.md",
    "wiki/log.md",
    "wiki/overview.md",
    "wiki/gaps.md",
    "raw/sources/ne-prosto-nakormit/README.md",
    "raw/sources/related/README.md",
    "raw/sources/ne-prosto-nakormit/doklad/Не_просто_накормить_доклад.md",
    "raw/sources/ne-prosto-nakormit/doklad/Не_просто_накормить_доклад_редакция.pdf",
    "raw/sources/ne-prosto-nakormit/doklad/Не_просто_накормить_доклад_стиль_claude.pdf",
    "raw/sources/ne-prosto-nakormit/doklad/Не_просто_накормить_КРАТКАЯ_версия.pdf",
    "raw/sources/ne-prosto-nakormit/prezentaciya/Презентация_v6_Не_просто_накормить.pdf",
    "raw/sources/ne-prosto-nakormit/prezentaciya/Презентация_v6_Не_просто_накормить.pptx",
    "raw/sources/ne-prosto-nakormit/seminar-paket/README.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/Памятка_что_унести_в_регион.pdf",
    "raw/sources/ne-prosto-nakormit/seminar-paket/Вариативное_питание_опыт_реализации.pdf",
    "raw/sources/ne-prosto-nakormit/seminar-paket/21_если_инспектор_не_принял.pdf",
    "raw/sources/ne-prosto-nakormit/seminar-paket/21_если_инспектор_не_принял.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/Калькулятор_стоимости_вариативности.xlsx",
    "raw/sources/ne-prosto-nakormit/seminar-paket/04_записка_руководителю.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/05_чеклист_понедельник.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/06_10_ошибок.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/07_10_вопросов_учредителю.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/08_раздатка.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/09_сценарий_малых_групп.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/10_пять_вопросов_залу.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/11_экспресс_аудит_10мин.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/12_форма_ступени.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/13_трудные_вопросы.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/14_возражения.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/15_решения_без_средств.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/16_решения_с_финансированием.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/17_решения_с_учредителем.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/18_решения_не_без_врача.md",
    "raw/sources/ne-prosto-nakormit/seminar-paket/19_юридическое_заключение.md",
    "raw/sources/ne-prosto-nakormit/listovki/Раздатка_Лестница_вариативности_A4.pdf",
    "raw/sources/ne-prosto-nakormit/listovki/Раздатка_Моя_еда_мой_выбор_easy_read_A4.pdf",
    "raw/sources/ne-prosto-nakormit/listovki/Раздатка_План_Б_питание_при_закрытии_столовой_A4.pdf",
    "raw/sources/ne-prosto-nakormit/listovki/Раздатка_Таблица_замен_A4.pdf",
    "raw/sources/ne-prosto-nakormit/listovki/Раздатка_Что_сделать_в_понедельник_A4.pdf",
    "raw/sources/ne-prosto-nakormit/listovki/Раздатка_Шесть_измерений_стола_A4.pdf",
    "raw/sources/ne-prosto-nakormit/viktorina/Викторина_диплом_A4.pdf",
    "raw/sources/ne-prosto-nakormit/viktorina/Викторина_карточки_ответов_АБВГ.pdf",
    "raw/sources/ne-prosto-nakormit/viktorina/Викторина_плакат_QR.pdf",
    "raw/sources/ne-prosto-nakormit/viktorina/Викторина_тент_Стол_1.pdf",
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
]

KITCHEN_SNIPPETS = ("проект/chapters/",)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]+`")
WIKI_RE = re.compile(r"\[\[wiki/([^\]]+)\]\]")
FM_RE = re.compile(r"^---\n(.*?)\n---", re.S)


def markdown_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CLAUDE.md"]
    files.extend(sorted((ROOT / "wiki").rglob("*.md")))
    files.extend(sorted((ROOT / "raw/sources/ne-prosto-nakormit").rglob("*.md")))
    files.extend(sorted((ROOT / "raw/sources/related").glob("*/README.md")))
    files.append(ROOT / "raw/sources/related/README.md")
    files.append(ROOT / "raw/assets/README.md")
    seen: set[Path] = set()
    out: list[Path] = []
    for p in files:
        if p.is_file() and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def local_targets(raw: str) -> list[str]:
    target = raw.strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return []
    target = target.split()[0]
    target = target.split("#", 1)[0]
    return [target] if target else []


def wiki_pages() -> set[str]:
    pages = set()
    for path in (ROOT / "wiki").rglob("*.md"):
        rel = path.relative_to(ROOT / "wiki").as_posix()
        if rel.endswith(".md"):
            pages.add(rel[:-3])
    return pages


def main() -> int:
    errors: list[str] = []

    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    leftover = [p for p in FORBIDDEN if (ROOT / p).exists()]
    if missing:
        errors.append("Нет обязательных файлов:\n" + "\n".join(f"  {p}" for p in missing))
    if leftover:
        errors.append("На витрине осталась кухня:\n" + "\n".join(f"  {p}" for p in leftover))

    numbered = [p.name for p in ROOT.iterdir() if p.is_dir() and p.name[:1].isdigit()]
    if numbered:
        errors.append("Нумерованные каталоги должны жить в raw/: " + ", ".join(numbered))

    broken: list[str] = []
    kitchen: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        stripped = CODE_FENCE_RE.sub("", text)
        stripped = INLINE_CODE_RE.sub("", stripped)
        for snippet in KITCHEN_SNIPPETS:
            if snippet in text:
                kitchen.append(f"{path.relative_to(ROOT)}: `{snippet}`")
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
        if path.name in {"README.md"}:
            continue
        if path.parent == ROOT / "wiki" / "queries":
            continue
        if not FM_RE.match(text):
            errors.append(f"Нет frontmatter: {path.relative_to(ROOT)}")
    if dangling_wiki:
        errors.append("Битые wikilinks:\n" + "\n".join(f"  {p}" for p in dangling_wiki))

    index = (ROOT / "wiki/index.md").read_text(encoding="utf-8")
    catalogued = set(WIKI_RE.findall(index))
    content_pages = {
        p
        for p in pages
        if p not in {"index", "log", "queries/README"}
        and not p.startswith("queries/")
    }
    # overview, gaps listed; concepts/entities/sources must be in index
    unlisted = sorted(
        p
        for p in content_pages
        if p not in catalogued and p not in {"overview", "gaps"}
        and not p.startswith("queries/")
    )
    # overview and gaps are listed too — check they are catalogued
    for must in ("overview", "gaps"):
        if must not in catalogued:
            errors.append(f"wiki/index.md не содержит [[{must}]]")
    if unlisted:
        errors.append("Страницы wiki нет в index.md:\n" + "\n".join(f"  {p}" for p in unlisted))

    if errors:
        print("\n\n".join(errors))
        return 1
    wiki_count = len(list((ROOT / "wiki").rglob("*.md")))
    print(
        f"OK: {len(REQUIRED)} обязательных файлов, {wiki_count} wiki md, ссылки живые, raw на месте."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
