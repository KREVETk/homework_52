from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название статуса')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название типа')

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class Project(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    members = models.ManyToManyField(
        User,
        related_name='projects',
        verbose_name='Участники проекта',
        blank=True,
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name



class Issue(models.Model):
    summary = models.CharField(max_length=200, verbose_name='Краткое описание')
    description = models.TextField(blank=True, verbose_name='Полное описание')
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )
    type_temp = models.ManyToManyField(
        Type,
        verbose_name='Тип (новый)',
        related_name='issues_temp'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='issues'
    )

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.summary
