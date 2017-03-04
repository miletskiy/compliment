
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^twitter/$', views.twitter, name='twitter'),
    url(r'^instagram/$', views.instagram, name='instagram'),
    url(r'^photo/$', views.photo, name='photo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))

