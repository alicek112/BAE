from django.conf.urls import url
from . import views

urlpatterns = [
    # ex : /activities/
    url(r'^$', views.index, name = 'index'),
    # ex: /activities/category/
    url(r'^(?P<cat_id>\w+)/$', views.cat, name = 'cat'),
]
