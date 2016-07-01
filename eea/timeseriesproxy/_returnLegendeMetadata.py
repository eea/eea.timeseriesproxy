#! /usr/bin/env python
# -*- coding: utf-8 -*-
#========================================================================
#========================================================================
# File: _returnLegendeMetadata.py
#========================================================================
#========================================================================
# File used to retrieve Legend and Metadata for a specific layer.
#========================================================================


from mdlFunctions import _returnDatasetAttributes
from mdlFunctions import _returnLegendString
from mdlFunctions import returnVariableFeature
from mdlFunctions import logger
import cgi
import cgitb
import json

#from mdlFunctions import _writeTrace
#import sys


def main():
    response = {}
    strLegend = ''

    # read from input parameters
    form = cgi.FieldStorage()
    strCoverage = form.getfirst("coverage")
    strDateCoverage = form.getfirst("dateCoverage")

    # return dataset features
    arrayFName = returnVariableFeature(strCoverage)
    # return dataset values from GN
    arrayVDataset = _returnDatasetAttributes(
        arrayFName["id"], arrayFName["type"])

    # retunr Legend image of getLegend using WMS
    strLegend = _returnLegendString(arrayFName, arrayVDataset, strDateCoverage)

    # response
    response["description"] = arrayFName["description"]
    response["legendLink"] = strLegend
    # response["metadataLink"]=_returnMetadataLink(arrayFName["id"])
    response["id"] = arrayFName["id"]
    response['result'] = 1
    response['error'] = ''
    # print the output json array
    print(json.JSONEncoder().encode(response))


if __name__ == "__main__":

    cgitb.enable()

    try:
        print "Content-type: application/json"
        print
        main()
    except:
        #_writeTrace(str(sys.exc_info()))
        strError = 'There was an error with the request. Pleae, try again.'
        logger.exception(strError)
        response = {'result': 0, 'error': strError}
        print(json.JSONEncoder().encode(response))
