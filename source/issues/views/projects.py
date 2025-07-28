from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView, ListView
)
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from issues.models import Project
from issues.forms import ProjectForm, ProjectMembersForm


class ProjectListView(ListView):
    model = Project
    template_name = 'issues/projects/project_list.html'  # папка projects
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        if not context['object_list']:
            context['no_results'] = True
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'issues/projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = self.object.issues.filter(is_deleted=False)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'issues/projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_type': 'Проект',
            'cancel_url': reverse('project_list'),
        })
        return context


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'issues/projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        user = self.request.user
        project = self.get_object()
        return user.groups.filter(name='Project Manager').exists() and user in project.members.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_type': 'Проект',
            'object_name': self.object.name,
            'cancel_url': reverse('project_detail', args=[self.object.pk]),
        })
        return context


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        user = self.request.user
        project = self.get_object()
        return user.groups.filter(name='Project Manager').exists() and user in project.members.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_type': 'Проект',
            'object_name': self.object.name,
            'cancel_url': reverse('project_detail', args=[self.object.pk]),
        })
        return context


class ProjectMembersUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectMembersForm
    template_name = 'issues/projects/project_members_form.html'

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        user = self.request.user
        project = self.get_object()
        return user in project.members.all() and user.groups.filter(name__in=['Project Manager', 'Team Lead']).exists()
