# from django.db import models
# from django.contrib.auth.models import User, Group
# import uuid


# class CodigoSecreto(models.Model):
#     code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     used = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True, editable=False)
#     used_at = models.DateTimeField(null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=False, blank=False)
    
#     def __str__(self):
#         return f"{self.code} - {self.group.name} - {'Usado' if self.used else 'Disponível'}"


from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from django.utils import timezone

class CodigoSecreto(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Define automaticamente a data de criação
    used_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuário que gerou o código

    def __str__(self):
        return f"{self.code} - {self.group.name} - {'Usado' if self.used else 'Disponível'}"
