from django.urls import path
from .views import (task_list, task_add, task_edit, task_delete, task_detail, task_bulk_delete)

urlpatterns = [
    path('', task_list, name='task_list'),
    path('add/', task_add, name='task_add'),
    path('<int:pk>/edit/', task_edit, name='task_edit'),
    path('<int:pk>/delete/', task_delete, name='task_delete'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('bulk-delete/', task_bulk_delete, name='task_bulk_delete'),
]
