from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import LoginForm, SignUpForm


class SignUpFormTests(TestCase):
    def test_email_is_required_and_saved_to_user(self):
        form = SignUpForm(data={
            "full_name": "Portfolio User",
            "email": "owner@example.com",
            "password1": "StrongPass!458",
            "password2": "StrongPass!458",
        })

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.email, "owner@example.com")
        self.assertEqual(user.get_full_name(), "Portfolio User")
        self.assertEqual(user.username, "portfolio_user")
        self.assertEqual(user.portfolio.name, "Portfolio User")
        self.assertEqual(user.portfolio.email, "owner@example.com")

    def test_email_is_required(self):
        form = SignUpForm(data={
            "full_name": "Portfolio User",
            "password1": "StrongPass!458",
            "password2": "StrongPass!458",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_signup_rejects_email_already_in_use_case_insensitively(self):
        get_user_model().objects.create_user(
            username="existing-user",
            email="owner@example.com",
            password="StrongPass!458",
        )
        form = SignUpForm(data={
            "full_name": "New User",
            "email": "OWNER@example.com",
            "password1": "StrongPass!458",
            "password2": "StrongPass!458",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_username_is_generated_from_full_name_and_is_unique(self):
        from django.contrib.auth import get_user_model

        get_user_model().objects.create_user(
            username="jane_doe",
            password="StrongPass!458",
        )
        form = SignUpForm(data={
            "full_name": "Jane Doe",
            "email": "jane@example.com",
            "password1": "StrongPass!458",
            "password2": "StrongPass!458",
        })

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.username, "jane_doe_2")
        self.assertEqual(user.get_full_name(), "Jane Doe")

    def test_password_guidance_is_hidden_but_validation_errors_are_shown(self):
        form = SignUpForm(data={
            "full_name": "Portfolio User",
            "email": "owner@example.com",
            "password1": "password",
            "password2": "password",
        })

        self.assertTrue(all(not field.help_text for field in form.fields.values()))
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_login_uses_email_case_insensitively(self):
        user = get_user_model().objects.create_user(
            username="email-login-user",
            email="owner@example.com",
            password="StrongPass!458",
        )
        form = LoginForm(
            data={"email": "OWNER@example.com", "password": "StrongPass!458"}
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.get_user(), user)

    def test_login_resolves_existing_duplicate_email_by_password(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username="duplicate-one",
            email="shared@example.com",
            password="StrongPass!458",
        )
        matching_user = user_model.objects.create_user(
            username="duplicate-two",
            email="shared@example.com",
            password="DifferentPass!976",
        )
        form = LoginForm(
            data={"email": "shared@example.com", "password": "DifferentPass!976"}
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.get_user(), matching_user)

    def test_login_rejects_duplicate_email_when_credentials_are_ambiguous(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username="duplicate-one",
            email="shared@example.com",
            password="SamePass!458",
        )
        user_model.objects.create_user(
            username="duplicate-two",
            email="shared@example.com",
            password="SamePass!458",
        )
        form = LoginForm(
            data={"email": "shared@example.com", "password": "SamePass!458"}
        )

        self.assertFalse(form.is_valid())

    def test_login_view_authenticates_with_email_and_uses_email_input(self):
        user = get_user_model().objects.create_user(
            username="login-view-user",
            email="login@example.com",
            password="StrongPass!458",
        )

        response = self.client.post(
            reverse("login"),
            {"email": "login@example.com", "password": "StrongPass!458"},
        )

        self.assertRedirects(response, "/dashboard/", fetch_redirect_response=False)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_login_page_renders_an_email_input(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'type="email"')
        self.assertContains(response, 'name="email"')
