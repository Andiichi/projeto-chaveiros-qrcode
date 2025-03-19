from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages  
from django.contrib.auth.models import Group, User
from validarcodigo_app.models import CodigoSecreto
from django.contrib.auth.decorators import login_required

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('auth_app:pagina_inicial')  # Redireciona para a página de login


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')