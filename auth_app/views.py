from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash, get_user_model
from django.contrib import messages  
from django.contrib.auth.models import Group
from validarcodigo_app.models import CodigoSecreto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()  # Busca o modelo de usuário dinamicamente


def cadastro(request, codigo):
    try:
        secret_code = CodigoSecreto.objects.get(code=codigo, used=False)
        grupo = secret_code.group  # Obtendo o grupo associado ao código
    except CodigoSecreto.DoesNotExist:
        secret_code = None
        grupo = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')  # Nome
        last_name = request.POST.get('last_name')  # Sobrenome

        if secret_code:
            user = User.objects.create_user(email=email, password=password)

            # Atribuindo o nome e sobrenome ao usuário
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Adiciona o usuário ao grupo, se existir
            if grupo:
                user.groups.add(grupo)

            # Marca o código como usado
            secret_code.used = True
            secret_code.save()

            messages.success(request, 'Cadastro realizado com sucesso! Você já pode fazer login.')
            return redirect('auth_app:entrar')

        messages.error(request, 'Código inválido ou já utilizado.')

    return render(request, 'register.html', {'codigo': codigo, 'grupo': grupo})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Autenticar usuário com email
        user = authenticate(request, email=email, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name}!')
            return redirect('auth_app:dashboard')
        else:
            messages.error(request, 'Credenciais inválidas. Tente novamente.')

    return render(request, 'login.html')

def admin_login(request):
   return redirect('/admin/login/')

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
    next_url = request.GET.get('next', 'auth_app:pagina_inicial')  # Redireciona para a página inicial ou outro destino
    return redirect(next_url)

def admin_logout(request):
    logout(request)
    return redirect('/admin/login/')

@login_required(login_url='auth_app:entrar')
def dashboard(request):
    return render(request, 'dashboard.html')
