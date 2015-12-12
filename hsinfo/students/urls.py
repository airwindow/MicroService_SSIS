from django.conf.urls import url
from students import views


urlpatterns = [
    url(r'^api/k12/$', views.student_list),
    url(r'^api/k12/(?P<ssn>[0-9]{9})/$', views.student_detail),
]