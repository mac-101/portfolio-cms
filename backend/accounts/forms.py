from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .utils import username_for_full_name

INPUT = (
    "block w-full rounded-md border border-neutral-300 px-3 py-2 text-sm "
    "focus:border-neutral-900 focus:outline-none"
)


def style(form):
    for field in form.fields.values():
        field.widget.attrs["class"] = INPUT


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=300, label="Full name")
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs["placeholder"] = "e.g. Jane Doe"
        for field in self.fields.values():
            field.help_text = ""
        style(self)

    def clean_full_name(self):
        full_name = " ".join(self.cleaned_data["full_name"].split())
        name_parts = full_name.split(" ", 1)
        if not username_for_full_name(full_name):
            raise forms.ValidationError("Enter a name containing letters or numbers.")
        if len(name_parts[0]) > 150 or (len(name_parts) > 1 and len(name_parts[1]) > 150):
            raise forms.ValidationError("Each part of your name must be 150 characters or fewer.")
        return full_name

    def save(self, commit=True):
        user = super().save(commit=False)
        name_parts = self.cleaned_data["full_name"].split(" ", 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        user.username = username_for_full_name(self.cleaned_data["full_name"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style(self)