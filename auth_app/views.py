from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash, get_user_model
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import User
from validarcodigo_app.models import  CodigoSecreto
from datetime import datetime


User = get_user_model()  # Busca o modelo de usuário dinamicamente


def cadastro(request, codigo):
    try:
        secret_code = CodigoSecreto.objects.get(code=codigo, used=False)
        grupo = secret_code.group
    except CodigoSecreto.DoesNotExist:
        secret_code = None
        grupo = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        foto_profile = request.FILES.get('foto_profile')
        endereco = request.POST.get('endereco', '')
        numero_endereco = request.POST.get('numero_endereco', '')
        complemento = request.POST.get('complemento', '')
        cidade = request.POST.get('cidade', '')
        estado = request.POST.get('estado', '')  # deve ser uma sigla válida
        data_nascimento_raw = request.POST.get('data_nascimento')
        telefone = request.POST.get('telefone', '')
        whatsapp = request.POST.get('whatsapp', '')
        lembrar = request.POST.get('lembrar')

        tipo_sanguineo = request.POST.get('tipo_sanguineo', '')
        alergias = request.POST.get('alergias_intolerancias', '')
        medicamentos = request.POST.get('medicamentos', '')
        link_whatsapp = request.POST.get('link_whatsapp', '')
        links_outros = request.POST.get('links_outros', '')

        # Validação da senha
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'register.html', {'codigo': codigo, 'grupo': grupo})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'register.html', {'codigo': codigo, 'grupo': grupo})

        # Converter data
        try:
            data_nascimento = datetime.strptime(data_nascimento_raw, '%Y-%m-%d').date() if data_nascimento_raw else None
        except ValueError:
            messages.error(request, 'Data de nascimento inválida.')
            return render(request, 'register.html', {'codigo': codigo, 'grupo': grupo})

        if secret_code:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    endereco=endereco,
                    numero_endereco=numero_endereco,
                    complemento=complemento,
                    cidade=cidade,
                    estado=estado,
                    data_nascimento=data_nascimento,
                    telefone=telefone,
                    whatsapp=whatsapp,
                )

                if foto_profile:
                    user.foto_profile = foto_profile
                    user.save()

                if grupo:
                    user.groups.add(grupo)

                DadosOpcionais.objects.create(
                    usuario=user,
                    tipo_sanguineo=tipo_sanguineo,
                    alergias_intolerancias=alergias,
                    medicamentos=medicamentos,
                    link_whatsapp=link_whatsapp,
                    links_outros=links_outros
                )

                secret_code.used = True
                secret_code.used_at = timezone.now()
                secret_code.save()

            messages.success(request, 'Cadastro realizado com sucesso! Você já pode fazer login.')
            response = redirect('auth_app:entrar')

            if lembrar:
                response.set_cookie('lembrar_email', email, max_age=30 * 24 * 60 * 60)

            return response
        else:
            messages.error(request, 'Código inválido ou já utilizado.')

    return render(request, 'register.html', {
        'codigo': codigo,
        'grupo': grupo,
        'lembrar_email': request.COOKIES.get('lembrar_email', '')
    })

def user_login(request):
    if request.user.is_authenticated:
        return redirect('chaveiros:dashboard')  # nome da sua URL do dashboard
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        lembrar = request.POST.get('lembrar')

        # Autenticar usuário com email
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.first_name}!')
            response = redirect('chaveiros:dashboard')

            if lembrar:
                response.set_cookie('lembrar_email', email, max_age=30 * 24 * 60 * 60)
            
            return response
        
        else:
            messages.error(request, 'Credenciais inválidas. Tente novamente.')

    return render(request, 'login.html')


@login_required(login_url='auth_app:entrar')
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)  # Mantém o usuário autenticado após a alteração
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('auth_app:dashboard')
        else:
            messages.error(request, "Houve um erro ao alterar a senha. Tente novamente.")
    else:
        form_senha = PasswordChangeForm(request.user)
    
    return render(request, 'alterar_senha.html', {'form_senha': form_senha})


@login_required(login_url='auth_app:entrar')
def logout_view(request):
    logout(request)
    # next_url = request.GET.get('next', 'chaveiros:pagina_inicial')  # Redireciona para a página inicial ou outro destino
    messages.success(request, f'Logout feito com sucesso! Até logo!')
    return redirect('chaveiros:pagina_inicial')
