from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class SignUpTests(TestCase):
    def test_success_message_is_shown_on_login_page(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newbie",
                "email": "newbie@example.com",
                "first_name": "New",
                "last_name": "Bie",
                "course": "BSIT",
                "password1": "c0rrect-horse-battery",
                "password2": "c0rrect-horse-battery",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("login"))
        self.assertContains(response, "Your account was created")
        self.assertContains(response, "alert-success")
        self.assertTrue(CustomUser.objects.filter(username="newbie").exists())

    def test_invalid_signup_shows_errors_and_no_success_message(self):
        response = self.client.post(
            reverse("signup"),
            {"username": "newbie", "password1": "abc", "password2": "xyz"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "is-invalid")
        self.assertEqual(list(get_messages(response.wsgi_request)), [])
        self.assertFalse(CustomUser.objects.filter(username="newbie").exists())


class ProfileTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("alice", password="pw")
        self.other = CustomUser.objects.create_user("bob", password="pw", course="Math")

    def test_anonymous_user_is_sent_to_login(self):
        url = reverse("profile")
        self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")

    def test_user_can_edit_own_profile(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("profile"),
            {
                "first_name": "Alice",
                "last_name": "Smith",
                "email": "alice@example.com",
                "course": "BSCS",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("dashboard"))
        self.assertContains(response, "Your profile was updated.")
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Alice")
        self.assertEqual(self.user.course, "BSCS")

    def test_invalid_email_is_rejected(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("profile"), {"email": "not-an-email"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "is-invalid")
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "")

    def test_user_cannot_change_own_role_or_staff_status(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("profile"),
            {
                "email": "alice@example.com",
                "role": CustomUser.Role.ADMIN,
                "is_staff": "on",
                "is_superuser": "on",
            },
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "alice@example.com")
        self.assertEqual(self.user.role, CustomUser.Role.STUDENT)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_edit_only_affects_logged_in_user(self):
        self.client.force_login(self.user)
        self.client.post(reverse("profile"), {"course": "Hacked", "id": self.other.pk})
        self.other.refresh_from_db()
        self.assertEqual(self.other.course, "Math")
