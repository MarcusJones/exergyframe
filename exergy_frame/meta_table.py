#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B. 
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
from __future__ import division    
import logging.config
from utility_inspect import get_self, get_parent
import unittest
from config import *
from utility_excelOLD import ExtendedExcelBookAPI, ExcelBookRead
import os

#===============================================================================
# Code
#===============================================================================



def getDescriptionsOut(descriptionsFilePath):
    # descriptionsFilePath is an excel file with a proper "Descriptions" sheet
    parametersBook = ExcelBookRead(descriptionsFilePath)
    descriptionsTable = parametersBook.get_table_literal("Descriptions",1,None,0,None)
    #print descriptionsTable
    descriptions = list()
    #print descriptionsTable
    for row in descriptionsTable[1:]:

        if row[0] and row[3]:
            try:
                row[2] = int(row[2])
                row[2] = str(row[2])
            except:
                print "This row fails", row
                raise
            row = [str(item) for item in row]
            #print row
            descriptions.append((tuple(row[:3]), row[3]))
    
    
    logging.info("Descriptions added for {} points".format(len(descriptions)))

    #descriptions = dict(descriptions)
    return descriptions

def getDescriptionsBal(descriptionsFilePath,sheetName):
    # descriptionsFilePath is an excel file with a proper "Descriptions" sheet
    parametersBook = ExtendedExcelBookAPI(descriptionsFilePath)
    descriptionsTable = parametersBook.get_table_literal(sheetName,1,200,1,4)
    descriptions = list()
    for row in descriptionsTable[1:]:
        if row[0]:
            try:
                vals = row[0].split("_")
                vals = [str(item) for item in vals]
                vals = vals + [str(row[1])]
                print vals
                descriptions.append(vals)
            except:
                raise Exception("This row fails: \n {}".format(row))                
        
    logging.info("Descriptions added for {} points".format(len(descriptions)))

    #descriptions = dict(descriptions)
    return descriptions

def getDescriptionsZoneNames(descriptionsFilePath,sheetName):
    # descriptionsFilePath is an excel file with a proper "Descriptions" sheet
    parametersBook = ExtendedExcelBookAPI(descriptionsFilePath)
    descriptionsTable = parametersBook.get_table_literal(sheetName,1,200,1,2)
    descriptions = list()
    for row in descriptionsTable[1:]:
        if row[0]:
            try:
                row[0] = int(row[0])
                row = [str(item) for item in row]
                descriptions.append(row)
            except:
                print "This row fails: \n {}".format(row)
                raise
                                
        
    logging.info("Descriptions added for {} points".format(len(descriptions)))

    #descriptions = dict(descriptions)
    return descriptions

def getSearchIndexes(excelFilePath):
    # descriptionsFilePath is an excel file with a proper "Descriptions" sheet
    wb = ExcelBookRead(excelFilePath)
    sheetName = "Search1"
    searchIdxTable = wb.get_table_all(sheetName)
    print searchIdxTable
    logging.info("".format())

    
    return searchIdxTable


#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    @unittest.skip("")
    def SKIPtest010_TrnsysOutDesc(self):
        print "**** TEST {} ****".format(get_self())
        
        #descFilePath = FREELANCE_DIR + r"\TRNSYSlib\"
        #getDescriptions()
    @unittest.skip("")
    def Skiptest010_TrnsysBalDesc(self):
        print "**** TEST {} ****".format(get_self())
        
        descFilePath = FREELANCE_DIR + r"\TRNSYSlib\BalanceDescriptions.xls"
        #getDescriptions()
        sheetName = "Solar balance 901"
        
        print getDescriptionsBal(descFilePath,sheetName)
    
    @unittest.skip("")
    def test010_TrnsysZoneNames(self):
        print "**** TEST {} ****".format(get_self())
        
        descFilePath = os.getcwd() + r"\..\..\test files\ZoneNames.xlsx"
        
         
        #getDescriptions()
        sheetName = "Sheet1"
        
        print getDescriptionsZoneNames(descFilePath,sheetName)
    
    def test050_getSearchIDX(self):
        print "**** TEST {} ****".format(get_self())
        
        wbPath = os.getcwd() + r"\..\..\test files\testingAll.xlsx"
        
        print getSearchIndexes(wbPath)
        
                
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())
    
    #print FREELANCE_DIR
    
    unittest.main()
        
    logging.debug("Finished _main".format())
    