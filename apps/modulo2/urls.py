from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Mod2LoginView, dashboard_mod2

urlpatterns = [
    # Login personalizado:
    path('login/', Mod2LoginView.as_view(), name='mod2_login'),

    # Logout vuelve al login de este módulo:
    path('logout/',
         LogoutView.as_view(next_page='mod2_login'),
         name='mod2_logout'),

    # Dashboard protegido:
    path('', dashboard_mod2, name='mod2_dashboard'),
]
