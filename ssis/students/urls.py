from django.conf.urls import url
from students import views

urlpatterns = [
    url(r'^students/$', views.student_list),
    #url(r'^', views.student_list),
    url(r'^students/(?P<sID>[a-zA-Z0-9]+)/$', views.student_detail),
]