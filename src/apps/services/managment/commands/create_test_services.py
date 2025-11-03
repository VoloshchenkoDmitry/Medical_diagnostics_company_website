from django.core.management.base import BaseCommand

from apps.services.models import Service, ServiceCategory


class Command(BaseCommand):
    help = "Create test services and categories"

    def handle(self, *args, **options):
        # Создаем категории
        cardiology, created = ServiceCategory.objects.get_or_create(
            name="Кардиология",
            defaults={"description": "Диагностика и лечение заболеваний сердца"},
        )

        neurology, created = ServiceCategory.objects.get_or_create(
            name="Неврология",
            defaults={"description": "Диагностика заболеваний нервной системы"},
        )

        radiology, created = ServiceCategory.objects.get_or_create(
            name="Рентгенология", defaults={"description": "Лучевая диагностика"}
        )

        # Создаем услуги
        services_data = [
            {
                "category": cardiology,
                "name": "ЭКГ (Электрокардиография)",
                "description": "Регистрация электрической активности сердца. Позволяет выявить нарушения ритма, ишемическую болезнь, инфаркт миокарда и другие патологии.",
                "price": 1500.00,
            },
            {
                "category": cardiology,
                "name": "УЗИ сердца (Эхокардиография)",
                "description": "Ультразвуковое исследование сердца, позволяющее оценить структуру и функцию сердечной мышцы, клапанов и крупных сосудов.",
                "price": 3500.00,
            },
            {
                "category": neurology,
                "name": "ЭЭГ (Электроэнцефалография)",
                "description": "Исследование электрической активности головного мозга. Используется для диагностики эпилепсии, нарушений сна и других неврологических заболеваний.",
                "price": 2500.00,
            },
            {
                "category": radiology,
                "name": "Рентген грудной клетки",
                "description": "Рентгенологическое исследование органов грудной клетки для оценки состояния легких, сердца и костных структур.",
                "price": 1200.00,
            },
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(name=service_data["name"], defaults=service_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Создана услуга: {service.name}"))

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
