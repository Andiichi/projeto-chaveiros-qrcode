from django.apps import AppConfig


class AuthAppConfig(AppConfig):  
    default_auto_field = "django.db.models.BigAutoField" 
    name = 'auth_app'  
    verbose_name = "Gereciamento de Usuários"  

    def ready(self):
        import auth_app.signals 
