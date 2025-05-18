from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Mod6LoginView, dashboard_mod6

urlpatterns = [
    # Login personalizado:
    path('login/', Mod6LoginView.as_view(), name='mod6_login'),

    # Logout vuelve al login de este módulo:
    path('logout/',
         LogoutView.as_view(next_page='mod6_login'),
         name='mod6_logout'),

    # Dashboard protegido:
    path('', dashboard_mod6, name='mod6_dashboard'),
]
