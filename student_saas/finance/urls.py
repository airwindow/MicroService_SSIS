from django.conf.urls import url
from finance import views


urlpatterns = [
	url(r'^api/finance/tenant/$', views.tenant_list),
    url(r'^api/finance/tenant/(?P<tid>[0-9]{9})/$', views.tenant_detail),
	url(r'^api/finance/attribute/(?P<tid>[0-9]{9})/$', views.tenant_attribute_list),
	url(r'^api/finance/attribute/(?P<tid>[0-9]{9})/(?P<attr_name>.+)/$', views.tenant_attribute),
    url(r'^api/finance/student/(?P<tid>[0-9]{9})/$', views.student_finance_list),
    url(r'^api/finance/student/(?P<tid>[0-9]{9})/(?P<ssn>[0-9]{9})/$', views.student_finance),
]