"""
Author: Ken Smith
Last Updated: 2024-02-09

Notes for N00bs
---------------
* Why are there two authentication classes in the ConeView class?
in a Django REST Framework view the authentication_classes specify which clases should be used to tdo the authenticification process. 
Both options will be used in turn. First the TokenAuthentification class (which is a default in Django) and if that doesn't work it will try the 
QueryAuthentication class which is a custom class that is defined in the query_auth module in this package. 

* HTTP request methods:
GET: retrieve data from the server .
POST: submit data to be processed by the server.
PUT: Update an existing resource on the server
PATCH: Partially update an existing resource on the server (??)
DELETE: Delete an existing resource on the server. 

"""

from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ConeSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .query_auth import QueryAuthentication

def retcode(message):
    """
    Return error code based on message. 
    """
    if 'error' in message: return status.HTTP_400_BAD_REQUEST
    else:                  return status.HTTP_200_OK

class ConeView(APIView):
    authentication_classes = [TokenAuthentication, QueryAuthentication]
    permission_classes = [IsAuthenticated]

    # Handler for GET requests (one of the standard HTTP request methods)
    def get(self, request):
        serializer = ConeSerializer(data=request.GET, context={'request': request})
        if serializer.is_valid():
            message = serializer.save()
            return Response(message, status=retcode(message))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle for the POST requests (another one of the standard HTTP request metods)
    def post(self, request, format=None):
        serializer = ConeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            message = serializer.save()
            return Response(message, status=retcode(message))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

