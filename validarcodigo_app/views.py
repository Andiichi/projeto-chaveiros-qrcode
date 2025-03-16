# from django.shortcuts import render, redirect
# from .models import CodigoSecreto
# from django.urls import reverse
# from django.contrib import messages
# from django.contrib.auth.models import User, Group
# from django.utils import timezone
# import uuid

# def validar_codigo(request):
#     if request.method == "POST":
#         code = request.POST.get('code')
#         try:
#             # Tenta obter o código secreto que não foi usado
#             secret_code = CodigoSecreto.objects.get(code=code, used=False)
#             group = secret_code.group

#             # Marca o código como usado e preenche os campos adicionais
#             secret_code.used = True
#             secret_code.used_at = timezone.now()  # Define a data e hora de uso
#             secret_code.user = request.user  # Define o usuário que usou o código
#             secret_code.save()

#             # Redireciona para a URL de cadastro (com o nome correto)
#             return redirect(reverse('cadastro', args=[secret_code.code]))  # Certifique-se de que o nome da URL seja 'cadastro'
        
#         except CodigoSecreto.DoesNotExist:
#             # Exibe uma mensagem de erro se o código não existir ou já tiver sido usado
#             messages.error(request, 'Código inválido ou já utilizado.')

#     return render(request, 'validate_code.html')

# # def generate_code(request):
# #     if request.method == "POST":
# #         group_id = request.POST.get('group_id')
# #         group = Group.objects.get(id=group_id)  # Obtém o grupo selecionado
# #         code = str(uuid.uuid4())  # Gera um código UUID
# #         secret_code = CodigoSecreto.objects.create(
# #             code=code,
# #             group=group,
# #             created_at=timezone.now(),  # Define a data e hora de criação
# #             user=request.user  # Define o usuário que gerou o código
# #         )
# #         secret_code.save()
# #         messages.success(request, 'Código gerado com sucesso.')
# #         return redirect('some_view_name')  # Substitua 'some_view_name' pelo nome da view para redirecionar após a geração do código

# #     groups = Group.objects.all()  # Obtém todos os grupos
# #     return render(request, 'generate_code.html', {'groups': groups})  # Renderiza a página de geração de código com os grupos disponíveis


from django.shortcuts import render, redirect
from .models import CodigoSecreto
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.utils import timezone
import uuid

def validar_codigo(request):
    if request.method == "POST":
        code = request.POST.get('code')
        try:
            # Tenta obter o código secreto que não foi usado
            secret_code = CodigoSecreto.objects.get(code=code, used=False)
            group = secret_code.group

            # Marca o código como usado e preenche os campos adicionais
            secret_code.used = True
            secret_code.used_at = timezone.now()  # Define a data e hora de uso
            # secret_code.user = request.user  # Define o usuário que usou o código
            secret_code.save()

            # Redireciona para a URL de cadastro (com o nome correto)
            messages.success(request, 'Código validado com sucesso!')
            return redirect(reverse('home', args=[secret_code.code]))  # Certifique-se de que o nome da URL seja 'cadastro'
        
        except CodigoSecreto.DoesNotExist:
            # Exibe uma mensagem de erro se o código não existir ou já tiver sido usado
            messages.error(request, 'Código inválido ou já utilizado.')

    return render(request, 'validate_code.html')

def generate_code(request):
    if request.method == "POST":
        group_id = request.POST.get('group_id')
        group = Group.objects.get(id=group_id)  # Obtém o grupo selecionado
        code = str(uuid.uuid4())  # Gera um código UUID
        secret_code = CodigoSecreto.objects.create(
            code=code,
            group=group,
            user=request.user  # Define o usuário que gerou o código
        )
        secret_code.save()
        messages.success(request, 'Código gerado com sucesso.')
        return redirect('home')  # Substitua 'some_view_name' pelo nome da view para redirecionar após a geração do código

    groups = Group.objects.all()  # Obtém todos os grupos
    return render(request, 'home.html', {'groups': groups})  # Renderiza a página de geração de código com os grupos disponíveis