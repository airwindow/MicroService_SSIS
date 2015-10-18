from django.conf.urls import url
from courses import views

urlpatterns = [
    url(r'^courses/$', views.course_list),
    #url(r'courses/enrollment/$', views.enroll_list),
    #url(r'^', views.student_list),
    url(r'^courses/(?P<cID>[a-zA-Z0-9]+)/$', views.course_detail),
    #url(r'courses/enrollment/student/(?P<sID>[a-zA-Z0-9]+)/$',views.enroll_student_detail),
    #url(r'courses/enrollment/course/(?P<cID>[a-zA-Z0-9]+)/$',views.enroll_course_detail),
    #url(r'courses/enrollment/(?P<sID>[a-zA-Z0-9]+)/(?P<cID>[a-zA-Z0-9]+)/$',views.enroll_double_detail),
    
]