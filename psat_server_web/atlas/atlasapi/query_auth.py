"""
Author: Ken Smith
Last Edited: 2024-02-09 (HFS)

Description
-----------
Class to check that the query made has a valid token

Notes for N00bs
---------------
* What is a token?
A token is just a piece of data that authenticates the identify of the user making a request. 
"""

# Commented with the help of Chat GPT
from django.contrib.auth.models import User        # Importing the User model from Django's authentication system
from rest_framework import authentication          # Importing authentication classes from Django REST Framework
from rest_framework import exceptions              # Importing exceptions module from Django REST Framework
from re import match                               # Importing the match function from the regular expression module


# Defining a custom authentication class that extends TokenAuthentication provided by DRF
class QueryAuthentication(authentication.TokenAuthentication):
    
    # Overriding the authenticate method of TokenAuthentication
    def authenticate(self, request):
        # Extracting the token from the query parameters of the request
        token = request.query_params.get('token')
        
        # If token is not provided in the query parameters, return None indicating authentication failure
        if not token:
            return None
        
        # Checking if the token matches the specified format using a regular expression
        # This regular expression checks for ANY number of alphanumeric characters between the start and
        # end of the token - THIS JUST CHECKS THE FORMAT IS CORRECT.
        if not match("^\w+$", token):
            # If the token format is invalid, raise an AuthenticationFailed exception with an error message
            msg = 'Invalid token format.'
            raise exceptions.AuthenticationFailed(msg)
        
        # If the token format is valid, call the authenticate_credentials method to verify the token
        # TODO: [HFS 2024-02-09] NOT SURE HOW IT CHECKS THE TOKEN - DOES IT JUST HAVE A LIST OF VALID STRINGS?
        return self.authenticate_credentials(token)
