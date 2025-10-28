from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages


class CommonViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Медицинский Диагностический Центр')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertContains(response, 'О нашей компании')

    def test_contacts_view_get(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts.html')
        # Проверяем наличие ключевых элементов на странице контактов
        self.assertContains(response, 'Контакты')
        self.assertContains(response, 'форма')  # Ищем форму или связанный текст
        self.assertContains(response, 'name')  # Поле имени в форме
        self.assertContains(response, 'email')  # Поле email в форме

    def test_contacts_view_post_valid(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }
        response = self.client.post(reverse('contacts'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertRedirects(response, reverse('contacts'))

        # Проверяем, что сообщение об успехе добавлено
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')

    def test_contacts_view_post_invalid(self):
        data = {
            'name': '',  # Invalid - empty name
            'email': 'invalid-email',
            'subject': '',
            'message': ''
        }
        response = self.client.post(reverse('contacts'), data)
        self.assertEqual(response.status_code, 200)  # Stays on same page
        self.assertTemplateUsed(response, 'contacts.html')
        # Проверяем, что форма показывает ошибки
        self.assertContains(response, 'form')