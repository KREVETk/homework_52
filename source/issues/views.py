from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import Issue
from .forms import IssueForm

class IssueCreateView(CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/issue_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.type_temp.set(form.cleaned_data['type_temp'])
        return response

    def get_success_url(self):
        return reverse_lazy('issue_detail', kwargs={'pk': self.object.pk})


class IssueUpdateView(UpdateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/issue_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.type_temp.set(form.cleaned_data['type_temp'])
        return response

    def get_success_url(self):
        return reverse_lazy('issue_detail', kwargs={'pk': self.object.pk})
