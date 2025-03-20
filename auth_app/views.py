from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages  
from django.contrib.auth.models import Group, User
from validarcodigo_app.models import CodigoSecreto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


def cadastro(request, codigo):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            secret_code = CodigoSecreto.objects.get(code=codigo, used=False)

            user = User.objects.create_user(email=email, password=password)
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
        email = request.POST.get('email')
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
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
        email = request.POST.get('email')  # Usando get() para evitar KeyError
        password = request.POST.get('password')  # Usando get() para evitar KeyError

        # Verificando se email e senha foram fornecidos
        if email and password:
            # Autenticar o usuário com base no email e senha
            user = authenticate(request, email=email, password=password)
            if user is not None and user.is_staff and user.is_active:
                # Se o usuário é autenticado, é staff e está ativo, faz login
                login(request, user)
                return redirect('admin:index')  # Redireciona para o painel admin
            else:
                # Se as credenciais não forem válidas ou o usuário não for staff
                messages.error(request, 'Credenciais inválidas ou você não tem acesso de administrador.')
        else:
            messages.error(request, 'Por favor, insira tanto o e-mail quanto a senha.')

    return render(request, 'login_admin.html')


def alterar_senha(request):
    if request.method == "POST":
        email = request.POST.get('email')
        # Verificar se o email corresponde ao email autenticado
        if email != request.user.email:
            messages.error(request, "Email inválido")
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



@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('auth_app:pagina_inicial')  # Redireciona para a página de login



@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'dashboard.html')