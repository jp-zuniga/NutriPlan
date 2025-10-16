from django.db import migrations


def forwards(apps, schema_editor) -> None:
    Recipe = apps.get_model("nutriplan", "Recipe")
    for r in Recipe.objects.exclude(category__isnull=True).iterator():
        r.categories.add(r.category_id)


class Migration(migrations.Migration):
    dependencies = [
        ("nutriplan", "0004_recipe_categories"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
