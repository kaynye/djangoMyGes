from django import forms
from .models import ProfileUser

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ('pu_picture', )