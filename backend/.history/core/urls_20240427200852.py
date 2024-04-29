from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.template.response import TemplateResponse

def welcome_view(request):
    return TemplateResponse(request, 'welcome.html', {'message': 'Welcome to Virtual try On Website'})

print('')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('imageApp.api.urls')),
    path('', welcome_view, name='welcome'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
