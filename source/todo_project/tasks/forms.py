from django import forms

from .models import Task

class TaskForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES)
    due_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Task
        fields = ['description', 'status', 'due_date']
