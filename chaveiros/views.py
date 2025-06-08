from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone


@login_required
def atualizar_perfil(request):
    user = request.user
    estados = get_user_model().CHOICES_UF  # Lista de estados para o formulário

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        data_nascimento_raw = request.POST.get('data_nascimento', '')
        telefone = request.POST.get('telefone', '')
        whatsapp = request.POST.get('whatsapp', '')
        endereco = request.POST.get('endereco', '')
        numero_endereco = request.POST.get('numero', '')
        complemento = request.POST.get('complemento', '')
        cidade = request.POST.get('cidade', '')
        estado = request.POST.get('estado', '')  # deve ser uma sigla válida
        bio = request.POST.get('bio', '')

        # Verifica se já existe outro usuário com esse e-mail
        if get_user_model().objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Este e-mail já está em uso por outro usuário.')
            return render(request, 'dashboard/dashboard_profile_editar.html', {
                'form_data': request.POST,
                'user': user,
                'estados': estados,
            })

        # Valida data de nascimento e maioridade
        try:
            data_nascimento = datetime.strptime(data_nascimento_raw, '%Y-%m-%d').date() if data_nascimento_raw else None
            if data_nascimento:
                hoje = datetime.now().date()
                idade = (hoje - data_nascimento).days // 365
                if idade < 18:
                    messages.error(request, 'Você precisa ter pelo menos 18 anos.')
                    return render(request, 'dashboard/dashboard_profile_editar.html', {
                        'form_data': request.POST,
                        'user': user,
                        'estados': estados,
                    })
        except ValueError:
            messages.error(request, 'Data de nascimento inválida.')
            return render(request, 'dashboard/dashboard_profile_editar.html', {
                'form_data': request.POST,
                'user': user,
                'estados': estados,
            })

        # Atualiza os dados
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.data_nascimento = data_nascimento
        user.telefone = telefone
        user.whatsapp = whatsapp
        user.endereco = endereco
        user.numero_endereco = numero_endereco
        user.complemento = complemento
        user.cidade = cidade
        user.estado = estado
        user.bio = bio
        user.updated_at = timezone.now()
        
        user.save()

        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('chaveiros:perfil')  # ou a página que você quiser
    
    # Renderiza o template com os dados do usuário e a lista de estados
    return render(request, 'dashboard/dashboard_profile_editar.html', {
        'user': user,
        'estados': estados,
        })


@login_required
def atualizar_foto(request):
    if request.method == 'POST':
        foto = request.FILES.get('foto_profile')
        if foto:
            user = request.user
            user.foto_profile = foto
            user.updated_at = timezone.now()
            user.save()
            messages.success(request, 'Foto atualizada com sucesso!')
        else:
            messages.error(request, 'Nenhuma foto selecionada.')

    return redirect('chaveiros:perfil-editar')  # Ou sua URL do perfil


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
    