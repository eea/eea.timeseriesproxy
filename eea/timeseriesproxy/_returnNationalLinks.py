#! /usr/bin/env python
# -*- coding: utf-8 -*-
#========================================================================
#========================================================================
# File: _returnNationalLinks.py
#========================================================================
#========================================================================
# File used to retrieve all common dates for a list of coverages.
#========================================================================


from mdlFunctions import _returnNationalLinks
from mdlFunctions import _writeTrace
import cgi
import cgitb
import json
import sys


cgitb.enable()


print "Content-type: application/json"
print
try:

	# reads input parameters
	form   = cgi.FieldStorage()
	# from latitude and longiture as input parameters return national and meteo links
	lat= float(form.getfirst("lat"))
	lon= float(form.getfirst("lon"))

	# return national and meteo links for the selected point
	response=_returnNationalLinks(lat,lon);
	response["error"]=''
	response["result"]='1'
	print(json.JSONEncoder().encode(response))
except:
	_writeTrace(str(sys.exc_info()))
	strError='There was an error with the request. Pleae, try again.'
	response={'result': 0, 'error': strError}
	print(json.JSONEncoder().encode(response))



