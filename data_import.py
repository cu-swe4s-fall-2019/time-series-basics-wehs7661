import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import math


class ImportData:
    def __init__(self, data_csv, replace=False):
        """
        The initialization function import time and value entries from the .csv file.

        Parameters
        ----------
        
        data_csv : str
            the filename of the .csv file
        replace : bool
            whether to trigger the loop for examining if there are strings like 'high' or 'low' in the value column

        Returns
        -------
        None 
        """
        self._time = []
        self._value = []

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
                        print("Replacing the string 'high' with 300...")
                        row['value'] = 300
                try: 
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError:
                    print('Bad input format for time')

                if (not math.isnan(float(row['value'])) and not math.isinf(float(row['value']))):
                    self._value.append(int(row['value']))
            f.close()

    def linear_search_value(self, key_time):
        """ This function returns a list of value(s) associated with key_time. If the list is empty, return -1 and error message.

        Parameters
        ----------
        key_time : datetime
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
    pass
    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned


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
