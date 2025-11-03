#!/usr/bin/env python
"""
Финальное исправление appointments/admin.py
"""

import os
from pathlib import Path


def find_appointments_admin():
    """Находим файл appointments/admin.py"""
    possible_paths = [
        "src/apps/appointments/admin.py",
        "apps/appointments/admin.py",
        "appointments/admin.py",
        "./appointments/admin.py",
    ]

    for path in possible_paths:
        if Path(path).exists():
            print(f"✅ Найден файл: {path}")
            return Path(path)

    # Ищем рекурсивно
    for root, dirs, files in os.walk("."):
        if "appointments" in root and "admin.py" in files:
            file_path = Path(root) / "admin.py"
            print(f"✅ Найден файл: {file_path}")
            return file_path

    print("❌ Файл appointments/admin.py не найден")
    return None


def fix_appointments_admin():
    """Исправляем appointments/admin.py"""
    file_path = find_appointments_admin()
    if not file_path:
        return

    content = file_path.read_text(encoding="utf-8")
    print(f"📏 Размер файла: {len(content)} символов")

    # Покажем первые 10 строк для диагностики
    lines = content.split("\n")
    print("📄 Первые 10 строк файла:")
    for i, line in enumerate(lines[:10]):
        print(f"{i + 1:3}: {line}")

    # Исправляем проблемные места
    new_content = content

    # Исправляем multiple spaces before operator (E221)
    new_content = new_content.replace("  )", " )")
    new_content = new_content.replace("  +", " +")

    # Исправляем multiple statements on one line (E702)
    new_content = new_content.replace(";", "\n")

    # Исправляем missing whitespace (E231)
    new_content = new_content.replace("):", ": ")
    new_content = new_content.replace("user,", "user, ")
    new_content = new_content.replace("service,", "service, ")

    # Исправляем multiple spaces after operator (E222)
    new_content = new_content.replace("=  ", "= ")

    # Записываем исправленный файл
    file_path.write_text(new_content, encoding="utf-8")
    print("✅ appointments/admin.py исправлен")


if __name__ == "__main__":
    fix_appointments_admin()
