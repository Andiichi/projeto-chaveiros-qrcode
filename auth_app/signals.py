from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import date
from .models import User  # Se preferir pode usar get_user_model()


# Criando o usuario superadmin
@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            email='admin@teste.com',
            password='123456',
            first_name='Admininstrador',
            last_name='Master',
            data_nascimento=date(1992, 11, 22)  # ← Esse campo é necessário // formato yyyy-mm-dd
        )

# Usuario 1
@receiver(post_save, sender=User)
def usuario_comum_pos_criacao(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        # Aqui você pode colocar ações específicas para novos usuários
        User.objects.create_user(
            email='user1@teste.com',
            password='123456',  # ← Senha padrão, você pode mudar isso
            first_name='Andreia',
            last_name=instance.last_name,
            data_nascimento=date(1990, 11, 22),  # ← Esse campo é necessário // formato yyyy-mm-dd
            endereco=instance.endereco,
            numero_endereco=instance.numero_endereco,
            complemento=instance.complemento,
            cidade=instance.cidade,
            estado=instance.estado,
            telefone=instance.telefone,
            whatsapp=instance.whatsapp
        )

        # Exemplo: Adicionar a um grupo padrão
        grupo_padrao, _ = Group.objects.get_or_create(name='full_access')
        instance.groups.add(grupo_padrao)

        # Ou definir alguma lógica especial
        # instance.algum_campo = algo
        # instance.save()


# Usuario 2
@receiver(post_save, sender=User)
def usuario_comum_pos_criacao(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
         # Aqui você pode colocar ações específicas para novos usuários
        User.objects.create_user(
            email='user2@teste.com',
            password='123456',  # ← Senha padrão, você pode mudar isso
            first_name='Roberto',
            last_name=instance.last_name,
            data_nascimento=date(1995, 11, 22),  # ← Esse campo é necessário // formato yyyy-mm-dd
            endereco=instance.endereco,
            numero_endereco=instance.numero_endereco,
            complemento=instance.complemento,
            cidade=instance.cidade,
            estado=instance.estado,
            telefone=instance.telefone,
            whatsapp=instance.whatsapp
        )

        # Exemplo: Adicionar a um grupo padrão
        grupo_padrao, _ = Group.objects.get_or_create(name='basic')
        instance.groups.add(grupo_padrao)

        # Ou definir alguma lógica especial
        # instance.algum_campo = algo
        # instance.save()


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    # Cria o grupo 'Nome do Grupo' se ele não existir após a migração
    Group.objects.get_or_create(name='full_access')
    Group.objects.get_or_create(name='basic')