from django.conf.urls import url

from mrouter import views

urlpatterns = [
    url(r'^', views.route),
]
