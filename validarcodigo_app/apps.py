from django.apps import AppConfig

class ValidarCodigoAppConfig(AppConfig):  # ⬅️ Nome da classe de configuração do app
    default_auto_field = "django.db.models.BigAutoField"
    name = "validarcodigo_app"  # ⬅️ Nome original do app (mantenha o caminho correto)
    verbose_name = "Gereciamento de Códigos Secretos"  # ⬅️ Nome amigável que aparecerá no Admin