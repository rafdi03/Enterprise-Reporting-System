# FILE: config/urls.py
from django.contrib import admin
from django.urls import path, include  # <--- Jangan lupa 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Sambungkan ke file urls.py yang baru kamu buat di folder upload
    path('', include('upload.urls')), 
]
