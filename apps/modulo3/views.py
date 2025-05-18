from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.core.decorators import group_required

class Mod3LoginView(LoginView):
    """
    Formulario de login para Módulo 3.
    Si el usuario se valida, redirige a 'mod3_dashboard'.
    """
    template_name = 'modulo3/login.html'
    # Asegura que un usuario autenticado vea el formulario si entra aquí:
    redirect_authenticated_user = False

    def get_success_url(self):
        # Aquí definimos adónde va tras el login exitoso:
        return reverse_lazy('mod3_dashboard')

@group_required('Módulo3', login_url='mod3_login')
def dashboard_mod3(request):
    """
    Dashboard para el Módulo 3.
    Solo accesible si el usuario pertenece a 'Módulo3'.
    """
    return render(request, 'modulo3/dashboard.html', {
        'titulo': 'Panel de control – Módulo 3'
    })
