"""Create a standalone, escaped HTML view of pytest and Vitest JUnit reports."""

import argparse
from datetime import UTC, datetime
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET


def section(name, path):
    title = f"<h2>{escape(name)}</h2>"
    if not path.exists():
        return title + '<p class="missing">Отчёт отсутствует. Результаты неизвестны.</p>'
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return title + '<p class="missing">Не удалось прочитать XML отчёта.</p>'
    counts = {"passed": 0, "failed": 0, "skipped": 0}
    labels = {"passed": "Пройден", "failed": "Ошибка", "skipped": "Пропущен"}
    rows = []
    for case in root.iter("testcase"):
        problems = list(case.findall("failure")) + list(case.findall("error"))
        skipped = case.find("skipped")
        status = "failed" if problems else "skipped" if skipped is not None else "passed"
        counts[status] += 1
        diagnostics = problems or ([skipped] if skipped is not None else [])
        detail = "\n\n".join(
            "\n".join(filter(None, [item.get("message"), item.text]))
            for item in diagnostics
        )
        details = (
            f'<details><summary>Подробности</summary><pre>{escape(detail)}</pre></details>'
            if detail else ""
        )
        rows.append(
            f'<tr><td><span class="{status}">{labels[status]}</span></td>'
            f'<td>{escape(case.get("classname", ""))}</td>'
            f'<td>{escape(case.get("name", "Без названия"))}{details}</td>'
            f'<td>{escape(case.get("time", "—"))}</td></tr>'
        )
    summary = (
        f'<p class="counts">Всего: {sum(counts.values())} · '
        f'Пройдено: {counts["passed"]} · Ошибок: {counts["failed"]} · '
        f'Пропущено: {counts["skipped"]}</p>'
    )
    if not rows:
        summary += '<p class="missing">В отчёте нет отдельных тестов. Проверьте журнал запуска.</p>'
    return title + summary + (
        '<div class="scroll"><table><thead><tr><th>Результат</th><th>Набор</th>'
        '<th>Тест и подробности</th><th>Время, с</th></tr></thead><tbody>'
        + "".join(rows) + '</tbody></table></div>'
    )


def render(backend, frontend):
    generated = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    return '''<!doctype html><html lang="ru"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VolunteerHub — результаты тестов</title>
<style>
body{font:16px/1.5 system-ui,sans-serif;color:#172536;background:#f5f7fa;margin:0}
main{max-width:1250px;margin:40px auto;padding:0 24px 40px}
h1{font-size:30px;margin-bottom:8px}h2{margin-top:36px}
.meta{color:#536174}.counts{font-weight:600}.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;background:white;font-size:14px}
th,td{padding:12px;text-align:left;border:1px solid #dce2e8;vertical-align:top}
th{background:#e8edf3}td{overflow-wrap:anywhere}td:last-child{white-space:nowrap}
.passed{color:#17613a;font-weight:700}.failed,.missing{color:#a11c20;font-weight:700}
.skipped{color:#825000;font-weight:700}summary{cursor:pointer;margin-top:8px}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;max-width:700px}
@media print{body{background:white}main{margin:0;padding:0}tr{break-inside:avoid}}
</style><main><h1>VolunteerHub — результаты тестов</h1>
<p class="meta">''' + f"Сформировано: {generated}. Источник: JUnit XML." + '''</p>
<p>Backend — серверные тесты pytest. Frontend — клиентские тесты Vitest.
Для ошибок и пропусков раскройте «Подробности». Время указано для отдельных тестов,
оно не равно длительности всего запуска CI. Отчёт показывает результаты тестов, а не покрытие кода.</p>
''' + section("Backend", backend) + section("Frontend", frontend) + "</main></html>"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", type=Path, default=Path("reports/backend/junit.xml"))
    parser.add_argument("--frontend", type=Path, default=Path("reports/frontend/junit.xml"))
    parser.add_argument("--output", type=Path, default=Path("reports/test-results.html"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(args.backend, args.frontend), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
