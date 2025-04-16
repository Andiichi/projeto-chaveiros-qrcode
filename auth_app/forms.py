from django import forms
from .models import User

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['estado', 'cidade', 'endereco', 'numero_endereco', 'complemento']  # Ajuste os campos conforme necessário
        widgets = {
            'estado': forms.Select(choices=User.CHOICES_UF, attrs={'class': 'form-select'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            # outros widgets
        }
