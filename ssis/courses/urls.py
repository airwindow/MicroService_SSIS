from django.conf.urls import url
from courses import views

urlpatterns = [
    url(r'^api/courses/$', views.course_list),
    url(r'api/courses/enrollment/$', views.enroll_list),

    url(r'^api/courses/(?P<cID>[a-zA-Z0-9]+)/$', views.course_detail),
    url(r'api/courses/enrollment/student/(?P<sID>[a-zA-Z0-9]+)/$',views.enroll_student_detail),
    url(r'api/courses/enrollment/course/(?P<cID>[a-zA-Z0-9]+)/$',views.enroll_course_detail),
    url(r'api/courses/enrollment/(?P<sID>[a-zA-Z0-9]+)/(?P<cID>[a-zA-Z0-9]+)/$',views.enroll_detail),
    
]