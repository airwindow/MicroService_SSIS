from django.conf.urls import url
from students import views

urlpatterns = [
    url(r'^students/$', views.student_list),
    # url(r'^', views.student_list),
    # url(r'^students/(?P<pk>[0-9]+)/$', views.snippet_detail),
]