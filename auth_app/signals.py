from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.dispatch import receiver

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        # Adicionando o primeiro e o último nome ao criar o superusuário
        User.objects.create_superuser(
            email="admin@teste.com",
            password="123456",
            first_name="Admininstrador",  # Adicionando o nome
        )


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    # Cria o grupo 'Nome do Grupo' se ele não existir após a migração
    Group.objects.get_or_create(name='full_access')
    Group.objects.get_or_create(name='basic')