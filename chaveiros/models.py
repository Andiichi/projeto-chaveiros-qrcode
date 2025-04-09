from django.db import models
from auth_app.models import User
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from django.conf import settings


class DadosObrigatorios(models.Model):
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dados_obrigatorios')
    nome = models.CharField(max_length=100, null=False, blank=False)
    sobrenome = models.CharField(max_length=100, null=False, blank=False)
    telefone = models.CharField(max_length=15, blank=True, verbose_name='telefone_chaveiro')
    whatsapp = models.CharField(max_length=15, blank=True, verbose_name='whatsapp_chaveiro')
    data_nascimento = models.DateField(null=False, blank=False)

    idade = models.PositiveIntegerField(blank=True, null=True, editable=False) # Esse será preenchido automaticamente

    def calcular_idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    def save(self, *args, **kwargs):
        if self.data_nascimento:
            self.idade = self.calcular_idade()
        super().save(*args, **kwargs)

class DadosOpcionais(models.Model):

    CHOICES_SANGUINEOS = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    CHOICES_UF = (
        ('AC', 'Acre (AC)'),
        ('AL', 'Alagoas (AL)'),
        ('AP', 'Amapá (AP)'),
        ('AM', 'Amazonas (AM)'),
        ('BA', 'Bahia (BA)'),
        ('CE', 'Ceará (CE)'),
        ('DF', 'Distrito Federal (DF)'),
        ('ES', 'Espírito Santo (ES)'),
        ('GO', 'Goiás (GO)'),
        ('MA', 'Maranhão (MA)'),
        ('MT', 'Mato Grosso (MT)'),
        ('MS', 'Mato Grosso do Sul (MS)'),
        ('MG', 'Minas Gerais (MG)'),
        ('PA', 'Pará (PA)'),
        ('PB', 'Paraíba (PB)'),
        ('PR', 'Paraná (PR)'),
        ('PE', 'Pernambuco (PE)'),
        ('PI', 'Piauí (PI)'),
        ('RJ', 'Rio de Janeiro (RJ)'),
        ('RN', 'Rio Grande do Norte (RN)'),
        ('RS', 'Rio Grande do Sul (RS)'),
        ('RO', 'Rondônia (RO)'),
        ('RR', 'Roraima (RR)'),
        ('SC', 'Santa Catarina (SC)'),
        ('SP', 'São Paulo (SP)'),
        ('SE', 'Sergipe (SE)'),
        ('TO', 'Tocantins (TO)'),
    )

    dados_obrigatorios = models.OneToOneField(DadosObrigatorios, on_delete=models.CASCADE, related_name='dados_opcionais')
    endereco = models.CharField(max_length=30, blank=True)
    numero_endereco = models.CharField(max_length=10, blank=True, verbose_name='numero')
    complemento = models.CharField(max_length=30, blank=True)
    cidade = models.CharField(max_length=30, blank=True)
    estado = models.CharField(max_length=2, choices=CHOICES_UF, blank=True, verbose_name='uf')
    email = models.EmailField(unique=True)
    tipo_sanguineo = models.CharField(max_length=3, choices=CHOICES_SANGUINEOS, blank=True,verbose_name='sangue')
    alergias_intolerancias = models.TextField(blank=True)
    medicamentos = models.TextField(blank=True)
    link_whatsapp = models.URLField(blank=True, verbose_name='link-whats')
    links_outros = models.URLField(blank=True, verbose_name='link-outros')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.dados_obrigatorios.nome} {self.dados_obrigatorios.sobrenome}'
