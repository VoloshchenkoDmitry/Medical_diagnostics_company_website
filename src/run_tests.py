#!/usr/bin/env python
import subprocess
import sys


def run_command(command, description):
    """Запускает команду и выводит результат"""
    print(f"\n{'=' * 50}")
    print(f"🚀 {description}")
    print(f"{'=' * 50}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ {description} завершилась с ошибкой")
        return False
    print(f"✅ {description} завершена успешно")
    return True


def main():
    """Основная функция запуска тестов и проверок"""
    commands = [
        ("python -m pytest -x", "Запуск тестов"),
        ("python -m coverage report", "Отчет о покрытии кода"),
        ("python -m flake8 apps/", "Проверка стиля кода с flake8"),
        ("python -m isort --check-only apps/", "Проверка сортировки импортов"),
        ("python -m black --check apps/", "Проверка форматирования кода"),
    ]

    all_passed = True
    for command, description in commands:
        if not run_command(command, description):
            all_passed = False

    if all_passed:
        print(f"\n🎉 Все проверки пройдены успешно!")
        sys.exit(0)
    else:
        print(f"\n💥 Некоторые проверки не пройдены")
        sys.exit(1)


if __name__ == "__main__":
    main()