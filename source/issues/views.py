from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView, ListView)
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .models import Issue, Project
from .forms import IssueForm, ProjectForm, ProjectMembersForm


class ProjectListView(ListView):
    model = Project
    template_name = 'issues/project_list.html'
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
    template_name = 'issues/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = self.object.issues.filter(is_deleted=False)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'issues/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Проект'
        context['cancel_url'] = reverse('project_list')
        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'issues/project_form.html'
    success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Проект'
        context['object_name'] = self.object.name
        context['cancel_url'] = reverse('project_detail', args=[self.object.pk])
        return context


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'issues/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Проект'
        context['object_name'] = self.object.name
        context['cancel_url'] = reverse('project_detail', args=[self.object.pk])
        return context


class ProjectMembersUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectMembersForm
    template_name = 'issues/project_members_form.html'

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        project = self.get_object()
        user = self.request.user

        if user in project.members.all():
            if user.groups.filter(name__in=['Project Manager', 'Team Lead']).exists():
                return True
        return False


### ============ Issue Views ==========

class IssueListView(ListView):
    model = Issue
    template_name = 'issues/project_list.html'
    context_object_name = 'issues'

    def get_queryset(self):
        return Issue.objects.filter(is_deleted=False)


class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issues/project_detail.html'
    context_object_name = 'issue'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Задача удалена.")
        return obj


class IssueDeleteView(LoginRequiredMixin, DeleteView):
    model = Issue
    template_name = 'issues/confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return super().form_valid(form=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Задача'
        context['object_name'] = self.object.summary
        context['cancel_url'] = reverse('issue_detail', args=[self.object.pk])
        return context


class IssueCreateInProjectView(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/project_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        context['object_type'] = 'Задача'
        context['cancel_url'] = reverse('project_detail', args=[self.project.pk])
        return context

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.project.pk})


class IssueUpdateView(LoginRequiredMixin, UpdateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/project_form.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Задача'
        context['object_name'] = self.object.summary
        context['cancel_url'] = reverse('issue_detail', args=[self.object.pk])
        return context

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})