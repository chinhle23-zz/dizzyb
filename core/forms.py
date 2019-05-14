from django import forms
from .models import Task, Note
from django.contrib.auth import get_user_model, authenticate, password_validation
from registration.forms import RegistrationForm

User = get_user_model()
    # declares global variable User in forms.py

class BetterDateInput(forms.DateInput):
    input_type = 'date'

class CustomRegistrationForm(RegistrationForm):
    # https://github.com/macropin/django-registration/blob/master/registration/forms.py
    # https://github.com/django/django/blob/master/django/contrib/auth/forms.py

    email = forms.EmailField(
        label='E-mail', 
        widget=forms.TextInput(attrs={'class': ''}),
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': ''}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': ''}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = None

    class Meta(RegistrationForm.Meta): # Meta is a class defined in a class
        
        widgets = {
            'username': forms.TextInput(attrs={'class': ''}),
        }
        
class NewTaskForm(forms.Form):
    task = forms.CharField(label='Task', max_length=512, widget=forms.TextInput(attrs={
        'placeholder': 'add a new task',
        }))

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

class EditTaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = None

    class Meta:
        model = Task
        # fields = ['description', 'due_on', 'show_on']
        fields = ['description', 'show_on']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'w-100 mv2 pa2 f4'}),
            # 'due_on': BetterDateInput(attrs={'class': 'w-100 mv2 pa2'}),
            'show_on': BetterDateInput(attrs={'class': 'w-100 mv2 pa2'})
        }