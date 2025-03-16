from django.contrib import admin
from django.urls import path
from validarcodigo_app.views import *

urlpatterns = [
    path('validar-codigo/', validar_codigo, name='validar-codigo'),  # URL para validação do código
]