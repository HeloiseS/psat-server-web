"""
Author: Ken Smith
Last Update: 2024-02-09 HFS

Description:
-----------

Notes for Ken
-------------
* Why is there only one serialiser?
So actually I think I remember you mentioning that currently the only way to "search" for stuff is a cone search. 
But I can't remember the why and the limitations and why the alternatives are.

Notes for N00bs
---------------
* What is a serialiser? 

In the context of an API a serialiser is a piece of code that formats data into a format that can be shared over the network e.g. JSON orXML
Usually another part of the API will interact with the database to get the data and then it is the serialisers job to turn that data into 
something that can be shared over the internet. 
On the other end you may have a _deserialiser_ that takes your JSON/XML data and puts it back into the format that goes into your database.
"""
import datetime
import re
import json
import requests
from django.db import IntegrityError
from django.db import connection
from datetime import datetime # TODO: why do we have this AND import datetime at the top? probably trumps the first one. 
# I am guessing that this short for gengisken utils. Which probably means I can't run this code without asking ken for his utils. 
from gkutils.commonutils import coneSearchHTM, FULL, QUICK, COUNT, CAT_ID_RA_DEC_COLS, base26, Struct
from rest_framework import serializers
import sys

#CAT_ID_RA_DEC_COLS['objects'] = [['objectId', 'ramean', 'decmean'], 1018]

REQUEST_TYPE_CHOICES = (
    ('count', 'Count'),
    ('all', 'All'),
    ('nearest', 'Nearest'),
)



class ConeSerializer(serializers.Serializer):
    """
    Serialiser to hand the cone search data. 
    """
    ra = serializers.FloatField(required=True)
    dec = serializers.FloatField(required=True)
    radius = serializers.FloatField(required=True)
    requestType = serializers.ChoiceField(choices=REQUEST_TYPE_CHOICES)

    def save(self):

        ra = self.validated_data['ra']
        dec = self.validated_data['dec']
        radius = self.validated_data['radius']
        requestType = self.validated_data['requestType']

        # Get the authenticated user, if it exists.
        userId = 'unknown'
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            userId = request.user

        # Check if the radius of the cone search is bat shit crazy 
        if radius > 1000:
            replyMessage = "Max radius is 1000 arcsec."
            info = {"error": replyMessage}
            return info

        replyMessage = 'No object found ra=%.5f dec=%.5f radius=%.2f' % (ra, dec, radius)
        info = {"error": replyMessage}

        # Is there an object within RADIUS arcsec of this object? - KWS - need to fix the gkhtm code!!
        # For ATLAS QUICK does not work because of the `dec` syntax error problem. Use FULL until I figure out what
        # needs to be fixed.
        # HFS: this piece of code is from ken's utils not a Django specific thing
        message, results = coneSearchHTM(ra, dec, radius, 'atlas_diff_objects', queryType=FULL, conn=connection, django=True)

        obj = None
        separation = None
        objectList = []
        
        if len(results) > 0:
            if requestType == "nearest":
                obj = results[0][1]['id']
                separation = results[0][0]
                info = {"object": obj, "separation": separation}
            elif requestType == "all":
                for row in results:
                    objectList.append({"object": row[1]["id"], "separation": row[0]})
                info = objectList
            elif requestType == "count":
                info = {'count': len(results)}
            else:
                info = {"error": "Invalid request type"}

        return info

