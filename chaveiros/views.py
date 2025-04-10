from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect


# 📄 Página de dashboard para o usuário comum
def dashboard(request):
    if request.user.is_authenticated:
        return redirect(request, 'chaveiros:dashboard')
    return HttpResponse('Você precisa estar logado.')


# 📄 Dashboard exclusivo para admin (usando admin_sessionid)
def admin_dashboard(request):
    session_key = request.COOKIES.get('admin_sessionid')
    if session_key:
        try:
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get('_auth_user_id')
            user = get_user_model().objects.get(id=user_id)
            if user.is_staff:
                return HttpResponse(f'Admin logado como: {user.username}')
        except:
            pass
    return HttpResponse('Acesso negado para admin.')
    