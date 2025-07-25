# Generated by Django 5.2.3 on 2025-07-21 15:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0005_alter_issue_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='issues.project'),
        ),
    ]
