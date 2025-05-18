from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.core.decorators import group_required

class Mod4LoginView(LoginView):
    """
    Formulario de login para Módulo 4.
    Si el usuario se valida, redirige a 'mod4_dashboard'.
    """
    template_name = 'modulo4/login.html'
    # Asegura que un usuario autenticado vea el formulario si entra aquí:
    redirect_authenticated_user = False

    def get_success_url(self):
        # Aquí definimos adónde va tras el login exitoso:
        return reverse_lazy('mod4_dashboard')

@group_required('Módulo4', login_url='mod4_login')
def dashboard_mod4(request):
    """
    Dashboard para el Módulo 4.
    Solo accesible si el usuario pertenece a 'Módulo4'.
    """
    return render(request, 'modulo4/dashboard.html', {
        'titulo': 'Panel de control – Módulo 4'
    })
