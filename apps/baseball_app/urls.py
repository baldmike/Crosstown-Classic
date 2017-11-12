from django.conf.urls import url
from views import index, watch, swing, reset, game_over

urlpatterns = [
    url(r'^$', index),
    url(r'^watch$', watch),
    url(r'^swing$', swing),
    url(r'^reset$', reset),
    url(r'^game_over$', game_over)
]