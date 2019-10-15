import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import math
import copy
import sys
import time


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

        row_num = 1
        with open(data_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_num += 1
                if row['time'] == '' or row['value'] == '':
                    print("Row %s: skipping the rows with imcomplete data..." % str(row_num))
                if replace is True:
                    if row['value'] == 'low':
                        print("Row %s:, replacing the string 'low' with 40 ..." % str(row_num))
                        row['value'] = 40
                    if row['value'] == 'high':
                        print("Row %s: replacing the string 'high' with 300 ..." %str(row_num))
                        row['value'] = 300

                try: 
                    dateutil.parser.parse(row['time'])
                except ValueError:
                    print('Row %s: wrong data type / bad input format of time' %str(row_num))

                try: 
                    if (not math.isnan(float(row['value'])) and not math.isinf(float(row['value'])) and self._err == False):
                        self._time.append(datetime.datetime.strptime(row['time'], '%m/%d/%y %H:%M'))
                        self._value.append(float(row['value']))

                except ValueError:
                    print('Row %s: wrong data type / bad input format of value' %str(row_num))
            f.close()

    def linear_search_value(self, key_time):
        """ 
        This function returns a list of value(s) associated with key_time using a linear approach. If the list is empty, return -1 and error message.

        Parameters
        ----------
        key_time : datetime object
            the time for finding the associated value

        Returns
        -------
        vals : int or list
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

    def binary_search_value(self, key_time):
        """ 
        This function returns a list of value(s) associated with key_time using a linear approach. If the list is empty, return -1 and error message.

        Parameters
        ----------
        key_time : datetime object
            the time for finding the associated value

        Returns
        -------
        vals : int or list
            a list of value(s) associated with given key_time
        """
        vals = []
        self._time.sort()
        low, high = -1, len(self._time)  # indices
        while high > 0:
            mid = (high + low) // 2
            if key_time == self._time[mid] or low == len(self._time) - 1:
                break
            elif key_time < self._time[mid]:
                high = mid
            else:
                low = mid

        # Note that there might be several values associated to the same key_time
        left = mid - 1
        
        # first, find the leftmost value associated to key_time
        while left >= 0:
            if self._time[left] == key_time:
                left -= 1
            else:
                break

        # Then, start appending the values from the leftmost point
        left += 1    # the index of the leftmost point

        while left >= 0:
            if left <= len(self._time) - 1:
                if self._time[left] == key_time:
                    vals.append(self._value[left])
                    left += 1
                else:
                    break
            else:
                break


        if len(vals) == 0:
            print('No value associated with key_time found.')
            return -1
        return vals

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
            if roundtime._time[i] == roundtime._time[i - 1]:
                continue
            else:
                rtime_list.append(roundtime._time[i])
        search_vals = roundtime.binary_search_value(roundtime._time[i])
        if obj._type == 0:
            value_list.append(sum(search_vals))
        elif obj._type == 1:
            value_list.append(sum(search_vals)/len(search_vals))

    return zip(rtime_list, value_list)

def printArray(data_list, annotation_list, base_name, key_file):
    """
    This function creates a csv file which aligns the data in the given list of zip objects based on key_file. 

    Parameters
    ----------
    data_list : list
        a list of zip objects of data (time, value) pairs
    annotation_list : list
        a list of strings with column labels for the data value (file list)
    base_name : str
        the file name of the file to be printed
    key_file : str
        the name from annotation_list which the user wants to align the data on
    
    Returns
    -------
    None (but a .csv file will be produced)
    """
    
    if not (key_file in annotation_list):
        print('The reference file is not found in annotation_list!')
        return -1
    else:
        key_index = annotation_list.index(key_file)
        key_data = data_list[key_index]
        annotation_list.pop(key_index)   # the list of other file
        data_list.pop(key_index)         # the data of other file

    first_row = ['time', key_file] + annotation_list
    with open(base_name + '.csv', mode='w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(first_row)
        for (ref_time, ref_val) in key_data:
            other_vals = []
            for data in data_list:
                len_list = len(other_vals)
                for (time, val) in data:
                    if (ref_time == time):
                        other_vals.append(val)
                if len(other_vals) == len_list:
                    other_vals.append(0)
            writer.writerow([ref_time, ref_val] + other_vals)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description= 'A class to import, combine, and print data from a folder.',
    prog= 'dataImport')

    parser.add_argument('-f', 
                        '--folder_name', 
                        type = str, 
                        help = 'Name of the folder')

    parser.add_argument('-o', 
                        '--output_file', 
                        type=str, 
                        help = 'Name of Output file')

    parser.add_argument('-s',
                        '--sort_key', 
                        type = str, 
                        help = 'File to sort on')

    parser.add_argument('-n',
                        '--number_of_files', 
                        type = int,
                        help = "Number of Files", 
                        required = False)

    args = parser.parse_args()

    try:
        file_list = listdir(args.folder_name)   
    except FileNotFoundError:
        print('Folder not found.')
        sys.exit(1)
    
    data_list = []
    for i in range(len(file_list)):
        data_list.append(ImportData(args.folder_name + '/' + file_list[i]))
    if len(data_list) == 0:
        print('No data imported')
        sys.exit(1)

    start = time.time()
    data_5 = []
    for obj in data_list:
        data_5.append(roundTimeArray(obj, 5))
    result = printArray(data_5, listdir(args.folder_name), args.output_file+'_5', args.sort_key)
    if (result == -1):
        sys.exit(1)
    end = time.time()
    print('Time required to generate data_5.csv: %s seconds' %str(end-start))

    start = time.time()
    data_15 = []
    for obj in data_list:
        data_15.append(roundTimeArray(obj, 15))
    result = printArray(data_15, listdir(args.folder_name), args.output_file+'_15', args.sort_key)
    if (result == -1):
        sys.exit(1)
    end = time.time()
    print('Time required to generate data_15.csv: %s seconds' %str(end-start))