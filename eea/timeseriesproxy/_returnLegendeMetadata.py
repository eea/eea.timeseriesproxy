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
from mdlFunctions import _writeTrace
from mdlFunctions import returnVariableFeature
import cgi
import cgitb
import json
import sys

cgitb.enable()

print "Content-type: application/json"
print


response={}
strLegend='';

try:

	# read from input parameters
	form = cgi.FieldStorage()
	strCoverage = form.getfirst("coverage")
	strDateCoverage = form.getfirst("dateCoverage")

	# return dataset features
	arrayFName=returnVariableFeature(strCoverage)
	# return dataset values from GN
	arrayVDataset=_returnDatasetAttributes(arrayFName["id"],arrayFName["type"])

	# retunr Legend image of getLegend using WMS
	strLegend=_returnLegendString(arrayFName,arrayVDataset,strDateCoverage);

	# response
	response["description"]=arrayFName["description"]
	response["legendLink"]=strLegend
	#response["metadataLink"]=_returnMetadataLink(arrayFName["id"])
	response["id"]=arrayFName["id"]
	response['result']=1;
	response['error']='';
	# print the output json array
	print(json.JSONEncoder().encode(response))

except:
	_writeTrace(str(sys.exc_info()))
	strError='There was an error with the request. Pleae, try again.'
	response={'result': 0, 'error': strError}
	print(json.JSONEncoder().encode(response))
