from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Mod3LoginView, dashboard_mod3

urlpatterns = [
    # Login personalizado:
    path('login/', Mod3LoginView.as_view(), name='mod3_login'),

    # Logout vuelve al login de este módulo:
    path('logout/',
         LogoutView.as_view(next_page='mod3_login'),
         name='mod3_logout'),

    # Dashboard protegido:
    path('', dashboard_mod3, name='mod3_dashboard'),
]
