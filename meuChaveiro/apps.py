from django.apps import AppConfig


class CadastroAnimalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meuChaveiro'
    verbose_name = 'Meu Chaveiro'
# Compare this snippet from meuChaveiro/urls.py:
# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [   
#     path('admin/', admin.site.urls),
#     path('', include('validarcodigo_app.urls')),
from django.contrib import admin