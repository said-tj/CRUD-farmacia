from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group

class Modulo5AccessTest(TestCase):
    def setUp(self):
        # Preparamos datos de prueba
        self.client = Client()
        self.group = Group.objects.create(name='Módulo5')
        self.user_in = User.objects.create_user('u1', 'u1@example.com', 'pass123')
        self.user_in.groups.add(self.group)
        self.user_out = User.objects.create_user('u2', 'u2@example.com', 'pass456')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('mod5_dashboard'))
        self.assertRedirects(resp, reverse('mod5_login') + '?next=' + reverse('mod5_dashboard'))

    def test_access_for_group_member(self):
        self.client.login(username='u1', password='pass123')
        resp = self.client.get(reverse('mod5_dashboard'))
        self.assertEqual(resp.status_code, 200)

    def test_forbidden_for_non_member(self):
        self.client.login(username='u2', password='pass456')
        resp = self.client.get(reverse('mod5_dashboard'))
        self.assertRedirects(resp, reverse('mod5_login') + '?next=' + reverse('mod5_dashboard'))
