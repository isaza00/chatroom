from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='chat/')),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
]
