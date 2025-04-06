from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import User
from .forms import UserUpdateForm


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('profile')  # ou qualquer página que quiser redirecionar após o update

    def get_object(self, queryset=None):
        return self.request.user  # atualiza os dados do usuário logado
    
    