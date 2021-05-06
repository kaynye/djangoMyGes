from django import forms
from .models import Note


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