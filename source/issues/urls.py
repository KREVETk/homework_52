from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView,
    ProjectDeleteView, IssueCreateInProjectView, IssueDetailView, IssueUpdateView, IssueDeleteView)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('projects/add/', ProjectCreateView.as_view(), name='project_add'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/<int:project_pk>/issues/add/', IssueCreateInProjectView.as_view(), name='issue_add'),
    path('projects/<int:pk>/members/', ProjectMembersUpdateView.as_view(), name='project_members'),


    path('issues/<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),
    path('issues/<int:pk>/edit/', IssueUpdateView.as_view(), name='issue_edit'),
    path('issues/<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete')
]