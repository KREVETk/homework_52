from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, Count, F

from issues.models import Issue, Type

# 1. Закрытые задачи за последний месяц
one_month_ago = timezone.now() - timedelta(days=30)
Issue.objects.filter(updated_at__gte=one_month_ago, status__name__iexact='Done')

# 2. Задачи со статусами 'New' или 'In Progress' и типами 'Bug' или 'Enhancement'
Issue.objects.filter(
    status__name__in=['New', 'In Progress'],
    type_temp__name__in=['Bug', 'Enhancement']
).distinct()

# 3. Не закрытые задачи
Issue.objects.filter(
    ~Q(status__name__iexact='Done') & (
        Q(summary__icontains='ошибка') | Q(type_temp__name__iexact='Bug')
    )
).distinct()

# bonus 1
Issue.objects.values(
    'id', 'summary', 'status__name', 'type_temp__name'
).distinct()

# bonus 2
Issue.objects.filter(summary=F('description'))

# bonus 3
Type.objects.annotate(issue_count=Count('issues_temp')).values('name', 'issue_count')
