from django.conf.urls import url
from courses import views

urlpatterns = [
    url(r'^api/courses/$', views.course_list),
    url(r'^api/courses/enrollment/$', views.enroll_list),
    url(r'^api/courses/(?P<cID>[a-zA-Z0-9]+)/$', views.course_detail),
    url(r'^api/courses/enrollment/course/(?P<cID>[a-zA-Z0-9]+)/$',views.enroll_course_detail),
    url(r'^api/courses/enrollment/(?P<cID>[a-zA-Z0-9]+)/(?P<sID>[A-Za-z]{2,3}[\d]{4})/$',views.enroll_detail),
    
]