from django.contrib.sessions.middleware import SessionMiddleware

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