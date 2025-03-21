from django.contrib import admin
from django.utils import timezone
from .models import CodigoSecreto

class CodigoSecretoAdmin(admin.ModelAdmin):
    list_display = ('code_display', 'group_display', 'user_display', 'created_at_display', 'used', 'used_at_display')
    readonly_fields = ('code_display', 'group_display', 'created_at_display', 'used_at', 'used')  # Mantido como readonly
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('code_display', 'group')}),  # Removido created_at
    )

    def get_changeform_initial_data(self, request):
        return {
            'user': request.user,
        }

    def save_model(self, request, obj, form, change):
        if obj.used and obj.used_at is None:
            obj.used_at = timezone.now()
        elif not obj.used:
            obj.used_at = None

        if not obj.pk:
            obj.user = request.user

        super().save_model(request, obj, form, change)

    # Métodos de exibição no Admin
    @admin.display(description="Código Secreto")
    def code_display(self, obj):
        return obj.code 

    @admin.display(description="Grupo")
    def group_display(self, obj):
        return obj.group.name if obj.group else None
    
    @admin.display(description="Nome do Criador")
    def user_display(self, obj):
        return obj.user.get_full_name() if obj.user else "Usuário não definido"

    @admin.display(description="Criado em")
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M') if obj.created_at else "Desconhecido"

    @admin.display(description="Data de Uso")
    def used_at_display(self, obj):
        return obj.used_at.strftime('%d/%m/%Y %H:%M') if obj.used_at else "Ainda não utilizado"

    # Ações personalizadas
    @admin.action(description="Alterar para 'usado'")
    def marcar_como_usado(self, request, queryset):
        updated = queryset.update(used=True, used_at=timezone.now())
        self.message_user(request, f'{updated} código(s) marcado(s) como usado(s).')

    @admin.action(description="Alterar para 'disponível'")
    def marcar_como_disponivel(self, request, queryset):
        updated = queryset.update(used=False, used_at=None)
        self.message_user(request, f'{updated} código(s) marcado(s) como disponível(is).')

    actions = [marcar_como_disponivel, marcar_como_usado]

admin.site.register(CodigoSecreto, CodigoSecretoAdmin)
