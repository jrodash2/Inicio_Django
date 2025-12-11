from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.admin_group = Group.objects.create(name="administrador")
        self.manager_group = Group.objects.create(name="gestor")

        self.admin_user = self.User.objects.create_user(
            username="admin", password="pass1234", is_active=True
        )
        self.admin_user.groups.add(self.admin_group)

        self.manager_user = self.User.objects.create_user(
            username="manager", password="pass1234", is_active=True
        )
        self.manager_user.groups.add(self.manager_group)

        self.inactive_user = self.User.objects.create_user(
            username="inactive", password="pass1234", is_active=False
        )

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("inicio"))
        self.assertRedirects(response, f"{reverse('login')}?next=/")

    def test_dashboard_shows_user_metrics(self):
        self.client.login(username="admin", password="pass1234")
        response = self.client.get(reverse("inicio"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["usuarios_totales"], 3)
        self.assertEqual(response.context["usuarios_activos"], 2)
        self.assertEqual(response.context["usuarios_inactivos"], 1)
        self.assertEqual(response.context["administradores"], 1)
        self.assertEqual(response.context["gestores"], 1)
        self.assertContains(response, "Usuarios activos")
        self.assertContains(response, "Administradores")
