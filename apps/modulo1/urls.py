from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Mod1LoginView, dashboard_mod1

urlpatterns = [
    # Login personalizado:
    path('login/', Mod1LoginView.as_view(), name='mod1_login'),

    # Logout vuelve al login de este módulo:
    path('logout/',
         LogoutView.as_view(next_page='mod1_login'),
         name='mod1_logout'),

    # Dashboard protegido:
    path('', dashboard_mod1, name='mod1_dashboard'),
]
