from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView, ListView)
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Issue, Project
from .forms import IssueForm, ProjectForm


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
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
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = self.object.issues.all()
        return context


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Проект'
        context['cancel_url'] = reverse('project_list')
        return context


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Проект'
        context['object_name'] = self.object.name
        context['cancel_url'] = reverse('project_detail', args=[self.object.pk])
        return context


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Проект'
        context['object_name'] = self.object.name
        context['cancel_url'] = reverse('project_detail', args=[self.object.pk])
        return context


### ============ Issue Views ==========

class IssueListView(ListView):
    model = Issue
    template_name = 'issues/project_list.html'
    context_object_name = 'issues'


class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issues/project_detail.html'
    context_object_name = 'issue'


class IssueDeleteView(DeleteView):
    model = Issue
    template_name = 'issues/confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Задача'
        context['object_name'] = self.object.summary
        context['cancel_url'] = reverse('issue_detail', args=[self.object.pk])
        return context


class IssueCreateInProjectView(CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/project_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        response = super().form_valid(form)
        form.instance.type_temp.set(form.cleaned_data['type_temp'])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        context['object_type'] = 'Задача'
        context['cancel_url'] = reverse('project_detail', args=[self.project.pk])
        return context

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.project.pk})


class IssueUpdateView(UpdateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/project_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.type_temp.set(form.cleaned_data['type_temp'])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_type'] = 'Задача'
        context['object_name'] = self.object.summary
        context['cancel_url'] = reverse('issue_detail', args=[self.object.pk])
        return context

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})
