#! /usr/bin/env python
##!scl enable python27 bash
# -*- coding: utf-8 -*-
##!/opt/rh/python27/root/usr/bin/python

import os
import cgi
import cgitb
from owslib.wcs import WebCoverageService as w  
from owslib.wms import WebMapService
import numpy as np
import gdal
import ast
import sys
from gdalconst import *
from array import *
import time
from datetime import date
from mdlFunctions import _returnReplaceDatasetIndicator,_returnDatasetIndicatorGroup,_returnEncodedArrayLayers,_returnOwnerFromArrayLayers,_returnGroupFromArrayLayers,_returnMetadataLink,_returnGraphSettings,_writeTrace
import json

cgitb.enable()

print "Content-type: application/json"
print
print "aaa"


