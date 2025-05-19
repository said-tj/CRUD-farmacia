# apps/modulo7/urls.py
from django.urls import path
from .views import Mod7LoginView, dashboard_mod7, mod7_logout_view

urlpatterns = [
    path('login/', Mod7LoginView.as_view(), name='mod7_login'),
    path('logout/', mod7_logout_view,  name='mod7_logout'),
    path('', dashboard_mod7,           name='mod7_dashboard'),
]