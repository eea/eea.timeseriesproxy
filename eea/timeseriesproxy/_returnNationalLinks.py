#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
File used to retrieve all common dates for a list of coverages.
"""

from mdlFunctions import _returnNationalLinks
from mdlFunctions import logger
import cgi
import cgitb
import json

#from mdlFunctions import _writeTrace
#import sys


def main():
    # reads input parameters
    form = cgi.FieldStorage()
    # from latitude and longiture as input parameters return national and
    # meteo links
    lat = float(form.getfirst("lat"))
    lon = float(form.getfirst("lon"))

    # return national and meteo links for the selected point
    response = _returnNationalLinks(lat, lon)
    response["error"] = ''
    response["result"] = '1'
    print(json.JSONEncoder().encode(response))


if __name__ == "__main__":
    cgitb.enable()

    print "Content-type: application/json"
    print

    try:
        main()
    except:
        #_writeTrace(str(sys.exc_info()))
        strError = 'There was an error with the request. Pleae, try again.'
        logger.exception(strError)
        response = {'result': 0, 'error': strError}
        print(json.JSONEncoder().encode(response))
