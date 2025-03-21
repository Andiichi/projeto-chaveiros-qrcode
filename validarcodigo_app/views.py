from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
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
            # Tenta encontrar o código com o status 'usado=False'
            secret_code = CodigoSecreto.objects.get(code=code, used=False)
            group = secret_code.group  # Grupo associado ao código

            # Mensagem de sucesso
            messages.success(request, 'Código validado com sucesso!')
            # Redireciona para o cadastro com o código como parâmetro na URL
            return redirect(reverse('auth_app:cadastro', kwargs={'codigo': secret_code.code}))

        except CodigoSecreto.DoesNotExist:
            # Se o código não existir ou já foi utilizado
            messages.error(request, 'Código inválido ou já utilizado.')
            return redirect('validar-codigo')

    return render(request, 'validate_code.html')