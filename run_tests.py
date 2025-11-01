#!/usr/bin/env python
"""
Скрипт для запуска тестов проекта Medical Diagnostics
"""

import os
import sys
import subprocess
import django
from django.conf import settings

# Добавляем src в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


def run_command(command, description):
    """Запускает команду и выводит результат"""
    print(f"\n{'=' * 60}")
    print(f"🚀 {description}")
    print(f"{'=' * 60}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при выполнении: {e}")
        return False


def main():
    """Основная функция запуска тестов"""
    print("🧪 Запуск тестов и проверок качества кода")

    # 1. Проверка миграций
    success = run_command(
        "python src/manage.py makemigrations --check --dry-run",
        "Проверка миграций"
    )
    if not success:
        print("❌ Есть непримененные миграции")
        sys.exit(1)

    # 2. Запуск тестов
    success = run_command(
        "pytest --cov=. --cov-report=term --cov-report=html --cov-fail-under=75 -v",
        "Запуск тестов с покрытием"
    )
    if not success:
        print("❌ Тесты не пройдены")
        sys.exit(1)

    # 3. Проверка качества кода
    success = run_command(
        "flake8 . --count --statistics",
        "Проверка стиля кода (flake8)"
    )
    if not success:
        print("⚠️  Найдены проблемы со стилем кода")

    # 4. Форматирование кода
    success = run_command(
        "black . --check",
        "Проверка форматирования (black)"
    )
    if not success:
        print("⚠️  Код требует форматирования. Запустите: black .")

    # 5. Сортировка импортов
    success = run_command(
        "isort . --check-only",
        "Проверка сортировки импортов (isort)"
    )
    if not success:
        print("⚠️  Импорты требуют сортировки. Запустите: isort .")

    print(f"\n{'=' * 60}")
    print("✅ Все проверки завершены!")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()