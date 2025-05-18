# from django.urls import path
# from django.contrib.auth.views import LogoutView
# from .views import Mod5LoginView, dashboard_mod5

# urlpatterns = [
#     # Login personalizado:
#     path('login/', Mod5LoginView.as_view(), name='mod5_login'),

#     # Logout vuelve al login de este módulo:
#     path('logout/',
#          LogoutView.as_view(next_page='mod5_login'),
#          name='mod5_logout'),

#     # Dashboard protegido:
#     path('', dashboard_mod5, name='mod5_dashboard'),
# ]

# apps/modulo5/urls.py
# apps/modulo5/urls.py
# apps/modulo5/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView
from .views import (
    lista_medicamentos,
    add_medicamento,
    reduce_stock,
    delete_medicamento,
    mod5_logout_view,      # <–– importa tu logout “a mano”
)

class Mod5LoginView(LoginView):
    template_name = 'modulo5/login.html'
    redirect_authenticated_user = False
    def get_success_url(self):
        return reverse_lazy('mod5_list')

urlpatterns = [
    path('login/',  Mod5LoginView.as_view(), name='mod5_login'),
    path('logout/', mod5_logout_view,    name='mod5_logout'),  # ← aquí
    path('',       lista_medicamentos, name='mod5_list'),
    path('add/',   add_medicamento,    name='mod5_add'),
    path('reduce/',reduce_stock,       name='mod5_reduce'),
    path('delete/<int:pk>/', delete_medicamento, name='mod5_delete'),
]
