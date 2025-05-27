from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import NewsCategory, News, Partner
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Создает тестовые данные для сайта OVI'

    def handle(self, *args, **options):
        # Создаем суперпользователя
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@ovi.uz', 'admin')
            self.stdout.write(self.style.SUCCESS('Создан суперпользователь: admin/admin'))

        # Создаем категории новостей
        categories = [
            {'name': 'О компании', 'slug': 'company'},
            {'name': 'Продукт', 'slug': 'product'},
            {'name': 'Партнерства', 'slug': 'partnerships'},
            {'name': 'Награды', 'slug': 'awards'},
        ]
        
        for cat_data in categories:
            category, created = NewsCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'Создана категория: {category.name}')

        # Создаем тестовые новости
        admin_user = User.objects.get(username='admin')
        
        news_data = [
            {
                'title': 'OVI привлекает $5 млн инвестиций для расширения в регионе',
                'slug': 'ovi-investment-5m',
                'excerpt': 'Платформа OVI успешно привлекла 5 миллионов долларов в рамках раунда Series A.',
                'content': '''Платформа OVI успешно привлекла 5 миллионов долларов в рамках раунда Series A. 
                Инвестиции позволят расширить географию услуг, увеличить команду врачей и внедрить новые технологии 
                для улучшения качества медицинского обслуживания.
                
                Средства будут направлены на:
                - Расширение команды медицинских специалистов
                - Разработку новых функций приложения
                - Увеличение географии покрытия
                - Улучшение логистической инфраструктуры''',
                'category': 'company',
                'is_featured': True,
            },
            {
                'title': 'В команду OVI присоединились 15 новых врачей',
                'slug': 'new-doctors-team',
                'excerpt': 'Мы продолжаем расширять команду медицинских специалистов.',
                'content': '''В мае к команде OVI присоединились 15 врачей различных специальностей. 
                Среди новых коллег - кардиологи, терапевты, педиатры и неврологи с большим опытом работы.
                
                Все специалисты прошли тщательный отбор и обучение работе с нашей платформой.''',
                'category': 'product',
                'is_featured': False,
            },
            {
                'title': 'Запуск ИИ-помощника для предварительной диагностики',
                'slug': 'ai-assistant-launch',
                'excerpt': 'Новый ИИ-помощник поможет пациентам получить предварительные рекомендации.',
                'content': '''OVI запускает инновационного ИИ-помощника, который поможет пациентам получить 
                предварительные рекомендации по симптомам перед консультацией с врачом.
                
                Особенности нового помощника:
                - Анализ симптомов в режиме реального времени
                - Рекомендации по срочности обращения к врачу
                - Предварительная подготовка к консультации''',
                'category': 'product',
                'is_featured': False,
            }
        ]
        
        for news_item in news_data:
            category = NewsCategory.objects.get(slug=news_item['category'])
            news, created = News.objects.get_or_create(
                slug=news_item['slug'],
                defaults={
                    'title': news_item['title'],
                    'excerpt': news_item['excerpt'],
                    'content': news_item['content'],
                    'category': category,
                    'author': admin_user,
                    'is_featured': news_item['is_featured'],
                    'is_published': True,
                }
            )
            if created:
                self.stdout.write(f'Создана новость: {news.title}')

        # Создаем тестовых партнеров
        partners_data = [
            {
                'name': 'Медицинский центр "MedCenter"',
                'slug': 'medcenter',
                'category': 'clinics',
                'description': 'Многопрофильный медицинский центр с современным оборудованием и опытными специалистами.',
                'services': '''Консультации специалистов
Диагностические исследования
Амбулаторное лечение
Профилактические осмотры''',
                'contact_info': '📍 ул. Навои, 15 | 📞 +998 71 123-45-67',
            },
            {
                'name': 'Лаборатория "MedLab"',
                'slug': 'medlab',
                'category': 'labs',
                'description': 'Ведущая диагностическая лаборатория с полным спектром клинических анализов.',
                'services': '''Общеклинические анализы
Биохимические исследования
Гормональные тесты
Микробиологические анализы''',
                'contact_info': '📍 ул. Буюк Ипак Йули, 12 | 📞 +998 71 456-78-90',
            },
            {
                'name': 'Аптечная сеть "Pharma+"',
                'slug': 'pharma-plus',
                'category': 'pharmacies',
                'description': 'Крупнейшая аптечная сеть города с широким ассортиментом лекарственных средств.',
                'services': '''Рецептурные препараты
БАДы и витамины
Медицинские изделия
Косметика и гигиена''',
                'contact_info': '📍 20+ филиалов по городу | 📞 +998 71 678-90-12',
            }
        ]
        
        for partner_data in partners_data:
            partner, created = Partner.objects.get_or_create(
                slug=partner_data['slug'],
                defaults=partner_data
            )
            if created:
                self.stdout.write(f'Создан партнер: {partner.name}')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))