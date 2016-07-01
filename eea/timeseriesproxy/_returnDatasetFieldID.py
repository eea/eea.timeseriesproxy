#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
File used to retrieve geometry and a specific value from a vector file
when the user select a point identify by lat and long into the map.
"""

from mdlFunctions import _returnDatasetIndicatorGroup
from mdlFunctions import _returnEncodedArrayLayers
from mdlFunctions import _returnGraphSettings
from mdlFunctions import _returnGroupFromArrayLayers
from mdlFunctions import _returnMetadataLink
from mdlFunctions import _returnOwnerFromArrayLayers
from mdlFunctions import _returnReplaceDatasetIndicator
from mdlFunctions import logger
import cgi
import cgitb
import json

#from mdlFunctions import _writeTrace
#import sys


def main():
    response = {}
    # reads input parameters
    form = cgi.FieldStorage()
    # specific dataset name
    strReturn = str(form.getfirst("strReturn"))
    if (strReturn == "None"):
        strReturn = ""
    # blnOnlyValues
    blnOnlyValues = int(form.getfirst("blnOnlyValues"))
    #

    strType = (form.getfirst("strType"))
    # return array list from a specific section of ini file

    arrayLayers = _returnEncodedArrayLayers(strType, strReturn, blnOnlyValues)

    # return owner
    arrayOwner = _returnOwnerFromArrayLayers(arrayLayers, 0)

    if (strReturn == ""):
        arrayOwnerGraph = _returnOwnerFromArrayLayers(arrayLayers, 1)

    # return group
    arrayGroups = _returnGroupFromArrayLayers(arrayLayers)
    arrayDatasetIndicatorGroup = _returnDatasetIndicatorGroup()
    arrayReplaceDatasetIndicator = _returnReplaceDatasetIndicator()

    # json response
    response = {'result': 1, 'error': ''}
    # dataset availables
    response["data"] = arrayLayers

    # owners list
    arrayOwner.sort(reverse=False)
    response["owner"] = arrayOwner

    response["datasetIndicatorGroup"] = arrayDatasetIndicatorGroup
    response["replaceDatasetIndicator"] = arrayReplaceDatasetIndicator

    # groups list
    arrayGroups.sort(reverse=False)
    response["groups"] = arrayGroups
    response["GNpath"] = _returnMetadataLink('')
    response["ownerGraph"] = ""
    if (strReturn == ""):
        arrayOwnerGraph.sort(reverse=False)
        response["ownerGraph"] = arrayOwnerGraph

    # the first time returns also graph configurations parameters
    if (blnOnlyValues == 1):
        response["graphSettings"] = _returnGraphSettings()

    print(json.JSONEncoder().encode(response))


if __name__ == "__main__":

    cgitb.enable()

    print "Content-type: application/json"
    print
    try:
        main()
    except:
        # _writeTrace(str(sys.exc_info()))
        strError = 'There was an error with the request. Please, try again.'
        logger.exception(strError)
        response = {'result': 0, 'error': strError}
        print(json.JSONEncoder().encode(response))
