from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.core.decorators import group_required

class Mod1LoginView(LoginView):
    """
    Formulario de login para Módulo 1.
    Si el usuario se valida, redirige a 'mod1_dashboard'.
    """
    template_name = 'modulo1/login.html'
    # Asegura que un usuario autenticado vea el formulario si entra aquí:
    redirect_authenticated_user = False

    def get_success_url(self):
        # Aquí definimos adónde va tras el login exitoso:
        return reverse_lazy('mod1_dashboard')

@group_required('Módulo1', login_url='mod1_login')
def dashboard_mod1(request):
    """
    Dashboard para el Módulo 1.
    Solo accesible si el usuario pertenece a 'Módulo1'.
    """
    return render(request, 'modulo1/dashboard.html', {
        'titulo': 'Panel de control – Módulo 1'
    })
