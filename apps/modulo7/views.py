# apps/modulo7/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from apps.core.decorators import group_required
from apps.modulo5.models import Medicamento  # Importa modelo de módulo5

class Mod7LoginView(LoginView):
    template_name = 'modulo7/login.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('mod7_dashboard')

@group_required('Módulo7', login_url='mod7_login')
def dashboard_mod7(request):
    meds = Medicamento.objects.all()
    return render(request, 'modulo7/dashboard.html', {'meds': meds})


def mod7_logout_view(request):
    logout(request)
    return redirect('mod7_login')
