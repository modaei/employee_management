from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin console.
    path('admin/', admin.site.urls),

    # APIs for user accounts management.
    path('api/', include('employment.api.urls')),
]
