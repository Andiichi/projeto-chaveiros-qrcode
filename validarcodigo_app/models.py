from django.db import models
from django.contrib.auth.models import  Group
from django.conf import settings 
import uuid

class CodigoSecreto(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Define automaticamente a data de criação
    used_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="secret_codes")  # Usuário que gerou o código

    class Meta:
        verbose_name = "Codigo Secreto"
        verbose_name_plural = "Codigos Secretos"

    def __str__(self):
        return f"{self.code} - {self.group.name} - {'Usado' if self.used else 'Disponível'}"
