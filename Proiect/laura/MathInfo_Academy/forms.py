

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User        
        fields = UserCreationForm.Meta.fields + ('email','first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-control-lg bg-light fs-6', "placeholder": str(field.label)})

    def as_p(self):
        return ''.join(f'<div class="input-group mb-3">{field}</div>' for field in self)