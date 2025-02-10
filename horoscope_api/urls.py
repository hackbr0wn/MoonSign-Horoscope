# horoscope_api/urls.py
from django.contrib import admin
from django.urls import path
from .views import HoroscopeAPIView, home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', home, name='home'),  # Map the root URL (/) to the home view
    path('api/horoscope/', HoroscopeAPIView.as_view(), name='horoscope-api'),  # Existing API endpoint
]
