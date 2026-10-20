from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils.text import slugify
from accounts.utils import username_for_full_name
from .icons import SERVICE_ICON_BASE, SERVICE_ICONS, TECH_ICON_BASE, TECH_ICONS
from .models import Portfolio, Project, Resume, Service, SocialLink, Stack_Category, TechStack
from .utils import RESERVED

INPUT = (
    "block w-full rounded-md border border-neutral-300 px-3 py-2 text-sm "
    "focus:border-neutral-900 focus:outline-none"
)


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ["name", "slug", "bio", "profile_image", "location", "email"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}
        labels = {"name": "Full name"}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["name"].initial = self.instance.name or user.get_full_name() or user.username
        self.fields["email"].required = True
        self.fields["email"].initial = self.instance.email or user.email
        for field in self.fields.values():
            if not isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs["class"] = INPUT

    def clean_name(self):
        full_name = " ".join(self.cleaned_data["name"].split())
        name_parts = full_name.split(" ", 1)
        if not username_for_full_name(full_name, self.user):
            raise ValidationError("Enter a name containing letters or numbers.")
        if len(name_parts[0]) > 150 or (len(name_parts) > 1 and len(name_parts[1]) > 150):
            raise ValidationError("Each part of your name must be 150 characters or fewer.")
        return full_name

    def save(self, commit=True):
        full_name = self.cleaned_data["name"]
        name_parts = full_name.split(" ", 1)
        self.user.first_name = name_parts[0]
        self.user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        self.user.username = username_for_full_name(full_name, self.user)
        self.user.email = self.cleaned_data["email"]
        if commit:
            with transaction.atomic():
                portfolio = super().save(commit=True)
                self.user.save(
                    update_fields=["first_name", "last_name", "username", "email"]
                )
                return portfolio
        return super().save(commit=False)

    def clean_slug(self):
        slug = self.cleaned_data["slug"].lower()
        if slug in RESERVED:
            raise ValidationError("That slug is reserved. Please choose another.")
        return slug

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if email.casefold() != (self.user.email or "").casefold():
            conflicting_users = self.user.__class__._default_manager.filter(
                email__iexact=email
            ).exclude(pk=self.user.pk)
            if conflicting_users.exists():
                raise ValidationError("An account with this email address already exists.")
        return email
    
def style_fields(form):
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, forms.CheckboxSelectMultiple):
            widget.attrs["class"] = "space-y-1.5 rounded-md border border-neutral-200 p-3 text-sm"
        elif isinstance(widget, (forms.CheckboxInput, forms.ClearableFileInput)):
            continue
        elif isinstance(widget, forms.RadioSelect):
            widget.attrs["class"] = "peer sr-only"
        else:
            widget.attrs["class"] = INPUT


class PortfolioScopedForm(forms.ModelForm):
    """Always bound to a portfolio chosen by the server, never by the browser."""

    def __init__(self, *args, portfolio, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolio = portfolio
        self.instance.portfolio = portfolio
        style_fields(self)


class CustomCategoryFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_field = self.fields["category"]
        category_field.queryset = Stack_Category.objects.order_by("name")
        category_field.empty_label = "Choose a category"

    def _resolve_category(self):
        name = " ".join(self.cleaned_data.get("new_category", "").split())
        if not name:
            return self.cleaned_data.get("category")
        category = Stack_Category.objects.filter(name__iexact=name).first()
        if category:
            return category
        try:
            with transaction.atomic():
                return Stack_Category.objects.create(name=name)
        except IntegrityError:
            return Stack_Category.objects.get(name__iexact=name)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            with transaction.atomic():
                instance.category = self._resolve_category()
                instance.save()
                self.save_m2m()
        else:
            instance.category = self.cleaned_data.get("category")
            save_m2m = self.save_m2m

            def save_with_category():
                instance.category = self._resolve_category()
                instance.save(update_fields=["category"])
                save_m2m()

            self.save_m2m = save_with_category
        return instance


class SluggedFormMixin:
    """Stops duplicate slugs per portfolio with a form error instead of a crash."""

    slug_source = None

    def clean(self):
        cleaned = super().clean()
        value = cleaned.get(self.slug_source)
        if value and not self.instance.pk:
            slug = slugify(value)
            if not slug:
                self.add_error(self.slug_source, "Use at least one letter or number.")
            elif self._meta.model.objects.filter(portfolio=self.portfolio, slug=slug).exists():
                self.add_error(self.slug_source, "You already have one with this name.")
        return cleaned


class ProjectForm(CustomCategoryFormMixin, SluggedFormMixin, PortfolioScopedForm):
    slug_source = "title"
    new_category = forms.CharField(
        max_length=50,
        required=False,
        label="Or add a new category",
        help_text="If entered, this category will be created and selected.",
    )

    class Meta:
        model = Project
        fields = ["title", "category", "new_category", "description", "image", "tech_stack",
                  "github_url", "live_url", "featured", "published"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "tech_stack": forms.CheckboxSelectMultiple,
        }
        labels = {"github_url": "GitHub URL", "live_url": "Live URL"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tech_stack"].queryset = TechStack.objects.filter(portfolio=self.portfolio)
        self.fields["tech_stack"].help_text = "Manage your technologies on the Tech Stack page."


class TechStackForm(CustomCategoryFormMixin, SluggedFormMixin, PortfolioScopedForm):
    slug_source = "name"
    icon_base = TECH_ICON_BASE
    new_category = forms.CharField(
        max_length=50,
        required=False,
        label="Or add a new category",
        help_text="If entered, this category will be created and selected.",
    )
    icon = forms.ChoiceField(
        choices=[("", "None")] + TECH_ICONS,
        required=False,
        widget=forms.RadioSelect,
        help_text="Leave on None and we'll try to match the name.",
    )
    class Meta:
        model = TechStack
        fields = ["name", "category", "new_category", "experience_level", "icon"]
        help_texts = {
            "experience_level": "Enter a value from 1 to 100, or leave blank if unknown."
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ServiceForm(PortfolioScopedForm):
    icon_base = SERVICE_ICON_BASE
    icon = forms.ChoiceField(
        choices=[("", "None")] + SERVICE_ICONS,
        required=False,
        widget=forms.RadioSelect,
    )
    class Meta:
        model = Service
        fields = ["title", "description", "icon"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class SocialLinkForm(PortfolioScopedForm):
    class Meta:
        model = SocialLink
        fields = ["platform", "url", "label"]


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["file"]
        labels = {"file": "Resume file"}
        help_texts = {
            "file": "Accepted formats: PDF, DOC, or DOCX. Uploading a new file replaces your current resume."
        }
        widgets = {
            "file": forms.ClearableFileInput(
                attrs={"accept": ".pdf,.doc,.docx,application/pdf"}
            )
        }

    def __init__(self, *args, portfolio, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolio = portfolio
        self.instance.portfolio = portfolio
        style_fields(self)