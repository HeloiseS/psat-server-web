"""
Author: Ken Smith
Last Update: 2024-02-09

Description
-----------
Define needed mappings between URLs and our views. 

Notes for N00bs
---------------
* what is "routers" from rest_framework

The routers module from the Django REST Framework is used to automatically generate URL patterns for viewsets 

* What are "URLs" in Django?
The URLs are one of the key elements of the Django framework (Models, Views, URLs, Templates). The URLs, define mappings between URL patterns and 
view functions/classes.

* what are views?
The Views in the Django framework are a bunch of functions and classes that take in a request from a client and create a respinse by processing input 
amd queryinng the database. The response can be HTML (for webpages) or JSON/XML format for APIs. Here it's probs the latter :)

"""

from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # URL pattern for the ConeView API endpoint
    # when a request ins made to /api/cone/ Django will call the `as_view()` method in the `ConeView()` class in views.py
    path('api/cone/',                  views.ConeView.as_view()),
    path('api/objects/',               views.ObjectsView.as_view()),
    path('api/objectlist/',            views.ObjectListView.as_view()),
    path('api/vraprobabilities/',      views.VRAProbabilitiesView.as_view()),
    path('api/auth-token/',            obtain_auth_token, name='auth_token'),
]
