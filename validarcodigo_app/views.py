from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CodigoSecreto

def validar_codigo(request):
    if request.method == "POST":
        code = request.POST.get('code')

        # Verifica se o código não está vazio
        if not code:
            messages.error(request, 'O código não pode estar vazio.')
            return redirect('validar-codigo')

        code = code.strip()  # Remove espaços extras

        try:
            secret_code = CodigoSecreto.objects.get(code=code, used=False)
            group = secret_code.group  # Grupo associado ao código

            messages.success(request, 'Código validado com sucesso!')
            return redirect('auth_app:cadastro', codigo=secret_code.code)

        except CodigoSecreto.DoesNotExist:
            messages.error(request, 'Código inválido ou já utilizado.')
            return redirect('validar-codigo')

    return render(request, 'validate_code.html')

# def generate_code(request):
#     if request.method == "POST":
#         group_id = request.POST.get('group_id')
#         group = Group.objects.get(id=group_id)  # Obtém o grupo selecionado
#         code = str(uuid.uuid4())  # Gera um código UUID
#         secret_code = CodigoSecreto.objects.create(
#             code=code,
#             group=group,
#             user=request.user  # Define o usuário que gerou o código
#         )
#         secret_code.save()
#         messages.success(request, 'Código gerado com sucesso.')
#         return redirect('home')  # Substitua 'some_view_name' pelo nome da view para redirecionar após a geração do código

#     groups = Group.objects.all()  # Obtém todos os grupos
#     return render(request, 'home.html', {'groups': groups})  # Renderiza a página de geração de código com os grupos disponíveis