from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'pagina-inicial.html')  # Renderiza a página inicial