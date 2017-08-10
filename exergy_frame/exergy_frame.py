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
# Standard
from __future__ import division
from __future__ import print_function

#from config import *

import logging
#import unittest

#import os, re, csv, random
import pandas as pd
#import numpy as np
#import scipy as sp

#import UtilityGeneral as util_gen

#import datetime as datetime

#===============================================================================
# Code
#===============================================================================
raise Exception("Obselete, SEE util_pandas")
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
    

