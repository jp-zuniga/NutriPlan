from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("nutriplan", "0004_enable_pg_trgm")]
    operations = [
        TrigramExtension(),
        UnaccentExtension(),
    ]
