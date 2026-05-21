
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('accounts/', include('accounts.urls')),
    path('doctor/', include('doctor.urls')),
    path('appointment/', include('appointment.urls')),
    path('patient/', include('patient.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
