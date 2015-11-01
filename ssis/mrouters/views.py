from django.shortcuts import render

from mrouters.tasks import route_request

# Create your views here.
def route(request):
    return route_request(request)
