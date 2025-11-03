from django.core.management.base import BaseCommand

from apps.services.models import Service, ServiceCategory


class Command(BaseCommand):
    help = "Create sample services and categories for medical diagnostics center"

    def handle(self, *args, **options):
        # Создаем категории
        categories_data = [
            {
                "name": "Кардиология",
                "order": 1,
                "description": "Диагностика и лечение заболеваний сердечно-сосудистой системы",
            },
            {
                "name": "Неврология",
                "order": 2,
                "description": "Диагностика и лечение заболеваний нервной системы",
            },
            {
                "name": "Рентгенология",
                "order": 3,
                "description": "Лучевая диагностика различных органов и систем",
            },
            {
                "name": "УЗИ диагностика",
                "order": 4,
                "description": "Ультразвуковые исследования органов и тканей",
            },
            {
                "name": "Лабораторные исследования",
                "order": 5,
                "description": "Анализы крови, мочи и других биологических материалов",
            },
        ]

        services_data = [
            # Кардиология
            {
                "category": "Кардиология",
                "name": "Консультация кардиолога",
                "price": 2000,
                "description": "Первичный прием врача-кардиолога с осмотром и консультацией",
            },
            {
                "category": "Кардиология",
                "name": "ЭКГ с расшифровкой",
                "price": 1500,
                "description": "Электрокардиография с подробной расшифровкой результатов",
            },
            {
                "category": "Кардиология",
                "name": "Суточное мониторирование ЭКГ",
                "price": 3500,
                "description": "Холтеровское мониторирование в течение 24 часов",
            },
            {
                "category": "Кардиология",
                "name": "Эхокардиография (УЗИ сердца)",
                "price": 4000,
                "description": "Ультразвуковое исследование сердца и сосудов",
            },
            # Неврология
            {
                "category": "Неврология",
                "name": "Консультация невролога",
                "price": 2000,
                "description": "Первичный прием врача-невролога с неврологическим осмотром",
            },
            {
                "category": "Неврология",
                "name": "Электроэнцефалография (ЭЭГ)",
                "price": 2500,
                "description": "Исследование электрической активности головного мозга",
            },
            {
                "category": "Неврология",
                "name": "УЗИ сосудов головы и шеи",
                "price": 3500,
                "description": "Допплерография сосудов головного мозга и шеи",
            },
            {
                "category": "Неврология",
                "name": "МРТ головного мозга",
                "price": 8000,
                "description": "Магнитно-резонансная томография головного мозга",
            },
            # Рентгенология
            {
                "category": "Рентгенология",
                "name": "Рентген грудной клетки",
                "price": 1500,
                "description": "Рентгенологическое исследование органов грудной клетки",
            },
            {
                "category": "Рентгенология",
                "name": "Рентген позвоночника",
                "price": 2000,
                "description": "Рентгенологическое исследование различных отделов позвоночника",
            },
            {
                "category": "Рентгенология",
                "name": "Рентген суставов",
                "price": 1800,
                "description": "Рентгенологическое исследование суставов (коленный, тазобедренный, плечевой)",
            },
            {
                "category": "Рентгенология",
                "name": "Флюорография",
                "price": 1000,
                "description": "Профилактическое исследование органов грудной клетки",
            },
            # УЗИ диагностика
            {
                "category": "УЗИ диагностика",
                "name": "УЗИ брюшной полости",
                "price": 2500,
                "description": "Ультразвуковое исследование органов брюшной полости (печень, желчный пузырь, поджелудочная железа, селезенка)",
            },
            {
                "category": "УЗИ диагностика",
                "name": "УЗИ щитовидной железы",
                "price": 1800,
                "description": "Ультразвуковое исследование щитовидной железы и паращитовидных желез",
            },
            {
                "category": "УЗИ диагностика",
                "name": "УЗИ молочных желез",
                "price": 2200,
                "description": "Ультразвуковое исследование молочных желез",
            },
            {
                "category": "УЗИ диагностика",
                "name": "УЗИ органов малого таза",
                "price": 2800,
                "description": "Ультразвуковое исследование органов малого таза",
            },
            # Лабораторные исследования
            {
                "category": "Лабораторные исследования",
                "name": "Общий анализ крови",
                "price": 800,
                "description": "Развернутый клинический анализ крови с лейкоцитарной формулой",
            },
            {
                "category": "Лабораторные исследования",
                "name": "Биохимический анализ крови",
                "price": 2500,
                "description": "Комплексный биохимический анализ крови (12 показателей)",
            },
            {
                "category": "Лабораторные исследования",
                "name": "Общий анализ мочи",
                "price": 600,
                "description": "Общий клинический анализ мочи",
            },
            {
                "category": "Лабораторные исследования",
                "name": "Гормональные исследования",
                "price": 1500,
                "description": "Исследование гормонального профиля (ТТГ, Т4 свободный, пролактин и др.)",
            },
        ]

        # Создаем категории
        categories = {}
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data["name"],
                defaults={
                    "order": cat_data["order"],
                    "description": cat_data["description"],
                },
            )
            categories[cat_data["name"]] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана категория: {cat_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Категория уже существует: {cat_data["name"]}'))

        # Создаем услуги
        for service_data in services_data:
            category = categories[service_data["category"]]
            service, created = Service.objects.get_or_create(
                name=service_data["name"],
                category=category,
                defaults={
                    "price": service_data["price"],
                    "description": service_data["description"],
                    "is_active": True,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана услуга: {service_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Услуга уже существует: {service_data["name"]}'))

        self.stdout.write(self.style.SUCCESS("Успешно созданы тестовые данные для услуг!"))
