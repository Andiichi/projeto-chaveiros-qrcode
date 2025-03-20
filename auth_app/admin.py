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
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'data_nascimento')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'bio', 'endereco')
    ordering = ('email',)
    
    fieldsets = (
        ("Informações Pessoais", {"fields": ("email", "first_name", "last_name", "password", "foto_profile", "bio", "endereco", "data_nascimento")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            "Criar Novo Usuário",
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2", "foto_profile", "bio", "endereco", "data_nascimento"),
            },
        ),
    )

    inlines = [PhoneNumberInline]  # Adiciona o inline para exibir números de telefone

admin.site.register(User, CustomUserAdmin)