from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Mod4LoginView, dashboard_mod4

urlpatterns = [
    # Login personalizado:
    path('login/', Mod4LoginView.as_view(), name='mod4_login'),

    # Logout vuelve al login de este módulo:
    path('logout/',
         LogoutView.as_view(next_page='mod4_login'),
         name='mod4_logout'),

    # Dashboard protegido:
    path('', dashboard_mod4, name='mod4_dashboard'),
]
