#! /usr/bin/env python
# -*- coding: utf-8 -*-
#========================================================================
#========================================================================
# File: _returnGeometry.py
#========================================================================
#========================================================================
# File used to retrieve geometry and a specific value from a vector file
# when the user select a point identify by lat and long into the map.
#========================================================================

#from mdlFunctions import _writeTrace
#import sys
from mdlFunctions import _returnDatasetAttributes
from mdlFunctions import logger
from mdlFunctions import queryFeature
from mdlFunctions import returnVariableFeature
from mdlFunctions import strGEPSGF4326Proj
from mdlFunctions import strGEPSGF900913Proj
import cgi
import cgitb
import json


cgitb.enable()


def main():
    result=''
    # reads input parameters
    form   = cgi.FieldStorage()
    # latitude and longitude values
    arrayParams = {}
    # latitude and longitude values
    arrayParams["txtLLat"]=float(form.getfirst("lat"))
    arrayParams["txtULat"]=float(form.getfirst("lat"))
    arrayParams["txtLLon"]= float(form.getfirst("lon"))
    arrayParams["txtRLon"]= float(form.getfirst("lon"))
    # layer name
    arrayParams["layerCrop"]= (form.getfirst("layerCrop"))
    # date value
    try:
        arrayParams["strDate"]= (form.getfirst("strDate"))
    except:
        arrayParams["strDate"]=''

    strError=''
    response={}
    if (arrayParams["layerCrop"]==None):
        response["id"]=''
        response["geometry"]=''
        response["label"]=''
        response["projection"]=''
    else:
        # return dataset feature
        arrayFName=returnVariableFeature(arrayParams["layerCrop"])
        # return dataset attributes
        arrayVDataset=_returnDatasetAttributes(arrayFName["id"],arrayFName["type"])
        # return geometry
        #print arrayFName
        #print arrayVDataset
        result=queryFeature(arrayFName,arrayVDataset,arrayParams,'','the_geom','')

        resultGeom='';
        if (result["result"] == 1):
            resultGeom=result["value"]

            # query vector shapefile and retrieve the value
            result=queryFeature(arrayFName,arrayVDataset,arrayParams,'',arrayFName["returnid"],'')
            resultID=''
            if (result["result"] == 1):
                resultID=result["value"]
                # output google projection
                if (arrayVDataset["serverType"]=="MAPSERVER"):
                    strToProj=strGEPSGF900913Proj;
                else:
                    strToProj=strGEPSGF4326Proj;

                response["id"]=resultID
                response["geometry"]=resultGeom
                response["label"]=arrayFName["returnlabel"]
                response["projection"]=strToProj

            else:
                strError=result["error"]

        else:
            strError=result["error"]
    if (strError == ""):
        response["error"]=''
        response["result"]='1'
    else:
        response["error"]=strError
        response["result"]='0'

    print(json.JSONEncoder().encode(response))


if __name__ == "__main__":

    print "Content-type: application/json"
    print

    try:
        main()
    except:
        #_writeTrace(str(sys.exc_info()))
        strError='There was an error with the request. Please, try again.'
        logger.exception(strError)
        response={'result': 0, 'error': strError}
        print(json.JSONEncoder().encode(response))
