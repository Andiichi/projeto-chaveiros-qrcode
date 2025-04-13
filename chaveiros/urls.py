from django.contrib import admin
from django.urls import path
from auth_app.views import *

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import atualizar_perfil, atualizar_foto

app_name = 'chaveiros'  # Definição do namespace para a aplicação de autenticação

urlpatterns = [
    #Rotas comuns do site
    path('pagina-inicial/', TemplateView.as_view(template_name='pagina-inicial.html'), name='pagina_inicial'),

    # Rotas do Dashboard
    path('dashboard/', login_required(TemplateView.as_view(template_name='dashboard/dashboard_principal.html')), name='dashboard'),
    path('dashboard/listagem', login_required(TemplateView.as_view(template_name='dashboard/dashboard_listagem.html')), name='dashboard_listagem'),

    # Rotas do perfil e editar perfil
    path('dashboard/perfil', login_required(TemplateView.as_view(template_name='dashboard/dashboard_profile.html')), name='perfil'),
    path('dashboard/editar-perfil', atualizar_perfil, name='perfil-editar'),
    path('atualizar-foto/', atualizar_foto, name='atualizar_foto'),

]