from django.contrib.sessions.middleware import SessionMiddleware
    
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from meuChaveiro import settings

class SeparateSessionMiddleware(SessionMiddleware):
    def __call__(self, request):
        if request.path.startswith('/admin/'):
            # Para o painel admin, usa o cookie de sessão do admin
            request.session._session_cookie_name = settings.ADMIN_SESSION_COOKIE_NAME
        else:
            # Para usuários normais, mantém o cookie de sessão padrão
            request.session._session_cookie_name = settings.SESSION_COOKIE_NAME

        return super().__call__(request)


class LoginRequiredMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == settings.LOGIN_URL and 'next' in request.GET:
            messages.error(request, 'Você precisa estar logado para acessar o dashboard.')
        return self.get_response(request)