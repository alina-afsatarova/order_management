from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('orders.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'), name='api'),
]
