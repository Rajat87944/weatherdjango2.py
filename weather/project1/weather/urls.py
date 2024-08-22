from django.urls import path  # Corrected import
from .views import index

urlpatterns = [
    path('', index, name='home'),  # Root URL pattern
    path('get_weather/', index, name='get_weather'),
]
