from django.conf.urls import url
from students import views

urlpatterns = [
    url(r'^students/$', views.student_list),
    #url(r'^', views.student_list),
    url(r'^students/(?P<sID>[0-9]+)/$', views.student_detail),
]