from django.conf.urls import url
from . import views

urlpatterns = [
    # ex : /activities/
    url(r'^$', views.index, name = 'index'),
    # ex : /activities/about
    url(r'^about/$', views.about, name = 'about'),
    # ex: /activities/category/
    url(r'^((?!^about/$)?P<cat_id>\w+)/$', views.cat, name = 'cat'),
]
