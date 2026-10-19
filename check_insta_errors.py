from pathlib import Path
import json

ROOT = Path("../Instagram-All")
REPORT = ROOT / "error_report.txt"

index_files = list(ROOT.rglob("index.json"))

total_items = 0
failed_items = []
broken_indexes = []

for index_file in index_files:
    category = index_file.parent.name

    try:
        with open(index_file, "r", encoding="utf-8") as file:
            records = json.load(file)

    except Exception as error:
        broken_indexes.append({
            "category": category,
            "index": str(index_file),
            "error": str(error)
        })
        continue

    for record in records:
        total_items += 1

        status = str(record.get("status", "")).casefold()
        error = record.get("error")

        if status == "failed" or error:
            failed_items.append({
                "category": category,
                "shortcode": record.get("shortcode", "Unknown"),
                "url": record.get("url", "Unknown"),
                "error": error or "Status marked as failed"
            })


lines = [
    "INSTAGRAM BACKUP ERROR REPORT",
    "=" * 40,
    f"Index files found: {len(index_files)}",
    f"Items checked: {total_items}",
    f"Failed items: {len(failed_items)}",
    f"Unreadable index files: {len(broken_indexes)}",
    ""
]

if failed_items:
    lines.append("FAILED DOWNLOADS")
    lines.append("=" * 40)

    for number, item in enumerate(failed_items, start=1):
        lines.extend([
            f"{number}. Category: {item['category']}",
            f"   Shortcode: {item['shortcode']}",
            f"   URL: {item['url']}",
            f"   Error: {item['error']}",
            ""
        ])
else:
    lines.extend([
        "No failed downloads were found.",
        ""
    ])

if broken_indexes:
    lines.append("UNREADABLE INDEX FILES")
    lines.append("=" * 40)

    for number, item in enumerate(broken_indexes, start=1):
        lines.extend([
            f"{number}. Category: {item['category']}",
            f"   Index: {item['index']}",
            f"   Error: {item['error']}",
            ""
        ])

report_text = "\n".join(lines)

print(report_text)

with open(REPORT, "w", encoding="utf-8") as file:
    file.write(report_text)

print(f"\nReport saved to: {REPORT.resolve()}")