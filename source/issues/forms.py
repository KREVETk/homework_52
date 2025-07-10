from django import forms
from .models import Issue, Status, Type

class IssueForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label="Статус",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    type_temp = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        label="Тип задачи",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'type_temp']
        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }





