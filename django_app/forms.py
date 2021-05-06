from django import forms
from .models import Note
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group

class NoteForm(forms.ModelForm):
  
    # create meta class
    class Meta:
        # specify model to be used
        model = Note
  
        # specify fields to be used
        fields = [
            "n_note",
            "n_type",
            "n_matiere",
            "n_eleve",
        ]

class EditUserForm(UserChangeForm):
    groups_choices = ((gr.id, gr.name) for gr in Group.objects.all())
    
    groups = forms.ChoiceField(choices = groups_choices)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'groups', 'is_staff' )


# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )