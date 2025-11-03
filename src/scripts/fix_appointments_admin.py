#!/usr/bin/env python
"""
Исправляем конкретные проблемы в appointments/admin.py
"""

from pathlib import Path


def fix_appointments_admin():
    """Исправляем appointments/admin.py"""
    path = Path(".src/apps/appointments/admin.py")
    if not path.exists():
        print("❌ Файл appointments/admin.py не найден")
        return

    content = path.read_text(encoding="utf-8")

    # Исправляем проблемные строки
    lines = content.split("\n")
    new_lines = []

    for i, line in enumerate(lines):
        # Исправляем строку 108: multiple spaces before operator
        if i == 107:  # 0-based индекс
            line = line.replace("  )", " )")

        # Исправляем строки 110-115: убираем точки с запятой и лишние пробелы
        if i >= 109 and i <= 114:
            # Убираем точки с запятой
            line = line.replace(";", "")
            # Исправляем multiple spaces after operator
            line = line.replace("=  ", "= ")
            # Исправляем missing whitespace after :
            line = line.replace(":", ": ")
            # Исправляем multiple spaces before operator
            line = line.replace("  +", " +")

        new_lines.append(line)

    # Объединяем строки которые были разбиты точками с запятой
    final_lines = []
    i = 0
    while i < len(new_lines):
        line = new_lines[i]
        if i < len(new_lines) - 1 and new_lines[i + 1].strip() == "" and "select_related" in line:
            # Объединяем связанные строки
            next_line = new_lines[i + 2] if i + 2 < len(new_lines) else ""
            if "service__category" in next_line:
                combined_line = line.strip() + " " + next_line.strip()
                final_lines.append(combined_line)
                i += 3
            else:
                final_lines.append(line)
                i += 1
        else:
            final_lines.append(line)
            i += 1

    path.write_text("\n".join(final_lines), encoding="utf-8")
    print("✅ appointments/admin.py исправлен")


if __name__ == "__main__":
    fix_appointments_admin()
