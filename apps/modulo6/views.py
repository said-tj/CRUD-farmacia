from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.core.decorators import group_required

class Mod6LoginView(LoginView):
    """
    Formulario de login para Módulo 6.
    Si el usuario se valida, redirige a 'mod6_dashboard'.
    """
    template_name = 'modulo6/login.html'
    # Asegura que un usuario autenticado vea el formulario si entra aquí:
    redirect_authenticated_user = False

    def get_success_url(self):
        # Aquí definimos adónde va tras el login exitoso:
        return reverse_lazy('mod6_dashboard')

@group_required('Módulo6', login_url='mod6_login')
def dashboard_mod6(request):
    """
    Dashboard para el Módulo 6.
    Solo accesible si el usuario pertenece a 'Módulo6'.
    """
    return render(request, 'modulo6/dashboard.html', {
        'titulo': 'Panel de control – Módulo 6'
    })
