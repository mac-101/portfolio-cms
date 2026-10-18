from django.db import migrations


def copy_account_email(apps, schema_editor):
    Portfolio = apps.get_model("portfolio", "Portfolio")
    database = schema_editor.connection.alias
    portfolios = (
        Portfolio.objects.using(database)
        .select_related("owner")
        .filter(email="")
        .iterator()
    )

    for portfolio in portfolios:
        if portfolio.owner.email:
            Portfolio.objects.using(database).filter(pk=portfolio.pk).update(
                email=portfolio.owner.email
            )


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0007_allow_null_portfolio_category"),
    ]

    operations = [
        migrations.RunPython(copy_account_email, migrations.RunPython.noop),
    ]
