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
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject
import os, re, csv, random
import pandas as pd
import numpy as np
import scipy as sp
import scipy.io as sio
import UtilityGeneral as util_gen
import time
import datetime as datetime

#===============================================================================
# Code
#===============================================================================

class ExergyFrame(object):
    """
    
    data_frame is a pandas data frame
    header_frame is a pandas data frame
    """
    

    def __init__(self,

                 data_frame,
                 header_frame,
                 name = None
                 ):
        raise Exception("Obselete, just use a multi index frame!")

        self.data_frame = data_frame
        self.header_frame = header_frame
        self.name = name
        assert(list(self.data_frame.columns) == list(self.header_frame.columns)), \
           "Data and head columns not exactly matched\nData: {}\nHead: {}".format(self.data_frame.columns,self.header_frame.columns)
           
        logging.info(self.summary_string)

    @property
    def summary_string(self):
        return "FRAME - {}, {} columns, {} data rows, {} head rows".format(
            self.name, self.header_frame.shape[1], len(self.data_frame), len(self.header_frame))

    @property
    def n_data_rows(self):
        return len(self.data_frame)

    @property
    def n_cols(self):
        return self.header_frame.shape[1]

    def return_multi_index(self):
        m_index = pd.MultiIndex.from_arrays(self.header_frame.values,names = self.header_frame.index)
        return pd.DataFrame(data = self.data_frame.values, index = self.data_frame.index, columns = m_index)
    
#===============================================================================
# Unit testing
#===============================================================================
unittest.skipIf(1,"")
class test_frame(unittest.TestCase):
#class testFrame(unittest.TestCase):
    def setUp(self):
        print("**** {} ****".format(whoami()))
        # This is random


        data_2d = list()

        for i in range(5):
            row = [random.randint(0,10) for i in xrange(4)]
            data_2d.append(row)

        # This is fixed
        data_2d = [[1, 10, 0, 6], [6, 2, 5, 3], [0, 8, 10, 7], [10, 6, 6, 8], [8, 2, 2, 0]]

        headerDef = ["Attrib1","Xpos","Ypos"]

        headers = [
                   ["alpha","beta","charlie","delta"],
                   ["0","2","2","4"],
                   ["0","1","1","6"],
                   ]

        self.data_frame = pd.DataFrame(data_2d,)
        self.header_frame = pd.DataFrame(headers, index=headerDef)

    unittest.skipIf(1,"")
    def test01_print(self):
        print("**** TEST {} ****".format(whoami()))
        print(self.header_frame)
        print(self.data_frame)

    unittest.skipIf(1,"")
    def test02_creation(self):
        print("**** TEST {} ****".format(whoami()))

        #this_frame = MyFrame(self.data_frame,self.header_frame)

    unittest.skipIf(1,"")
    def test03_reshuffle(self):
        print("**** TEST {} ****".format(whoami()))
        # The original frames do not need to be re-ordered, so this raises an error
        self.assertRaises(AssertionError,reorder_columns,self.data_frame,self.header_frame)
        df_shuffled = self.data_frame.reindex(self.data_frame.index, [3,1,0,2])

        #df_unshuffled = df_shuffled.reindex(index = df_shuffled.index, columns = self.header_frame.columns)
        print(df_shuffled)
        print(reorder_columns(df_shuffled,self.header_frame))

    unittest.skipIf(1,"")
    def test04_creation(self):
        print("**** TEST {} ****".format(whoami()))

        pass

class test_matsave(unittest.TestCase):
#class testFrame(unittest.TestCase):
    def setUp(self):
        print("**** {} ****".format(whoami()))
        # This is random

    unittest.skipIf(1,"")
    def test01_print(self):
        print("**** TEST {} ****".format(whoami()))
        pth_root = r'C:\Projects\IDFout3\\'
        filename = r'Proposed 1 - HOTEL CENTRAL -   48.20 -   17.20 -    1.00 -  130.00'

        frame = pd.read_pickle(pth_root + filename + '.pck')

        write_matlab_tseries(frame,pth_root + filename + '.mat')
        #print(frame)
        
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    logging.debug("Finished _main".format())

