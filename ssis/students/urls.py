from django.conf.urls import url
from students import views

urlpatterns = [
    url(r'^api/students/$', views.student_list),
    url(r'^api/students/enrollment/$', views.enroll_list),
    url(r'^api/students/(?P<sID>[A-Za-z]{2,3}[\d]{4})/$', views.student_detail), 
    
    url(r'^api/students/enrollment/student/(?P<sID>[A-Za-z]{2,3}[\d]{4})/$',views.enroll_student_detail),
    url(r'^api/students/enrollment/(?P<cID>[a-zA-Z0-9]+)/(?P<sID>[A-Za-z]{2,3}[\d]{4})/$',views.enroll_detail),
]