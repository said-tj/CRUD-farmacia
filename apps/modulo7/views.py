from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.core.decorators import group_required

class Mod7LoginView(LoginView):
    """
    Formulario de login para Módulo 7.
    Si el usuario se valida, redirige a 'mod7_dashboard'.
    """
    template_name = 'modulo7/login.html'
    # Asegura que un usuario autenticado vea el formulario si entra aquí:
    redirect_authenticated_user = False

    def get_success_url(self):
        # Aquí definimos adónde va tras el login exitoso:
        return reverse_lazy('mod7_dashboard')

@group_required('Módulo7', login_url='mod7_login')
def dashboard_mod7(request):
    """
    Dashboard para el Módulo 7.
    Solo accesible si el usuario pertenece a 'Módulo7'.
    """
    return render(request, 'modulo7/dashboard.html', {
        'titulo': 'Panel de control – Módulo 7'
    })
