#!/usr/bin/env python
"""
Упрощенный скрипт для запуска тестов внутри Docker контейнера
"""

import os
import sys

import django

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    # Настраиваем Django
    django.setup()

    # Запускаем тесты
    import pytest

    exit_code = pytest.main(
        [
            "--cov=src",
            "--cov-report=term",
            "--cov-report=html",
            "--cov-fail-under=75",
            "-v",
        ]
    )

    sys.exit(exit_code)
