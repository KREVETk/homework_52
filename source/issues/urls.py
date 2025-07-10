from django.urls import path
from .views import (
    IssueListView, IssueDetailView, IssueCreateView, IssueUpdateView, IssueDeleteView)

urlpatterns = [
    path('', IssueListView.as_view(), name='issue_list'),
    path('<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),
    path('add/', IssueCreateView.as_view(), name='issue_add'),
    path('<int:pk>/edit/', IssueUpdateView.as_view(), name='issue_edit'),
    path('<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete')
]
