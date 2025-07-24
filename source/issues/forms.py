from django import forms
from .models import Issue, Status, Type, Project
from .validators import validate_summary_length, validate_forbidden_words


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
        widget=forms.CheckboxSelectMultiple()
    )

    summary = forms.CharField(
        validators=[validate_summary_length],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Краткое описание'
    )

    description = forms.CharField(
        required=False,
        validators=[validate_forbidden_words],
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Полное описание'
    )

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'project', 'status', 'types']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


