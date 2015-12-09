from django.conf.urls import url
from students import views

urlpatterns = [
    url(r'^$', views.student_list),
    url(r'^(?P<ssn>[\d]{9})', views.student_detail),
]
