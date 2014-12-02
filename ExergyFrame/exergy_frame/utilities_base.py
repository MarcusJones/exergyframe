#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest


#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")



#----- Input and output
def display(df):
    pd.set_option('display.width', 5000)
    print(df)

def read_excel(path):
    raise
    writer = pd.ExcelWriter(path)
    for n, df in enumerate(list_frames):
        df.to_excel(writer, sheet_name='sheet{}'.format(n),merge_cells = merge_cells)
        writer.save()
        logging.debug("Wrote {} to {}, Sheet {}".format(df, path, sheet_name))

def read_pickle(path):
    return pd.read_pickle(path)

def write_dict_to_excel(df_dict,path, merge_cells = True):
    """ Writes a name - df dictionary to an excel workbook
    """

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for name,df in df_dict.iteritems():
        t0 = time.time()
        df.to_excel(writer, sheet_name=name, merge_cells = merge_cells)
        t1 = time.time()
        total = t1-t0
        logging.debug("Wrote frame size {}, Sheet {}, {} seconds".format(df.shape, name,total))
    writer.save()
    logging.debug("Wrote {} frames to {}".format(len(df_dict), path))


def datetime2matlabdn(dt):
    ord = dt.toordinal()
    mdn = dt + datetime.timedelta(days = 366)
    frac = (dt-datetime.datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
    datenum = mdn.toordinal() + frac
    return datenum

def write_matlab_frame(frame,path,name = 'df'):
    #print(frame.index)
    mdict = {}

    # First get the datetime64 from the pandas frame as a regular datetime
    index = np.array(frame.index.values)


    mdict['index'] = index
    mdict['data'] = frame.values

    # Header come as a list of tuples
    headers = frame.columns.values
    if len(headers.shape) == 1:
        mdict['headers'] = np.array([headers], dtype=np.object)

    elif len(headers.shape) == 2:
        # Convert to a true 2D list for numpy
        headers = [list(item) for item in headers]
        headers = np.array(headers, dtype=np.object)

        mdict['headers'] = headers

    #print(mdict['headers'])
    #print(type(mdict['headers']))
    #raise
    if len(frame.columns.names) > 1:
        mdict['headerDef'] = np.array(frame.columns.names, dtype = np.object)
    else:
        mdict['headerDef'] = np.array('Header', dtype = np.object)

    sio.savemat(path, {name: mdict})

    logging.debug("Saved frame {} to {}".format(frame.shape, path))


def write_matlab_tseries(frame,path,name):
    #print(frame.index)
    mdict = {}

    # First get the datetime64 from the pandas frame as a regular datetime
    time_col = pd.to_datetime(frame.index.values)


    time_col = np.array([datetime2matlabdn(dt) for dt in time_col])

    mdict['time'] = time_col
    mdict['data'] = frame.values

    # Header come as a list of tuples
    headers = frame.columns.values
    # Convert to a true 2D list for numpy
    headers = [list(item) for item in headers]
    headers = np.array(headers, dtype=np.object)
    headers = headers.T
    mdict['headers'] = headers

    mdict['headerDef'] = np.array(frame.columns.names, dtype = np.object)

    sio.savemat(path, {name: mdict})

    logging.debug("Saved time series {} to {}".format(frame.shape, path))

def write_pickle_one(frame, path):
    frame.to_pickle(path)
    logging.debug("Wrote frame size {} to {}".format(frame.shape, path))

def write_excel_one(frame, path, sheet_name="Sheet1", merge_cells = True):
    """Writes a single data frame to a single sheet of an excel file
    """
    t0 = time.time()
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    
    #print(frame.data_frame)
    #print(frame.header_frame)
    #raise
    frame.to_excel(writer, sheet_name=sheet_name, merge_cells = merge_cells)
    writer.save()
    t1 = time.time()
    total = t1-t0
    logging.debug("Wrote frame size {} to {}, Sheet {}, {} seconds".format(frame.shape, path, sheet_name,total))


def write_excel_multiple(list_frames, path, sheet_name=None, merge_cells = True):
    """Takes a list of data frames
    Writes each one to their own sheets in excel
    """
    #    SEE write_dict_to_excel
    raise
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for n, df in enumerate(list_frames):
        t0 = time.time()
        df.to_excel(writer, sheet_name='sheet{}'.format(n),merge_cells = merge_cells)
        writer.save()
        t1 = time.time()
        total = t1-t0
        logging.debug("Wrote {} to {}, Sheet {}, {} seconds".format(df, path, sheet_name,total))


#----- Masking and querying

def get_mask_regex(frame, label, pattern):
    """On a column based multi-indexed DataFrame
    return a boolean mask over the columns of the data frame in the label
    To be used finally as a df.iloc[:,mask]
    """
    header_row = frame.columns.get_level_values(label)
    regex = re.compile(pattern)
    mask = np.array([bool(re.search(regex, head)) for head in header_row])
    assert(mask.any()), "Mask did not match items in {} headings".format(label)
    logging.debug("Masking returned '{}' columns".format(sum(mask)))
    return mask

def get_mask(frame, label, match_value):
    """On a column based multi-indexed DataFrame
    return a boolean mask over the columns of the data frame
    To be used finally as a df.iloc[:,mask]
    """
    return frame.columns.get_level_values(label) == match_value

def apply_col_mask(frame, mask):
    return frame.iloc[:,mask]

def my_sum(series):
    return np.sum(series)

def sum_rows(df,units_row_label = None, column_title = None):
    # Get existing multiindex
    names = df.columns.names
    vals = df.columns.values.tolist()
    # Add the column labels
    if not column_title:
        column_title = "Summed"

    new_column_label = [column_title for head in df.columns[0]]

    if units_row_label:
        units_row = df.columns.get_level_values(units_row_label)

        assert(util_gen.checkEqual(units_row)), "Inconsistent units {}".format(set(units_row))
        units = list(set(units_row))[0]
        units_position = df.columns.names.index(units_row_label)
        new_column_label[units_position] = units

    #print(new_column_label)
    vals = vals + [new_column_label]
    #print(vals)
    new_mi = pd.MultiIndex.from_tuples(tuples = vals, names=names)

    # First, generate the resulting column and append it
    df.loc[:,'Temp'] =  df.apply(my_sum, 1)

    # Then replace the existing mi
    df.columns = new_mi


    return df




    #df.loc[:,'sum_col'] = df.apply(my_sum, 1)




    #print(df)
    #print(df['asdf'])
    #print(df.iloc[:,:5])


    #print(df.head())
    raise
    return df

# ------
def rename_index_inplace(df,old,new):
    assert(old in df.index)
    df.rename(index={old : new},inplace=True)

def rename_columns_inplace(df,old,new):
    assert(old in df.columns)
    df.rename(columns={old : new},inplace=True)

def drop_missing_cols(df1,df2):
    # Gets the intersection of columns in frame 1 and 2
    # Drops all columns not in this intersected set


    #print(df1.columns)
    #print(df2.columns)
    set1 = set(df1.columns)
    set2 = set(df2.columns)
    intersec = set1 & set2
    logging.debug("df1 has {} columns, df2 has {} columns, intersection is size {}".format(len(set1),len(set2),len(intersec)))

    # drop in df1


    diff1 = set1 - set2
    logging.debug("df1 - df2 = {}".format(diff1))
    df1 = df1.drop(diff1,axis =1 )

    diff2 = set2 - set1
    logging.debug("df2 - df1 = {}".format(diff2))
    df2 = df2.drop(diff2,axis =1 )

    #print(set1 & set2)
    return(df1,df2)

def reorder_columns(data_frame,head_frame):
    #print(set(data_frame.columns))
    #print(set(head_frame.columns))
    #print(set(data_frame.columns)==set(head_frame.columns))
    assert(set(data_frame.columns)==set(head_frame.columns)), "The columns must at least have the same elements"
    assert(list(data_frame.columns) != list(head_frame.columns)), \
           "Data and head columns are already exactly the same\nData: {}\nHead: {}".format(data_frame.columns,head_frame.columns)

    df_unshuffled = data_frame.reindex(index = data_frame.index, columns = head_frame.columns)
    logging.debug("Re-ordered columns in data to match header".format())

    return df_unshuffled



def create_header_frame(df,id_row=None):
    """
    The columns store the id
    """
    raise
#     if not id_row:
#         df.loc['id'] = range(n_cols)
#         #print(df)
#         logging.debug("Added an id row to the frame")
#     else:
#         rename_index_inplace(df,)
#
    return df



#===============================================================================
# Unit testing
#===============================================================================

class DesignSpaceBasicTests(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(whoami())
        myLogger.setLevel("CRITICAL")
        print("Setup")
        myLogger.setLevel("DEBUG")

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))

