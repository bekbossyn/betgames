from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('main.urls')),
    url(r'^api/game/', include('game.urls')),
]
