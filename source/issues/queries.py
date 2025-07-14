from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, Count

from issues import models
from issues.models import Issue, Type


# 1
one_month_ago = timezone.now() - timedelta(days=30)
Issue.objects.filter(updated_at__gte=one_month_ago, status__name__iexact='Закрыта')


# 2
Issue.objects.filter(
    status__name__in=['Открыта', 'В процессе'],
    type_temp__name__in=['Баг', 'Фича']
).distinct()


# 3
Issue.objects.filter(
    Q(status__name__iexact='Открыта') & (
        Q(summary__icontains='bug') | Q(type_temp__name__iexact='Баг')
    )
).distinct()



# bonus 1
Issue.objects.values(
    'id', 'summary', 'status__name', 'type_temp__name'
).distinct()


# bonus 2
Issue.objects.filter(summary=models.F('description'))


# bonus 3
Type.objects.annotate(issue_count=Count('issues_temp')).values('name', 'issue_count')
