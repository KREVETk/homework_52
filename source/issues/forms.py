from django import forms
from .models import Issue, Status, Type, Project

class IssueForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        label="Проект",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label="Статус",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    types = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        label="Тип задачи",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'project', 'status', 'types']
        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
