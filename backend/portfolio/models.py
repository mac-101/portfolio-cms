import uuid
from django.conf import settings
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from pathlib import Path
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from .icons import SERVICE_ICON_BASE, TECH_ICON_BASE, guess_tech_icon


def project_image_path(instance, filename):
    ext = Path(filename).suffix.lower()
    return f"users/{instance.portfolio.owner_id}/projects/{uuid.uuid4().hex}{ext}"


def profile_image_path(instance, filename):
    ext = Path(filename).suffix.lower()
    return f"users/{instance.owner_id}/profile/{uuid.uuid4().hex}{ext}"


def resume_file_path(instance, filename):
    ext = Path(filename).suffix.lower()
    return f"users/{instance.portfolio.owner_id}/resume/{uuid.uuid4().hex}{ext}"


class Stack_Category(models.Model):
    CHOICE = (
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("devops", "DevOps"),
        ("mobile", "Mobile"),
        ("other", "Other"),
    )
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return dict(self.CHOICE).get(self.name, self.name)


class Portfolio(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolio"
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=50, unique=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to=profile_image_path, blank=True)
    location = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TechStack(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="tech_stack")
    name = models.CharField(max_length=60)
    category = models.ForeignKey(Stack_Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="tech_stacks")
    experience_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        default=1,
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=70, blank=True)
    icon = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["portfolio", "slug"], name="unique_tech_slug_per_portfolio")
        ]
        
    @property
    def icon_url(self):
        return f"{TECH_ICON_BASE}{self.icon}.svg" if self.icon else ""

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self._state.adding and not self.icon:      # only when first created
            self.icon = guess_tech_icon(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=120)
    category = models.ForeignKey(
        Stack_Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    slug = models.SlugField(max_length=140, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=project_image_path, blank=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name="projects")
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["portfolio", "slug"], name="unique_project_slug_per_portfolio")
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Service(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name="services")

    @property
    def icon_url(self):
        return f"{SERVICE_ICON_BASE}{self.icon}.svg" if self.icon else ""
    
    def __str__(self):
        return self.title


class SocialLink(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=50)
    url = models.URLField()
    label = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f"{self.platform}: {self.url}"


class Resume(models.Model):
    portfolio = models.OneToOneField(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="resume",
    )
    file = models.FileField(
        storage=RawMediaCloudinaryStorage(),
        upload_to=resume_file_path,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])],
    )
    original_filename = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.file and not self.file._committed:
            self.original_filename = Path(self.file.name).name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resume for {self.portfolio.name}"