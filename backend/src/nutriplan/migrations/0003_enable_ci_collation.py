from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "nutriplan",
            "0002_alter_customuser_managers_remove_customuser_username_and_more",
        )
    ]
    operations = [
        migrations.RunSQL(
            "CREATE COLLATION IF NOT EXISTS case_insensitive "
            "(provider = icu, locale = 'und-u-ks-level2', deterministic = false);"
        ),
    ]
