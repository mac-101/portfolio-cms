from django import forms

from .models import Feedback

INPUT = (
    "block w-full rounded-md border border-neutral-300 bg-white px-3 py-2.5 text-base "
    "text-neutral-900 focus:border-neutral-900 focus:outline-none "
    "focus-visible:ring-2 focus-visible:ring-neutral-900 sm:text-sm"
)

# "Contact" messages have their own form, so they're not offered as a feedback category.
PUBLIC_CATEGORIES = [
    choice for choice in Feedback.Category.choices
    if choice[0] != Feedback.Category.CONTACT
]


class FeedbackForm(forms.ModelForm):
    website = forms.CharField(required=False)  # honeypot: real people never fill this in

    class Meta:
        model = Feedback
        fields = ["category", "message", "name", "email"]
        labels = {
            "category": "Category",
            "message": "Your feedback",
            "name": "Name (optional)",
            "email": "Email (optional)",
        }
        help_texts = {"email": "Only add this if you'd like a reply."}
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = PUBLIC_CATEGORIES
        for name, field in self.fields.items():
            if name == "website":
                field.widget.attrs.update({"tabindex": "-1", "autocomplete": "off"})
            else:
                field.widget.attrs["class"] = INPUT

        if user is not None and user.is_authenticated and not self.is_bound:
            self.initial.setdefault("name", user.get_full_name() or user.username)
            self.initial.setdefault("email", user.email)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["email", "message"]
        labels = {"email": "Reply-to email", "message": "Message"}
        help_texts = {"email": "Replies are sent to this address."}
        widgets = {"message": forms.Textarea(attrs={"rows": 6})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT

        if user is not None and user.is_authenticated and not self.is_bound:
            self.initial.setdefault("email", user.email)