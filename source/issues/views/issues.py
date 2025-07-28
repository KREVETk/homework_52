from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from issues.models import Issue, Project
from issues.forms import IssueForm


class IssueListView(ListView):
    model = Issue
    template_name = 'issues/issues/issue_list.html'  # папка issues/issues
    context_object_name = 'issues'

    def get_queryset(self):
        return Issue.objects.filter(is_deleted=False)


class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issues/issues/issue_detail.html'
    context_object_name = 'issue'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Задача удалена.")
        return obj


class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def test_func(self):
        user = self.request.user
        issue = self.get_object()
        return (
            user.groups.filter(name__in=['Project Manager', 'Team Lead']).exists()
            and user in issue.project.members.all()
        )

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return super().form_valid(form=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_type': 'Задача',
            'object_name': self.object.summary,
            'cancel_url': reverse('issue_detail', args=[self.object.pk])
        })
        return context


class IssueCreateInProjectView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/issues/issue_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        user = self.request.user
        return (
            user.groups.filter(name__in=['Project Manager', 'Team Lead', 'Developer']).exists()
            and user in self.project.members.all()
        )

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project': self.project,
            'object_type': 'Задача',
            'cancel_url': reverse('project_detail', args=[self.project.pk])
        })
        return context

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.project.pk})


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/issues/issue_form.html'  # поправлено

    def test_func(self):
        user = self.request.user
        issue = self.get_object()
        return (
            user.groups.filter(name__in=['Project Manager', 'Team Lead', 'Developer']).exists()
            and user in issue.project.members.all()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'object_type': 'Задача',
            'object_name': self.object.summary,
            'cancel_url': reverse('issue_detail', args=[self.object.pk])
        })
        return context

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})
