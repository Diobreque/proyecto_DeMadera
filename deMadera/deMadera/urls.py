"""
URL configuration for deMadera project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app_deMadera import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index ),
    path('cotizar/',views.cotizar),
    path('cotizacion/',views.create_desk),
    path('coti/', views.index_desk, name='index_desk'),
    path('update-desk/', views.update_desk, name='update_desk'),
    path('crear-escritorio/', views.create_desk, name='create_desk'),
    path('crear-boleta/', views.create_boleta, name='create_boleta'),
    path('boleta-pdf/<int:boleta_id>/', views.generate_pdf, name='generate_pdf'),]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)