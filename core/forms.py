from django import forms
from .models import Task, Note
from django.contrib.auth import get_user_model

User = get_user_model()
    # declares global variable User in forms.py

class NewTaskForm(forms.Form):
    task = forms.CharField(label='Task', max_length=512, widget=forms.TextInput(attrs={'placeholder': 'add a new task'}))

    def save(self, **kwargs):
        if self.is_valid():
            task_props = {'description': self.cleaned_data['task']}
            task_props.update(kwargs)
            return Task.objects.create(**task_props)
        return None

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['text']

