from django.conf.urls import url
from students import views

urlpatterns = [
    url(r'^api/students/$', views.student_list),
    url(r'^api/students/enrollment/$', views.enroll_list),
    url(r'^api/students/(?P<sID>[a-z]{2,3}[\d]{4})/$', views.student_detail), 
    
    url(r'^api/students/enrollment/student/(?P<sID>[a-z]{2,3}[\d]{4})/$',views.enroll_student_detail),
    url(r'^api/students/enrollment/(?P<cID>[A-Z]{4}[\d]{4})/(?P<sID>[a-z]{2,3}[\d]{4})/$',views.enroll_detail),
]