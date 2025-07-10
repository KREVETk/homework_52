from django.db import models


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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.summary
