from django.db import models
from auth_app.models import User
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from django.conf import settings


class DadosObrigatorios(models.Model):
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dados_obrigatorios')
    nome_chaveiro = models.CharField(max_length=100, null=False, blank=False)
    sobrenome_chaveiro = models.CharField(max_length=100, null=False, blank=False)
    telefone_chaveiro = models.CharField(max_length=15, blank=True)
    whatsapp_chaveiro = models.CharField(max_length=15, blank=True)
    data_nascimento_chaveiro = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    idade_chaveiro = models.PositiveIntegerField(blank=True, null=True, editable=False) # Esse será preenchido automaticamente

    def calcular_idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento_chaveiro.year - (
            (hoje.month, hoje.day) < (self.data_nascimento_chaveiro.month, self.data_nascimento_chaveiro.day)
        )

    def save(self, *args, **kwargs):
        if self.data_nascimento_chaveiro:
            self.idade_chaveiro = self.calcular_idade()
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
        ('AC', 'Acre '),
        ('AL', 'Alagoas '),
        ('AP', 'Amapá '),
        ('AM', 'Amazonas '),
        ('BA', 'Bahia '),
        ('CE', 'Ceará '),
        ('DF', 'Distrito Federal '),
        ('ES', 'Espírito Santo '),
        ('GO', 'Goiás '),
        ('MA', 'Maranhão '),
        ('MT', 'Mato Grosso '),
        ('MS', 'Mato Grosso do Sul '),
        ('MG', 'Minas Gerais '),
        ('PA', 'Pará '),
        ('PB', 'Paraíba '),
        ('PR', 'Paraná '),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí '),
        ('RJ', 'Rio de Janeiro '),
        ('RN', 'Rio Grande do Norte '),
        ('RS', 'Rio Grande do Sul '),
        ('RO', 'Rondônia '),
        ('RR', 'Roraima '),
        ('SC', 'Santa Catarina' ),
        ('SP', 'São Paulo '),
        ('SE', 'Sergipe '),
        ('TO', 'Tocantins '),
    )

    dados_obrigatorios = models.OneToOneField(DadosObrigatorios, on_delete=models.CASCADE, related_name='dados_opcionais')
    foto_chaveiros = models.ImageField(upload_to='fotos_chaveiros/', blank=True, null=True) 
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

    def __str__(self):
        return f'{self.dados_obrigatorios.nome_chaveiro} {self.dados_obrigatorios.sobrenome_chaveiro}'
