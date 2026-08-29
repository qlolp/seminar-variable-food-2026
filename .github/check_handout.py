#!/usr/bin/env python3
"""Проверка витрины: канонические файлы есть, ссылки живые, кухня сборки отсутствует."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "LICENSE",
    "01_доклад/Не_просто_накормить_доклад_редакция.pdf",
    "01_доклад/Не_просто_накормить_доклад.md",
    "01_доклад/Не_просто_накормить_доклад_стиль_claude.pdf",
    "01_доклад/Не_просто_накормить_КРАТКАЯ_версия.pdf",
    "02_презентация/Презентация_v6_Не_просто_накормить.pdf",
    "02_презентация/Презентация_v6_Не_просто_накормить.pptx",
    "03_семинарский_пакет/README.md",
    "03_семинарский_пакет/Памятка_что_унести_в_регион.pdf",
    "03_семинарский_пакет/Вариативное_питание_опыт_реализации.pdf",
    "03_семинарский_пакет/21_если_инспектор_не_принял.pdf",
    "03_семинарский_пакет/21_если_инспектор_не_принял.md",
    "03_семинарский_пакет/Калькулятор_стоимости_вариативности.xlsx",
    "03_семинарский_пакет/04_записка_руководителю.md",
    "03_семинарский_пакет/05_чеклист_понедельник.md",
    "03_семинарский_пакет/06_10_ошибок.md",
    "03_семинарский_пакет/07_10_вопросов_учредителю.md",
    "03_семинарский_пакет/08_раздатка.md",
    "03_семинарский_пакет/09_сценарий_малых_групп.md",
    "03_семинарский_пакет/10_пять_вопросов_залу.md",
    "03_семинарский_пакет/11_экспресс_аудит_10мин.md",
    "03_семинарский_пакет/12_форма_ступени.md",
    "03_семинарский_пакет/13_трудные_вопросы.md",
    "03_семинарский_пакет/14_возражения.md",
    "03_семинарский_пакет/15_решения_без_средств.md",
    "03_семинарский_пакет/16_решения_с_финансированием.md",
    "03_семинарский_пакет/17_решения_с_учредителем.md",
    "03_семинарский_пакет/18_решения_не_без_врача.md",
    "03_семинарский_пакет/19_юридическое_заключение.md",
    "04_листовки/Раздатка_Лестница_вариативности_A4.pdf",
    "04_листовки/Раздатка_Моя_еда_мой_выбор_easy_read_A4.pdf",
    "04_листовки/Раздатка_План_Б_питание_при_закрытии_столовой_A4.pdf",
    "04_листовки/Раздатка_Таблица_замен_A4.pdf",
    "04_листовки/Раздатка_Что_сделать_в_понедельник_A4.pdf",
    "04_листовки/Раздатка_Шесть_измерений_стола_A4.pdf",
    "05_викторина/Викторина_диплом_A4.pdf",
    "05_викторина/Викторина_карточки_ответов_АБВГ.pdf",
    "05_викторина/Викторина_плакат_QR.pdf",
    "05_викторина/Викторина_тент_Стол_1.pdf",
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
    "02_презентация/archive",
    "02_презентация/презентация_v5_21_слайд",
    "02_презентация/презентация_v4_38_слайдов",
    "02_презентация/презентация_kimi_34_слайда",
    "02_презентация/презентация_v6",
    "04_приложения_и_реестры",
    "05_раздатка_canva",
    "06_викторина_canva",
]

KITCHEN_SNIPPETS = (
    "проект/chapters/",
    "проект/",
)

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    files = [ROOT / "README.md"]
    files.extend(sorted((ROOT / "03_семинарский_пакет").glob("*.md")))
    return files


def local_targets(raw: str) -> list[str]:
    target = raw.strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return []
    target = target.split()[0]
    target = target.split("#", 1)[0]
    return [target] if target else []


def main() -> int:
    errors: list[str] = []

    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    leftover = [p for p in FORBIDDEN if (ROOT / p).exists()]
    if missing:
        errors.append("Нет обязательных файлов:\n" + "\n".join(f"  {p}" for p in missing))
    if leftover:
        errors.append("На витрине осталась кухня:\n" + "\n".join(f"  {p}" for p in leftover))

    broken: list[str] = []
    kitchen: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for snippet in KITCHEN_SNIPPETS:
            if snippet in text:
                kitchen.append(f"{path.relative_to(ROOT)}: `{snippet}`")
        for match in LINK_RE.finditer(text):
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

    if errors:
        print("\n\n".join(errors))
        return 1
    print(
        f"OK: {len(REQUIRED)} файлов на месте, ссылки живые, кухня не вернулась."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
