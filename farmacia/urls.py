"""
URL configuration for farmacia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('accounts/logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),

    # Incluimos los módulos
    path('mod1/', include('apps.modulo1.urls')),
    path('mod2/', include('apps.modulo2.urls')),
    path('mod3/', include('apps.modulo3.urls')),
    path('mod4/', include('apps.modulo4.urls')),
    path('mod5/', include('apps.modulo5.urls')),
    path('mod6/', include('apps.modulo6.urls')),
    path('mod7/', include('apps.modulo7.urls')),
    # … hasta mod7 …
]


