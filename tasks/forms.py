from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "contact", "company", "due_date", "type", "priority", "status"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
