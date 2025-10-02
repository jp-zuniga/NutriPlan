from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("nutriplan", "0002_enable_ci_collation")]
    operations = [migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS pg_trgm;")]
