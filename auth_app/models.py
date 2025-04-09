from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import date
from django.utils import timezone

# Gerenciador personalizado para User
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
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

    foto_profile = models.ImageField(upload_to='fotos_perfis/', blank=True, null=True)  # Foto de perfil
    email = models.EmailField(unique=True)  # Login via e-mail
    endereco = models.CharField(max_length=30, blank=True)
    numero_endereco = models.CharField(max_length=10, blank=True, verbose_name='numero')
    complemento = models.CharField(max_length=30, blank=True)
    cidade = models.CharField(max_length=30, blank=True)
    estado = models.CharField(max_length=2, choices=CHOICES_UF, blank=True, verbose_name='uf')
    telefone = models.CharField(max_length=15, blank=True, verbose_name='telefone_chaveiro')
    whatsapp = models.CharField(max_length=15, blank=True, verbose_name='whatsapp_chaveiro')
    data_nascimento = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

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


    username = None  # Remove o campo username

    USERNAME_FIELD = 'email'  # Define o login via email
    REQUIRED_FIELDS = []  # Nenhum campo obrigatório além do email

    objects = UserManager()  # Definindo o UserManager personalizado

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'
