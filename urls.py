"""
URL configuration for oliveoshoppe project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts.views import auth_confirm, auth_confirm_verify
from api.views import shop_view

urlpatterns = [
    path('', shop_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('chatbot/', include('chatbot.urls')),
    
    # Auth confirmation endpoint (for Supabase redirect)
    path('auth/confirm/', auth_confirm, name='auth_confirm'),
    path('auth/confirm/verify/', auth_confirm_verify, name='auth_confirm_verify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
