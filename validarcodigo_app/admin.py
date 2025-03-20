from django.contrib import admin
from django.utils import timezone
from .models import CodigoSecreto

class CodigoSecretoAdmin(admin.ModelAdmin):
    list_display = ('code_display', 'group', 'user_display', 'created_at', 'used', 'used_at_display')
    # list_filter = ('group', 'used')
    readonly_fields = ('code_display','group_display', 'created_at_display', 'used_at', 'used')
    ordering = ('-created_at',)

    def get_changeform_initial_data(self, request):
        """Define valores padrão para novos registros no admin."""
        return {
            'user': request.user,
            'created_at': timezone.now(),
        }

    def save_model(self, request, obj, form, change):
        """Se o campo 'used' for marcado, define a data e hora no 'used_at'."""
        if obj.used and obj.used_at is None:
            obj.used_at = timezone.now()  # Define a data atual ao marcar como usado
        elif not obj.used:
            obj.used_at = None  # Se desmarcar, remove a data de uso

        # Se for um novo código, preenche o usuário e código
        if not obj.pk:
            obj.user = request.user

        super().save_model(request, obj, form, change)

    # Métodos para exibir textos padrões em campos readonly
    @admin.display(description="Código Secreto")
    def code_display(self, obj):
        return obj.code if obj.code else "Código será gerado automaticamente"

    @admin.display(description="Grupo")
    def group_display(self, obj):
        return obj.group
    
    @admin.display(description="Nome do Criador")
    def user_display(self, obj):
        return obj.user.email if obj.user.email else "Nome do Criador será definido automaticamente"

    @admin.display(description="Criado em")
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M') if obj.created_at else "Será preenchido na criação"

    @admin.display(description="Data de Uso")
    def used_at_display(self, obj):
        return obj.used_at.strftime('%d/%m/%Y %H:%M') if obj.used_at else "Ainda não utilizado"

    


    ##Ações personalizadas para alterar o status do codigo
    @admin.action(description="Alterar para 'usado'")
    def marcar_como_usado(self, request, queryset):
        updated = queryset.update(used=True, used_at=timezone.now())
        self.message_user(request, f'{updated} código(s) marcado(s) como usado(s).')

    @admin.action(description="Alterar para 'disponivel'")
    def marcar_como_disponivel(self, request, queryset):
        updated = queryset.update(used=False, used_at=None)
        self.message_user(request, f'{updated} código(s) marcado(s) como disponível(is).')
    

    actions = [marcar_como_disponivel, marcar_como_usado]


admin.site.register(CodigoSecreto, CodigoSecretoAdmin)

# from django.contrib import admin
# from django.utils import timezone
# from .models import CodigoSecreto

# class CodigoSecretoAdmin(admin.ModelAdmin):
#     list_display = ('code_display', 'group_display', 'user_display', 'created_at', 'used', 'used_at_display')
#     # list_filter = ('group', 'used')
#     readonly_fields = ('code_display', 'created_at_display', 'used_at')  # Inicialmente, apenas estes campos são readonly
#     ordering = ('-created_at',)

#     def get_readonly_fields(self, request, obj=None):
#         # Remover o campo 'used' de readonly quando não for um novo objeto
#         readonly_fields = super().get_readonly_fields(request, obj)
#         if obj and obj.pk:  # Se for um objeto já existente, remova 'used' da lista de campos readonly
#             readonly_fields = tuple(field for field in readonly_fields if field != 'used')
#         return readonly_fields

#     def get_changeform_initial_data(self, request):
#         """Define valores padrão para novos registros no admin."""
#         return {
#             'user': request.user,
#             'created_at': timezone.now(),
#         }

#     def save_model(self, request, obj, form, change):
#         """Se o campo 'used' for marcado, define a data e hora no 'used_at'."""
#         if obj.used and obj.used_at is None:
#             obj.used_at = timezone.now()  # Define a data atual ao marcar como usado
#         elif not obj.used:
#             obj.used_at = None  # Se desmarcar, remove a data de uso

#         # Se for um novo código, preenche o usuário e código
#         if not obj.pk:
#             obj.user = request.user

#         super().save_model(request, obj, form, change)

#     # Métodos para exibir textos padrões em campos readonly
#     @admin.display(description="Código Secreto")
#     def code_display(self, obj):
#         return obj.code if obj.code else "Código será gerado automaticamente"

#     @admin.display(description="Grupo")
#     def group_display(self, obj):
#         return obj.group
    
#     @admin.display(description="Nome do Criador")
#     def user_display(self, obj):
#         return obj.user.get_full_name if obj.user.get_full_name else "Nome do Criador será definido automaticamente"

#     @admin.display(description="Criado em")
#     def created_at_display(self, obj):
#         return obj.created_at.strftime('%d/%m/%Y %H:%M') if obj.created_at else "Será preenchido na criação"

#     @admin.display(description="Data de Uso")
#     def used_at_display(self, obj):
#         return obj.used_at.strftime('%d/%m/%Y %H:%M') if obj.used_at else "Ainda não utilizado"

#     ##Ações personalizadas para alterar o status do codigo
#     @admin.action(description="Alterar para 'usado'")
#     def marcar_como_usado(self, request, queryset):
#         updated = queryset.update(used=True, used_at=timezone.now())
#         self.message_user(request, f'{updated} código(s) marcado(s) como usado(s).')

#     @admin.action(description="Alterar para 'disponivel'")
#     def marcar_como_disponivel(self, request, queryset):
#         updated = queryset.update(used=False, used_at=None)
#         self.message_user(request, f'{updated} código(s) marcado(s) como disponível(is).')

#     actions = [marcar_como_disponivel, marcar_como_usado]

# admin.site.register(CodigoSecreto, CodigoSecretoAdmin)
