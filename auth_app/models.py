from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


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
    email = models.EmailField(unique=True)  # Login via e-mail
    foto_profile = models.ImageField(upload_to='user_photos/', blank=True, null=True)  # Foto de perfil
    bio = models.TextField(max_length=500, blank=True)
    endereco = models.CharField(max_length=30, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    username = None  # Remove o campo username

    USERNAME_FIELD = 'email'  # Define o login via email
    REQUIRED_FIELDS = []  # Nenhum campo obrigatório além do email

    objects = UserManager()  # Definindo o UserManager personalizado

    def __str__(self):
        return self.email
    

class PhoneNumber(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="phones")
    number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.number}"