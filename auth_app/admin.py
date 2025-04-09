from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
   
    readonly_fields = ('last_login', 'date_joined')
    exclude = ('username',)

    fieldsets = (
        ('Dados de Acesso', {
            'fields': ('email', 'password', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Informações Pessoais', {
            'fields': (
                'foto_profile',
                ('first_name', 'last_name'),
                'data_nascimento',
                ('endereco', 'numero_endereco'),
                ('complemento', 'cidade'),
                'estado',
                ('telefone', 'whatsapp'),
            )
        }),
        ('Permissões', {
            'fields': ('groups', 'user_permissions')
        }),
        ('Atividades', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Informações Pessoais', {
            'fields': (
                'foto_profile',
                ('first_name', 'last_name'),
                'data_nascimento',
                ('endereco', 'numero_endereco'),
                ('complemento', 'cidade'),
                'estado',
                ('telefone', 'whatsapp'),
            )
        }),
        ('Permissões', {
            'fields': ('groups', 'user_permissions')
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.site_header = 'Administração de Usuários'
