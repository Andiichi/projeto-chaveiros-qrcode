from django.contrib import admin
from django.urls import path
from validarcodigo_app.views import *

urlpatterns = [
    path('validacao/', validar_codigo, name='validar-codigo'),  # URL para validação do código
]