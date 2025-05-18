from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.core.decorators import group_required

class Mod2LoginView(LoginView):
    """
    Formulario de login para Módulo 2.
    Si el usuario se valida, redirige a 'mod2_dashboard'.
    """
    template_name = 'modulo2/login.html'
    # Asegura que un usuario autenticado vea el formulario si entra aquí:
    redirect_authenticated_user = False

    def get_success_url(self):
        # Aquí definimos adónde va tras el login exitoso:
        return reverse_lazy('mod2_dashboard')

@group_required('Módulo2', login_url='mod2_login')
def dashboard_mod2(request):
    """
    Dashboard para el Módulo 2.
    Solo accesible si el usuario pertenece a 'Módulo2'.
    """
    return render(request, 'modulo2/dashboard.html', {
        'titulo': 'Panel de control – Módulo 2'
    })
