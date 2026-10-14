from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .icons import SERVICE_ICON_BASE, SERVICE_ICONS, TECH_ICON_BASE, TECH_ICONS
from .models import Portfolio, Project, Service, SocialLink, Stack_Category, TechStack
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs["class"] = INPUT

    def clean_slug(self):
        slug = self.cleaned_data["slug"].lower()
        if slug in RESERVED:
            raise ValidationError("That slug is reserved. Please choose another.")
        return slug
    
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


class ProjectForm(SluggedFormMixin, PortfolioScopedForm):
    slug_source = "title"

    class Meta:
        model = Project
        fields = ["title", "description", "image", "tech_stack",
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


class TechStackForm(SluggedFormMixin, PortfolioScopedForm):
    slug_source = "name"
    icon_base = TECH_ICON_BASE
    icon = forms.ChoiceField(
        choices=[("", "None")] + TECH_ICONS,
        required=False,
        widget=forms.RadioSelect,
        help_text="Leave on None and we'll try to match the name.",
    )
    
    class Meta:
        model = TechStack
        fields = ["name", "category", "experience_level", "icon"]
        help_texts = {
            "experience_level": "Enter a value from 1 to 100, or leave blank if unknown."
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_field = self.fields["category"]
        valid_categories = [value for value, _ in Stack_Category.CHOICE]
        category_field.queryset = Stack_Category.objects.filter(
            name__in=valid_categories
        ).order_by("id")
        category_field.empty_label = "Choose a category"


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