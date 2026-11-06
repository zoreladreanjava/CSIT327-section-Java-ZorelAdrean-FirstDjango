from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser

BOOTSTRAP_CSS = "bootstrap@5.3.3/dist/css/bootstrap.min.css"


class AccessTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user("student", password="pw")
        self.admin = CustomUser.objects.create_user(
            "boss", password="pw", role=CustomUser.Role.ADMIN
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('dashboard')}"
        )

    def test_student_is_refused_admin_panel_on_styled_page(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("admin_panel"))
        self.assertContains(response, BOOTSTRAP_CSS, status_code=403)

    def test_admin_can_open_admin_panel(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("admin_panel")).status_code, 200)

    def test_admin_panel_link_only_shown_to_admins(self):
        url = reverse("admin_panel")
        self.client.force_login(self.student)
        self.assertNotContains(self.client.get(reverse("dashboard")), url)
        self.client.force_login(self.admin)
        self.assertContains(self.client.get(reverse("dashboard")), url)


class BootstrapTests(TestCase):
    def test_public_pages_load_bootstrap(self):
        for name in ("login", "signup"):
            with self.subTest(page=name):
                self.assertContains(self.client.get(reverse(name)), BOOTSTRAP_CSS)

    def test_logged_in_pages_load_bootstrap(self):
        user = CustomUser.objects.create_user(
            "boss", password="pw", role=CustomUser.Role.ADMIN
        )
        self.client.force_login(user)
        for name in ("dashboard", "profile", "admin_panel"):
            with self.subTest(page=name):
                self.assertContains(self.client.get(reverse(name)), BOOTSTRAP_CSS)
