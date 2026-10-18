from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0006_service_tech_stack"),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE "portfolio_portfolio" ALTER COLUMN "category" DROP NOT NULL',
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
