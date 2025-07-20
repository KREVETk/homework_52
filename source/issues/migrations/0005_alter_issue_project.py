from django.db import migrations

def set_default_project(apps, schema_editor):
    Project = apps.get_model('issues', 'Project')
    Issue = apps.get_model('issues', 'Issue')

    project = Project.objects.create(
        name='Тестовый проект',
        description='Создан для уже существующих задач',
        start_date='2024-01-01',
        end_date=None,
    )

    for issue in Issue.objects.filter(project__isnull=True):
        issue.project = project
        issue.save()


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0004_auto_20250719_0955'),
    ]

    operations = [
        migrations.RunPython(set_default_project),
    ]
