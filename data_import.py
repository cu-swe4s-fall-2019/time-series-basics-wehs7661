import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import math
import copy


class ImportData:
    def __init__(self, data_csv, replace=False):
        """
        The initialization function import time and value entries from the .csv file.

        Parameters
        ----------
        
        data_csv : str
            the filename of the .csv file
        replace : bool
            whether to trigger the loop for examining if there are strings like 'high' or 'low' in the value column. Should be set as True if 'cgm_small.csv' is in the filename

        Returns
        -------
        None 
        """
        self._time = []
        self._value = []
        self._type = 0       # type = 0: sum the values in roundTimeArray
        self._err = False    # No ValueError is raised 

        if 'smbg' in data_csv or 'hr' in data_csv or 'cgm' in data_csv or 'basal' in data_csv:
            self._type = 1   # type = 1: average the values in roundTimeArray

        if 'cgm_small.csv' in data_csv:
            replace = True

        with open(data_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['time'] == '' or row['value'] == '':
                    print("Skipping the rows with imcomplete data...")
                if replace is True:
                    if row['value'] == 'low':
                        print("Replacing the string 'low' with 40 ...")
                        row['value'] = 40
                    if row['value'] == 'high':
                        print("Replacing the string 'high' with 300 ...")
                        row['value'] = 300

                try: 
                    dateutil.parser.parse(row['time'])
                except ValueError:
                    self._err = True
                    print('Wrong data type / bad input format of time')

                try: 
                    if (not math.isnan(float(row['value'])) and not math.isinf(float(row['value'])) and self._err == False):
                        self._time.append(datetime.datetime.strptime(row['time'], '%m/%d/%y %H:%M'))
                        self._value.append(int(row['value']))

                except ValueError:
                    print('Wrong data type / bad input format of value')
            f.close()

    def linear_search_value(self, key_time):
        """ 
        This function returns a list of value(s) associated with key_time. If the list is empty, return -1 and error message.

        Parameters
        ----------
        key_time : datetime object
            the time for finding the associated value

        Returns
        -------
        a list of value(s) associated with given key_time
        """
        vals = []
        for i in range(len(self._time)):
            if self._time[i] == key_time:
                vals.append(self._value[i])

        if (len(vals) == 0):
            print('No value associated with key_time found.')
            return -1
        return vals

    def binary_search_value(self,key_time):
        pass
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message

def roundTimeArray(obj, res):
    """
    This function creates a list of datetime entries and associated values with the times rounded to the 
    nearest rounding resolution (res).

    Parameters
    ----------
    obj : data_import.ImportData
        an ImportData object
    res : int
        the time resolution for rounding (units: minute)

    Returns
    -------
    result : zip object
        an iterable zip object of the lists of datetime entries and associated values
    """

    roundtime = copy.deepcopy(obj)
    rtime_list = []
    value_list = []
    for i in range(len(roundtime._time)):
        t = roundtime._time[i]
        discard = datetime.timedelta(minutes=t.minute % res)
        t -= discard
        if discard >= datetime.timedelta(minutes= res / 2):
            t += datetime.timedelta(minutes=res)
        roundtime._time[i] = t

    for i in range(len(roundtime._time)):
        if i == 0:
            rtime_list.append(roundtime._time[0])
        else:
            if roundtime._time[i] != roundtime._time[i - 1]:
                rtime_list.append(roundtime._time[i])
        search_vals = roundtime.linear_search_value(roundtime._time[i])
        if obj._type == 0:
            value_list.append(sum(search_vals))
        elif obj._type == 1:
            value_list.append(sum(search_vals)/len(search_vals))

    return zip(rtime_list, value_list)

    


def printArray(data_list, annotation_list, base_name, key_file):
    pass
    # combine and print on the key_file


if __name__ == '__main__':

    #adding arguments
    parser = argparse.ArgumentParser(description= 'A class to import, combine, and print data from a folder.',
    prog= 'dataImport')

    parser.add_argument('folder_name', type = str, help = 'Name of the folder')

    parser.add_argument('output_file', type=str, help = 'Name of Output file')

    parser.add_argument('sort_key', type = str, help = 'File to sort on')

    parser.add_argument('--number_of_files', type = int,
    help = "Number of Files", required = False)

    args = parser.parse_args()


    #pull all the folders in the file
    #files_lst = # list the folders


    #import all the files into a list of ImportData objects (in a loop!)
    data_lst = []

    #create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = [] # a list with time rounded to 5min
    data_15 = [] # a list with time rounded to 15min

    #print to a csv file
    printLargeArray(data_5,files_lst,args.output_file+'_5',args.sort_key)
    printLargeArray(data_15, files_lst,args.output_file+'_15',args.sort_key)
