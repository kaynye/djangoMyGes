from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django_app.models import *

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

class MatiereCreationForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['m_name', 'm_description', 'm_coefficient', 'm_profs', 'm_classroom']

class EditMatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['m_name', 'm_description', 'm_coefficient', 'm_evenement', 'm_profs', 'm_classroom']

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['e_name', 'e_date_debut', 'e_date_fin', 'e_frequent', 'e_is_presenciel', 'e_commentaire']

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['e_name', 'e_date_debut', 'e_date_fin', 'e_frequent', 'e_is_presenciel', 'e_commentaire', 'e_class']
        
class ClassroomCreationForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['c_name', 'c_promotion']

class EditClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['c_name', 'c_student', 'c_promotion']
                
class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ('pu_picture', )
