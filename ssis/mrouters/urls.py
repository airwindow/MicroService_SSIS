from django.conf.urls import url
from mrouters import views

urlpatterns = [
    url(r'^', views.route_request),
]
