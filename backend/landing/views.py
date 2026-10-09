from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import redirect, render

from .forms import PUBLIC_CATEGORIES, ContactForm, FeedbackForm
from .models import Feedback


def too_many_submissions(request, limit=5, window=3600):
    """Allow 5 anonymous feedback posts per IP per hour."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    ip = forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR", "unknown")
    key = f"feedback-rate:{ip}"
    cache.add(key, 0, window)
    return cache.incr(key) > limit


def initial_category(request):
    category = request.GET.get("category")
    if category in [value for value, _ in PUBLIC_CATEGORIES]:
        return {"category": category}
    return {}


# ---------- Public (landing page) ----------

def home(request):
    return render(request, "landing/home.html", {"form": FeedbackForm(user=request.user)})


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST, user=request.user)
        if form.is_valid():
            if form.cleaned_data["website"]:          # honeypot filled in: it's a bot
                return redirect("feedback_thanks")
            if too_many_submissions(request):
                form.add_error(None, "Too many submissions from your network. Please try again later.")
            else:
                item = form.save(commit=False)
                item.user = request.user if request.user.is_authenticated else None
                item.save()
                return redirect("feedback_thanks")
    else:
        form = FeedbackForm(initial=initial_category(request), user=request.user)

    return render(request, "landing/feedback.html", {"form": form})


def feedback_thanks(request):
    return render(request, "landing/feedback_thanks.html")


# ---------- Dashboard (logged in) ----------

@login_required
def dashboard_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, "Thanks for helping shape the product. Your feedback has been received.")
            return redirect("dashboard_feedback")
    else:
        form = FeedbackForm(initial=initial_category(request), user=request.user)

    return render(request, "dashboard/feedback.html", {"form": form})


@login_required
def dashboard_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.category = Feedback.Category.CONTACT
            item.name = request.user.get_full_name() or request.user.username
            item.save()
            messages.success(request, "Message sent. Replies go to the email address you provided.")
            return redirect("dashboard_contact")
    else:
        form = ContactForm(user=request.user)

    return render(request, "dashboard/contact.html", {
        "form": form,
        "contact_email": settings.CONTACT_EMAIL,
        "contact_github": settings.CONTACT_GITHUB,
    })