from django.contrib.auth import get_user_model
from django.utils.text import slugify


def username_for_full_name(full_name, user=None):
    base = slugify(full_name, allow_unicode=True).replace("-", "_")[:150].strip("_")
    if not base:
        return ""

    username = base
    suffix = 2
    users = get_user_model().objects.all()
    if user and user.pk:
        users = users.exclude(pk=user.pk)
    while users.filter(username=username).exists():
        suffix_text = f"_{suffix}"
        username = f"{base[:150 - len(suffix_text)]}{suffix_text}"
        suffix += 1
    return username
