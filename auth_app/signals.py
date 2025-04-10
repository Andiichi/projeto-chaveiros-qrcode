from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import date

User = get_user_model()

# Cria os grupos uma única vez após as migrações
@receiver(post_migrate)
def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name='full_access')
    Group.objects.get_or_create(name='basic')


# Cria o superusuário se não existir
@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            email='admin@teste.com',
            password='123456',
            first_name='Administrador',
            last_name='Master',
            data_nascimento=date(1992, 11, 22)
        )


# Cria os usuários padrão (Andreia e Roberto) após as migrações
@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    if not User.objects.filter(email='user1@teste.com').exists():
        user1 = User.objects.create_user(
            email='user1@teste.com',
            password='123456',
            first_name='Andreia',
            last_name='da Silva',
            data_nascimento=date(1990, 11, 22),
            endereco='Rua A',
            numero_endereco='100',
            complemento='Apto 1',
            cidade='Cidade X',
            estado='Estado Y',
            telefone='11999999999',
            whatsapp='11999999999'
        )
        grupo1, _ = Group.objects.get_or_create(name='full_access')
        user1.groups.add(grupo1)

    if not User.objects.filter(email='user2@teste.com').exists():
        user2 = User.objects.create_user(
            email='user2@teste.com',
            password='123456',
            first_name='Roberto',
            last_name='dos Santos',
            data_nascimento=date(1995, 11, 22),
            endereco='Rua B',
            numero_endereco='200',
            complemento='Casa',
            cidade='Cidade Y',
            estado='Estado Z',
            telefone='11888888888',
            whatsapp='11888888888'
        )
        grupo2, _ = Group.objects.get_or_create(name='basic')
        user2.groups.add(grupo2)
