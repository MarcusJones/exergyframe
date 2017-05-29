
#% This function returns the enthalpy of the air from ASHRAE fundamentals
#% 2005 ASHRAE handbook "Fundamentals", chapter 6, equation 32 
#% Marcus Jones - July 2007 - from M.Sc. thesis
#% Marcus Jones - Novemeber 2009 - Update for AIT
#% 
#% T - Temperature [C]
#% W - asbsolute humidity [kg/kg]
#% EnthalpyAir - Enthalpy of moist air [kJ/kg]
#
#function EnthalpyAir=enthalpyMoistAir(T,W)
#
#EnthalpyAir = 1.006.*T + W.*(2501+1.805.*T);
#
#end

#===============================================================================
# Set up
#===============================================================================
from __future__ import division    
import logging.config
from utility_inspect import get_self, get_parent
import unittest
from config import *


def enthalpy(T,w):
    return 1.006*T + w*(2501+1.805*T)

def enthalpyFlow(T,w,mf):
    h = enthalpy(T,w) # kJ/kg
    ef1 = h * mf # kJ/hr
    ef = ef1/3600 # kW
    return ef


def getEnthalpyFrames():
    #===========================================================================
    # Expand moist air state points
    #===========================================================================
    
    # Get the statepoints
    thisMask = xrg.idx("pointType",r"MoistAir")
    thisMask = xrg.evalIdx(finalFrame,thisMask)
    
    systemRow = xrg.findHeadRow(finalFrame,"system")
    numberRow = xrg.findHeadRow(finalFrame,"number")
    
    systemNames = finalFrame.headersArray[systemRow,thisMask]
    numbers =  finalFrame.headersArray[numberRow,thisMask]
    
    uniqueMoaPoints = set(zip(systemNames,numbers))
    
    def calculateEnthalpyFlow(tripleColumn):
        #print tripleColumn
        return enthalpyFlow(tripleColumn[:,0],tripleColumn[:,1],tripleColumn[:,2])
    
    enthalpyCols = list()
    for moaPoint in uniqueMoaPoints:
        fullMask = (
         xrg.idx("pointType",r"MoistAir") & 
         xrg.idx("system",moaPoint[0]) &
         xrg.idx("number",moaPoint[1])
         )
        thisEnthalpyCol = xrg.rowWiseFunction(finalFrame,fullMask,calculateEnthalpyFlow)
        print thisEnthalpyCol.headersArray
        thisEnthalpyCol.headersArray = np.array(
                                                [
                    ["hf"],
                    ["[kW]"],
                    [""],
                    [moaPoint[0]],
                    ["MoistAir"],
                    [str(moaPoint[1])],
                    [""],
                    [""],
                    [""],
                ])
        
        enthalpyCols.append(thisEnthalpyCol)
        #print xrg.evalIdx(finalFrame,fullMask)

    
#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    def test010_SimpleCreation(self):
        print "**** TEST {} ****".format(get_self())
        T = 22 #C
        w = 0.0093 # kg/kg
        mf = 50 # kg/hr
        print enthalpy(T,w), "kJ/kg"
        print enthalpyFlow(T,w,mf), "kW"
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
    