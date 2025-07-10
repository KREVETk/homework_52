from django import forms
from .models import Issue, Status, Type


class IssueForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label="Статус",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        label="Тип задачи",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'type']
        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }











