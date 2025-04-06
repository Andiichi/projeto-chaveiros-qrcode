from django import forms
from django.forms import modelformset_factory
from .models import PhoneNumber

class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ['number']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone ou WhatsApp'}),
        }

# Aqui criamos o FormSet
PhoneNumberFormSet = modelformset_factory(
    PhoneNumber,             # Modelo que será usado
    form=PhoneNumberForm,    # Formulário que define os campos
    extra=1,                 # Um campo em branco adicional para novo número
    can_delete=True          # Permite que o usuário remova números existentes
)
