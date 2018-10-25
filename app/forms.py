from django import forms
from .models import Corso, Utente

class CreaCorso(forms.ModelForm):

    class Meta:
        model = Corso
        fields = ('nome', 'is_progressive', 'descrizione', 'aula', 'categoria')

        widgets = {
            'descrizione': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'descrivi il tuo corso'}),
        }

        labels = {
            'is_progressive': 'progressivo',
        }

        #implement manually: ospitanti, creatore, fasce
        #implement manually: add hosted_cour
