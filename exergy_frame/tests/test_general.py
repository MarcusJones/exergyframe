"""This is a testing module
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function
import os
import unittest
import random
import xlrd as xlrd
# Logging
LOGGING_CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), r'loggingNofile.conf')
import logging.config
logging.config.fileConfig(LOGGING_CONFIG_FILE)
my_logger = logging.getLogger()
my_logger.setLevel("DEBUG")

# External 
import nose
import pandas as pd

# Own
from utility_inspect import get_self, get_parent
import exergy_frame as xrg
#import utilities_base as util 

class test_frame(unittest.TestCase):
    def setUp(self):
        print("**** {} ****".format(get_self()))
        # This is random

        data_2d = list()

        for i in range(5):
            row = [random.randint(0,10) for i in xrange(4)]
            data_2d.append(row)

        # This is fixed
        self.data_2d = [[1, "Chicken", "A", 6.0], [6, 2, "B", 3], [0, 8, "C", 7.5], [10, 6, "D", 8], [8, 2, "E", 0]]

        self.headerDef = ["Attrib1","Xpos","Ypos"]

        self.headers = [
                   ["alpha","beta","charlie","delta"],
                   ["0","2","2","4"],
                   ["0","1","1","6"],
                   ]
        
        self.data_frame = pd.DataFrame(self.data_2d,)
        self.header_frame = pd.DataFrame(self.headers, index=self.headerDef)

    def test01_print(self):
        print("**** TEST {} ****".format(get_self()))

        print("\n-Headers-")
        print(self.header_frame)
        
        print("\n-Data-")        
        print(self.data_frame)

    def test02_creation(self):
        print("**** TEST {} ****".format(get_self()))
        df = xrg.create_frame(self.headerDef, zip(*self.headers), self.data_2d)
        print("\n-Assembled frame-")
        print(df)
        print("\n-Describe-")
        print(df.describe())
        print(df.dtypes)
    

class test_matsave(unittest.TestCase):
#class testFrame(unittest.TestCase):
    def setUp(self):
        print("**** {} ****".format(get_self()))
        # This is random
        
    def test01_load(self):
        print("**** {} ****".format(get_self()))
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        test_data_dir = os.path.abspath(curr_dir + r"\..\Example data")
        path_input_data1 = os.path.join(test_data_dir, r'Solar day.xlsx')
        
        path_output_excel =  os.path.join(test_data_dir, r'Solar day out.xlsx')
        print(path_input_data1)
        #xls = pd.ExcelFile(path_input_data1)
        book = xlrd.open_workbook(path_input_data1)
        sh = book.sheet_by_index(0)
        
        N_heads = 5
        
        data = []
        for col in range(sh.ncols):
            values = []
            for row in range(sh.nrows):
                values.append(sh.cell(row,col).value)
            data.append(values)

        labels = data.pop(0)
        labels = labels[:N_heads]
        index = data.pop(0)
        index = index[N_heads:]
        
        data = zip(*data)
        headers = data[:N_heads]
        headers = zip(*headers)
        data = data[N_heads:]
        
        print(labels)
        print(index)
        print(headers)
        print(data)
        
        df = xrg.create_frame(labels, headers, data)
        print(df)
        
        df.to_excel(path_output_excel,merge_cells=True)
        
        # Select columns
        mask_temp = xrg.get_mask(df, 'Type','T')
        mask_system = xrg.get_mask(df, 'System','Solar')
        mask_total = mask_temp & mask_system
        print(df.loc[:,mask_total])
        
        # Convert kj/hr to W
        mask_kjhr = xrg.get_mask(df, 'Units','kj/hr')
        
        def convert_kjhr_w(val):
            return val/3.6
        
        #df.loc[:,mask_kjhr] = df.loc[:,mask_kjhr].apply(convert_kjhr_w)
        #df.app
        xrg.convert_cols(df,'Units','kj/hr','W',convert_kjhr_w)
        
        print(df)
        
        #df.to_excel(path_output_excel,engine=r'io.excel.xlsx.writer',merge_cells=False)
        
        
    def test03_reshuffle(self):
        print("**** TEST {} ****".format(get_self()))
        # The original frames do not need to be re-ordered, so this raises an error
        self.assertRaises(AssertionError,reorder_columns,self.data_frame,self.header_frame)
        df_shuffled = self.data_frame.reindex(self.data_frame.index, [3,1,0,2])

        #df_unshuffled = df_shuffled.reindex(index = df_shuffled.index, columns = self.header_frame.columns)
        print(df_shuffled)
        print(reorder_columns(df_shuffled,self.header_frame))


    unittest.skipIf(1,"")
    def test01_print(self):
        print("**** TEST {} ****".format(get_self()))
        pth_root = r'C:\Projects\IDFout3\\'
        filename = r'Proposed 1 - HOTEL CENTRAL -   48.20 -   17.20 -    1.00 -  130.00'

        frame = pd.read_pickle(pth_root + filename + '.pck')

        write_matlab_tseries(frame,pth_root + filename + '.mat')
        #print(frame)
                
#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
               exit=False)
