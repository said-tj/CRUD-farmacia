from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Mod7LoginView, dashboard_mod7

urlpatterns = [
    # Login personalizado:
    path('login/', Mod7LoginView.as_view(), name='mod7_login'),

    # Logout vuelve al login de este módulo:
    path('logout/',
         LogoutView.as_view(next_page='mod7_login'),
         name='mod7_logout'),

    # Dashboard protegido:
    path('', dashboard_mod7, name='mod7_dashboard'),
]
