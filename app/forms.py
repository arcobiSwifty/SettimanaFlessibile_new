from django import forms
from .models import Corso, Utente

class CreaCorso(forms.ModelForm):

    class Meta:
        model = Corso
        fields = ('nome', 'is_progressive', 'categoria')


        #implement manually: ospitanti, creatore, fasce
        #implement manually: add hosted_cour
