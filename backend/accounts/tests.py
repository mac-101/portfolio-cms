from django.test import TestCase

from .forms import SignUpForm


class SignUpFormTests(TestCase):
    def test_email_is_required_and_saved_to_user(self):
        form = SignUpForm(data={
            "username": "portfolio-user",
            "email": "owner@example.com",
            "password1": "StrongPass!458",
            "password2": "StrongPass!458",
        })

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.email, "owner@example.com")
        self.assertEqual(user.portfolio.email, "owner@example.com")

    def test_email_is_required(self):
        form = SignUpForm(data={
            "username": "portfolio-user",
            "password1": "StrongPass!458",
            "password2": "StrongPass!458",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_password_guidance_is_hidden_but_validation_errors_are_shown(self):
        form = SignUpForm(data={
            "username": "portfolio-user",
            "email": "owner@example.com",
            "password1": "password",
            "password2": "password",
        })

        self.assertTrue(all(not field.help_text for field in form.fields.values()))
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
