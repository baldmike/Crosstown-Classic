from django.conf.urls import url
from views import index, watch, swing, reset

urlpatterns = [
    url(r'^$', index),
    url(r'^watch$', watch),
    url(r'^swing$', swing),
    url(r'^reset$', reset)
]