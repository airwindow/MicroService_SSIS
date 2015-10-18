from django.conf.urls import url
from students import views

urlpatterns = [
    url(r'^api/students/$', views.student_list),
    #url(r'^', views.student_list),
    url(r'^api/students/(?P<sID>[A-Za-z]{2}[\d]{4})/$', views.student_detail), 
]