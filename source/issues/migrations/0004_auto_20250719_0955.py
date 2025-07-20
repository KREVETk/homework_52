from django.db import migrations

def create_default_project(apps, schema_editor):
    Project = apps.get_model('issues', 'Project')
    Issue = apps.get_model('issues', 'Issue')
    default_project = Project.objects.create(
        name="Тестовый проект",
        description="Создан для связывания существующих задач",
        start_date="2024-01-01"
    )
    for issue in Issue.objects.all():
        issue.project = default_project
        issue.save()

class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0003_project_issue_project'),
    ]

    operations = [
        migrations.RunPython(create_default_project),
    ]
