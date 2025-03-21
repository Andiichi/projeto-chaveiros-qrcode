from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PhoneNumber

# Inline para exibir os números de telefone dentro do UserAdmin
class PhoneNumberInline(admin.TabularInline):  # Ou admin.StackedInline para exibição vertical
    model = PhoneNumber
    extra = 1  # Define quantos campos extras aparecem ao editar um usuário
    min_num = 1  # Define mínimo de telefones
    max_num = 3  # Define máximo de telefones permitido (opcional)

class CustomUserAdmin(UserAdmin):
    """Admin personalizado para o modelo User"""

    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff')  # Adicionando o campo 'photo' ao list_display
    search_fields = ('email', 'first_name')
    ordering = ('email',)
    readonly_fields = ('first_name', 'last_name', 'email', 'data_nascimento')  # Remova 'username' se não existir

    fieldsets = (
        ('Dados de acesso', {'fields': ('email', 'password', 'is_active')}),
        ('Dados pessoais', {'fields': ('foto_profile', 'first_name', 'last_name', 'data_nascimento', 'endereco')}),  # Adicionando o campo 'photo' aqui
        ('Grupos', {'fields': ('groups',)}),
        ('Ultimo login e cadastro', {'fields': ('last_login', 'date_joined')}),
    )
    
    inlines = [PhoneNumberInline]  # Adiciona o inline para exibir números de telefone

admin.site.register(User, CustomUserAdmin)