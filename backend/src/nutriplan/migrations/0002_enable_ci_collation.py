from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "nutriplan",
            "0001_initial",
        )
    ]
    operations = [
        migrations.RunSQL(
            "CREATE COLLATION IF NOT EXISTS case_insensitive "
            "(provider = icu, locale = 'und-u-ks-level2', deterministic = false);"
        ),
    ]
