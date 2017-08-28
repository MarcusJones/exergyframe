#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function
import logging
import time
import re 
import datetime

# External 
import pandas as pd
import numpy as np 
import scipy.io as sio

raise Exception("Obselete, SEE util_pandas, moved all code!")


# Old --- 
def read_excel(path):
    raise
    writer = pd.ExcelWriter(path)
    for n, df in enumerate(list_frames):
        df.to_excel(writer, sheet_name='sheet{}'.format(n),merge_cells = merge_cells)
        writer.save()
        logging.debug("Wrote {} to {}, Sheet {}".format(df, path, sheet_name))

def read_pickle(path):
    return pd.read_pickle(path)
