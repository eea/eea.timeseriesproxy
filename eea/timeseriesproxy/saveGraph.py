#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" File used to publish a graph into a pdf file.
"""

from fpdf import FPDF
from mdlFunctions import _returnDatasetAttributes
from mdlFunctions import _returnHttpAddress
from mdlFunctions import _returnIniValue
from mdlFunctions import _returnMetadataAdditionalInfo
from mdlFunctions import _returnMetadataLink
from mdlFunctions import _returnPdfCopyright
from mdlFunctions import _returnTempDirectory
from mdlFunctions import _returnUniqueFilename
from mdlFunctions import logger
from mdlFunctions import returnVariableFeature
import base64
import cgi

# import datetime
# import os
# import socket
#from mdlFunctions import _writeTrace
#from mdlFunctions import naive_unicode_fixer
#import HTMLParser
#import sys


def main():
    # reads input parameters
    form = cgi.FieldStorage()
    #h = HTMLParser.HTMLParser()

    data = form.getfirst("data")

    strParams = form.getfirst("strParams")

    pos = data.find(",")

    data = data[pos + 1:]

    arrayParams = strParams.split('<%%>')
    data = base64.b64decode(data)

    # output directory
    strOutputDirectory = _returnTempDirectory(0)
    # return filename
    strName = _returnUniqueFilename()
    # png and pdf extensions
    strOutFilenamePNG = strName + '.png'
    strOutFilenamePDF = strName + '.pdf'
    # open png file for writing
    f = open(strOutputDirectory + strOutFilenamePNG, 'w')
    f.write(data)
    f.close()
    # parameters

    # print arrayParams[1]
    # strText=arrayParams[1].encode("utf-8")

    # print strText
    # arrayParams[1]=h.unescape(arrayParams[1])
    #arrayParams[1]=arrayParams[1].replace("<br>", ", ");
    #arrayParams[1]=arrayParams[1].replace("Â", "");

    # variables
    arrayVars1 = arrayParams[2].split('#')
    arrayVars2 = arrayParams[3].split('#')

    # pdf istance
    pdf = FPDF()
    # add page
    pdf.add_page()

    #pdf.add_font('Arial', '', r'/var/lib/opengeo/geoserver/styles/ArialSansCondensed.ttf', uni=True)
    #pdf.set_font('Arial', '', 14)

    pdf.set_font('Arial', 'B', 16)
    cont = 0
    # add title
    strTitle = _returnIniValue('PDF_CONFIGURATION', 'PDF_TITLE')
    pdf.cell(200, 10, txt=strTitle, ln=1, align="L")
    pdf.set_font('Arial', '', 16)
    strHttp = _returnHttpAddress()
    # add ce ll for address
    pdf.cell(200, 10, strHttp, 0, 1, 'L')
    pdf.ln(10)
    cont = cont + 10
    # add cell for operation
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 0, 'Operation: ')
    pdf.ln(5)
    cont = cont + 5
    pdf.set_x(15)
    # add cell for coordinates
    # pdf.set_font('Arial','',12)
    pdf.cell(0, 0, arrayParams[0].decode('UTF-8'))
    pdf.ln(5)
    cont = cont + 5
    # add cell for coordinates
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 0, 'Coordinates: ')
    pdf.ln(5)
    cont = cont + 5
    pdf.set_x(15)
    # pdf.set_font('Arial','',12)
    pdf.cell(0, 0, arrayParams[1].decode('UTF-8'))

    #pdf.write(8, text)
    pdf.ln(5)
    cont = cont + 5
    pdf.set_font('Arial', '', 12)
    # variables list
    pdf.cell(0, 0, 'Variables Y1: ')
    pdf.ln(5)
    cont = cont + 5
    strAdditionalInfo = ''
    strTextCopyright = ''
    for value in arrayVars1:
        if (value != ""):
            arrayFName = returnVariableFeature(value)

            arrayVDataset = _returnDatasetAttributes(
                arrayFName["id"], arrayFName["type"])
            pdf.set_font('Arial', '', 12)
            strAdd = arrayFName["description"].decode('UTF-8')
            if (arrayVDataset["unit"] != ""):
                strAdd += ' (' + arrayVDataset["unit"].decode('UTF-8') + ')'

            pdf.set_x(15)
            pdf.cell(0, 0, strAdd)
            # for each variable add a description
            pdf.ln(5)
            cont = cont + 5
            # save the copyright for each variable in order to put the text
            # after the graph
            strTextCopyright += '\n\n' + strAdd + '\n' + \
                _returnPdfCopyright(arrayFName["id"])

            strAdditionalInfo += _returnMetadataAdditionalInfo(
                arrayFName["id"])
            strAdditionalInfo += '\n\nMetadata link: \n' + \
                _returnMetadataLink(arrayFName["id"])

    blnPrimaVolta = 1

    for value in arrayVars2:
        if (value != ""):
            if (blnPrimaVolta == 1):
                blnPrimaVolta = 0
                pdf.cell(0, 0, 'Variables Y2: ')
                pdf.ln(5)

            pdf.set_x(15)
            arrayFName = returnVariableFeature(value)
            arrayVDataset = _returnDatasetAttributes(
                arrayFName["id"], arrayFName["type"])
            pdf.set_font('Arial', '', 12)
            strAdd = arrayFName["description"].decode('UTF-8')
            if (arrayVDataset["unit"] != ""):
                strAdd += ' (' + arrayVDataset["unit"].decode('UTF-8') + ')'

            pdf.cell(0, 0, strAdd)
            # for each variable add a description
            pdf.ln(5)
            cont = cont + 5
            # save the copyright for each variable in order to put the text
            # after the graph
            strTextCopyright += '\n\n' + strAdd + '\n' + \
                _returnPdfCopyright(arrayFName["id"])
            strAdditionalInfo += '\n\n' + \
                _returnMetadataAdditionalInfo(arrayFName["id"])
            strAdditionalInfo += '\n\nMetadata link: \n' + \
                _returnMetadataLink(arrayFName["id"])
    # add graph image
    pdf.image(strOutputDirectory + strOutFilenamePNG,
              10, cont + 40, 180, 120, 'PNG')
    # add copyright
    if (strTextCopyright != ""):
        pdf.ln(130)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 0, 'Use limitation: ')
        pdf.ln(1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(180, 5, strTextCopyright.decode('UTF-8'))
        strHTTPOutputDirectory = _returnTempDirectory(1)
    pdf.ln(5)
    if (strAdditionalInfo != ""):
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(180, 5, strAdditionalInfo.decode('UTF-8'))
        strHTTPOutputDirectory = _returnTempDirectory(1)
    pdf.ln(5)

    pdf.output(strOutputDirectory + strOutFilenamePDF, 'F')
    # print and return the output link
    print strHTTPOutputDirectory + strOutFilenamePDF


if __name__ == "__main__":
    try:
        print "Content-Type: text/plain;charset=utf-8"
        print

        main()
    except:
        #_writeTrace(str(sys.exc_info()))
        logger.exception()
        print ""
