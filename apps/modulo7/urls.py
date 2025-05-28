# apps/modulo7/urls.py
from django.urls import path
from .views import (
    Mod7LoginView, dashboard_mod7, notifications,
    add_to_canasta, remove_from_canasta, basket,
    basket_confirm, providers_catalog, provider_create,
    provider_edit, provider_delete, provider_upload,
    mod7_logout, pedido_pdf
)

urlpatterns = [
    path('login/', Mod7LoginView.as_view(), name='mod7_login'),
    path('logout/', mod7_logout, name='mod7_logout'),
    path('', dashboard_mod7, name='mod7_dashboard'),
    path('notifications/', notifications, name='mod7_notifications'),
    path('notifications/add/<int:pk>/', add_to_canasta, name='mod7_notifications_add'),
    path('basket/', basket, name='mod7_basket'),
    path('basket/remove/<int:pk>/', remove_from_canasta, name='mod7_basket_remove'),
    path('basket/confirm/', basket_confirm, name='mod7_basket_confirm'),
    path('basket/pdf/<int:pk>/', pedido_pdf, name='mod7_pedido_pdf'),
    path('providers/', providers_catalog, name='mod7_providers'),
    path('providers/create/', provider_create, name='mod7_provider_create'),
    path('providers/edit/<int:pk>/', provider_edit, name='mod7_provider_edit'),
    path('providers/delete/<int:pk>/', provider_delete, name='mod7_provider_delete'),
    path('providers/upload/<int:pk>/', provider_upload, name='mod7_provider_upload'),
]