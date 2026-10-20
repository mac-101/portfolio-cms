import tempfile

from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from api.serializers import PortfolioSerializer, ProjectSerializer, TechStackSerializer
from .forms import PortfolioForm, ProjectForm, TechStackForm
from .models import Project, Resume, Stack_Category, TechStack


class CustomCategoryFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
            username="category-user",
            email="category@example.com",
            password="test-password",
        )
        cls.portfolio = user.portfolio
        cls.portfolio.name = "Category Portfolio"
        cls.portfolio.slug = "category-portfolio"
        cls.portfolio.save()

    def test_project_form_creates_and_saves_custom_category(self):
        form = ProjectForm(
            data={
                "title": "Custom category project",
                "category": "",
                "new_category": "  Game Development  ",
            },
            portfolio=self.portfolio,
        )

        self.assertTrue(form.is_valid(), form.errors)
        project = form.save()

        self.assertEqual(project.category.name, "Game Development")
        self.assertEqual(Stack_Category.objects.filter(name="Game Development").count(), 1)

    def test_tech_stack_form_reuses_custom_category_case_insensitively(self):
        category = Stack_Category.objects.create(name="Data Platform")
        form = TechStackForm(
            data={
                "name": "ClickHouse",
                "category": "",
                "new_category": "data platform",
                "experience_level": "80",
                "icon": "",
            },
            portfolio=self.portfolio,
        )

        self.assertTrue(form.is_valid(), form.errors)
        technology = form.save()

        self.assertEqual(technology.category, category)
        self.assertEqual(Stack_Category.objects.filter(name__iexact="data platform").count(), 1)

    def test_project_and_tech_stack_forms_share_custom_categories(self):
        project_form = ProjectForm(
            data={
                "title": "Shared category project",
                "category": "",
                "new_category": "Creative Tools",
            },
            portfolio=self.portfolio,
        )
        tech_form = TechStackForm(
            data={
                "name": "Blender",
                "category": "",
                "new_category": "creative tools",
                "experience_level": "",
                "icon": "",
            },
            portfolio=self.portfolio,
        )

        self.assertTrue(project_form.is_valid(), project_form.errors)
        self.assertTrue(tech_form.is_valid(), tech_form.errors)
        project = project_form.save()
        technology = tech_form.save()

        self.assertEqual(project.category, technology.category)
        self.assertEqual(Stack_Category.objects.filter(name__iexact="creative tools").count(), 1)

    def test_custom_category_is_saved_when_model_form_uses_commit_false(self):
        form = ProjectForm(
            data={
                "title": "Deferred project",
                "category": "",
                "new_category": "Research",
            },
            portfolio=self.portfolio,
        )

        self.assertTrue(form.is_valid(), form.errors)
        project = form.save(commit=False)
        project.save()
        form.save_m2m()

        project.refresh_from_db()
        self.assertEqual(project.category.name, "Research")

    def test_project_form_page_renders_category_dropdown_and_custom_input(self):
        self.client.force_login(self.portfolio.owner)

        response = self.client.get(reverse("project_create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="category"', count=1)
        self.assertContains(response, 'name="new_category"', count=1)
        self.assertContains(response, "Backend")

    def test_tech_stack_form_renders_category_dropdown_and_custom_input(self):
        self.client.force_login(self.portfolio.owner)

        response = self.client.get(reverse("tech_create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="category"', count=1)
        self.assertContains(response, 'name="new_category"', count=1)

    def test_category_names_are_included_in_public_serializers(self):
        category = Stack_Category.objects.create(name="Data Science")
        project = Project.objects.create(
            portfolio=self.portfolio,
            title="Data project",
            slug="data-project",
            category=category,
        )
        technology = TechStack.objects.create(
            portfolio=self.portfolio,
            name="Polars",
            slug="polars",
            category=category,
        )

        self.assertEqual(ProjectSerializer(project).data["category"], "Data Science")
        self.assertEqual(TechStackSerializer(technology).data["category"], "Data Science")

    def test_profile_full_name_updates_account_and_generates_username(self):
        form = PortfolioForm(
            data={
                "name": "Jordan Smith",
                "slug": self.portfolio.slug,
                "bio": self.portfolio.bio,
                "location": self.portfolio.location,
                "email": "jordan@example.com",
            },
            instance=self.portfolio,
            user=self.portfolio.owner,
        )

        self.assertTrue(form.is_valid(), form.errors)
        form.save()

        self.portfolio.owner.refresh_from_db()
        self.portfolio.refresh_from_db()
        self.assertEqual(self.portfolio.name, "Jordan Smith")
        self.assertEqual(PortfolioSerializer(self.portfolio).data["name"], "Jordan Smith")
        self.assertEqual(self.portfolio.owner.get_full_name(), "Jordan Smith")
        self.assertEqual(self.portfolio.owner.username, "jordan_smith")
        self.assertEqual(self.portfolio.email, "jordan@example.com")
        self.assertEqual(self.portfolio.owner.email, "jordan@example.com")


class ResumeUploadTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media_directory = tempfile.TemporaryDirectory()
        cls.file_field = Resume._meta.get_field("file")
        cls.original_storage = cls.file_field.storage
        cls.file_field.storage = FileSystemStorage(location=cls.media_directory.name)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.file_field.storage = cls.original_storage
        cls.media_directory.cleanup()

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
            username="resume-user",
            email="resume@example.com",
            password="test-password",
        )
        cls.portfolio = user.portfolio

    def make_upload(self, filename, content=b"%PDF-test"):
        return SimpleUploadedFile(filename, content, content_type="application/pdf")

    def test_upload_replaces_existing_file_and_keeps_one_resume(self):
        self.client.force_login(self.portfolio.owner)

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("resume_manage"),
                {"file": self.make_upload("first.pdf")},
            )
        self.assertRedirects(response, reverse("resume_manage"))
        resume = Resume.objects.get(portfolio=self.portfolio)
        first_file_name = resume.file.name
        self.assertEqual(resume.original_filename, "first.pdf")
        self.assertTrue(resume.file.storage.exists(first_file_name))

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("resume_manage"),
                {"file": self.make_upload("replacement.docx", b"docx-content")},
            )
        self.assertRedirects(response, reverse("resume_manage"))
        resume.refresh_from_db()

        self.assertEqual(Resume.objects.filter(portfolio=self.portfolio).count(), 1)
        self.assertEqual(resume.original_filename, "replacement.docx")
        self.assertNotEqual(resume.file.name, first_file_name)
        self.assertFalse(resume.file.storage.exists(first_file_name))
        self.assertTrue(resume.file.storage.exists(resume.file.name))

    def test_upload_rejects_unsupported_extension(self):
        self.client.force_login(self.portfolio.owner)

        response = self.client.post(
            reverse("resume_manage"),
            {"file": self.make_upload("notes.txt", b"text")},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Resume.objects.filter(portfolio=self.portfolio).exists())
        self.assertContains(response, "File extension")

    def test_resume_api_returns_download_url_and_missing_resume_is_404(self):
        response = self.client.get(
            reverse("public_resume", kwargs={"slug": self.portfolio.slug})
        )
        self.assertEqual(response.status_code, 404)

        resume = Resume.objects.create(
            portfolio=self.portfolio,
            file=self.make_upload("portfolio.pdf"),
        )
        response = self.client.get(
            reverse("public_resume", kwargs={"slug": self.portfolio.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["original_filename"], "portfolio.pdf")
        self.assertTrue(response.json()["file"].endswith(resume.file.url))

    def test_resume_delete_removes_record_and_file(self):
        resume = Resume.objects.create(
            portfolio=self.portfolio,
            file=self.make_upload("private.pdf"),
        )
        self.client.force_login(self.portfolio.owner)

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(reverse("resume_delete"))

        self.assertRedirects(response, reverse("resume_manage"))
        self.assertFalse(Resume.objects.filter(pk=resume.pk).exists())
        self.assertFalse(resume.file.storage.exists(resume.file.name))

    def test_resume_management_requires_login(self):
        response = self.client.get(reverse("resume_manage"))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('resume_manage')}")
