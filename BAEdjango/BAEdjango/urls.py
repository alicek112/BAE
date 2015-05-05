from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'BAEdjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^activities/', include('activities.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
