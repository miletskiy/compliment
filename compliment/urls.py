from django.conf.urls import include, url
from django.contrib import admin

from core import urls as core_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'compliment.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(core_urls, namespace='core')),
]
