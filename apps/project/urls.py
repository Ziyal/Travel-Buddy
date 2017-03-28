from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    # url(r'^logout$', views.logout, name = 'logout'),
    url(r'^add_travel_plan$', views.add_travel_plan, name = 'add_travel_plan'),
    url(r'^process_trip$', views.process_trip, name = 'process_trip'),
    url(r'^trip/(?P<id>\d+)$', views.trip, name = 'trip'),
    url(r'^trip/join/(?P<id>\d+)$', views.join, name = 'join'),
]
