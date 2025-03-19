from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages  
from django.contrib.auth.models import Group, User
from validarcodigo_app.models import CodigoSecreto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


def cadastro(request, codigo):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            secret_code = CodigoSecreto.objects.get(code=codigo, used=False)

            user = User.objects.create_user(username=username, password=password)
            user.groups.add(secret_code.group)

            secret_code.used = True
            secret_code.save()

            messages.success(request, 'Cadastro realizado com sucesso! Você já pode fazer login.')
            return redirect('auth_app:entrar')

        except CodigoSecreto.DoesNotExist:
            messages.error(request, 'Código inválido ou já utilizado.')

    return render(request, 'register.html', {'codigo': codigo})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            messages.success(request, 'Bem-vindo, {}!'.format(user.first_name))
            return redirect('auth_app:dashboard')
        else:
#             # Caso as credenciais estejam erradas
            messages.error(request, 'Credenciais inválidas. Tente novamente.')
    return render(request, 'login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin:index')  # Redireciona para o painel admin
        else:
#             # Caso as credenciais estejam erradas
            messages.error(request, 'Credenciais inválidas. Tente novamente.')

    return render(request, 'login_admin.html')


def alterar_senha(request):
    if request.method == "POST":
        username = request.POST.get('username')
        # Verificar se o nome de usuário corresponde ao usuário autenticado
        if username != request.user.username:
            messages.error(request, "Nome de usuário inválido.")
            return redirect('auth_app:alterar_senha')  # Redireciona de volta para a página de alteração de senha

        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)  # Mantém o usuário autenticado após a alteração
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('auth_app:dashboard')  # Altere o nome da URL conforme necessário
        else:
            messages.error(request, "Houve um erro ao alterar a senha. Tente novamente.")
    else:
        form_senha = PasswordChangeForm(request.user)
    
    return render(request, 'alterar_senha.html', {'form_senha': form_senha})


# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('auth_app:dashboard')  # Ou qualquer outra página

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Autentica o usuário
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             # Usuário autenticado, faz login na sessão
#             login(request, user)
#             messages.success(request, 'Bem-vindo, {}!'.format(user.first_name))
#             return redirect('auth_app:dashboard')  # Redireciona para a página inicial ou página desejada
#         else:
#             # Caso as credenciais estejam erradas
#             messages.error(request, 'Credenciais inválidas. Tente novamente.')

#     return render(request, 'login.html')


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('auth_app:pagina_inicial')  # Redireciona para a página de login



@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'dashboard.html')