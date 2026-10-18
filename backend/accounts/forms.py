from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

INPUT = (
    "block w-full rounded-md border border-neutral-300 px-3 py-2 text-sm "
    "focus:border-neutral-900 focus:outline-none"
)


def style(form):
    for field in form.fields.values():
        field.widget.attrs["class"] = INPUT


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""
        style(self)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style(self)