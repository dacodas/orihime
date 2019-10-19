from django.db import migrations

def seed_search_sources(apps, schema_editor):

    search_backends = [
        "goo辞書",
        "Larousse"
        ]

    Source = apps.get_model('orihime', 'Source')

    for name in search_backends:

        Source(name=name).save()

class Migration(migrations.Migration):

    dependencies = [
            ('orihime', '0001_initial')
            ]
    operations = [
        migrations.RunPython(seed_search_sources),
    ]
