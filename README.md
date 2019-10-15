[![Build Status](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-wehs7661.svg?branch=master)](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-wehs7661)

# Time-Series Basics
Time Series basics - importing, cleaning, printing to csv

## Description
This is a repository for Assignment 5 of course Software Engineering for Scientist (CSCI7000) at CU Boulder, which includes the following files:
- `data_import.py`: a Python code to import, combine and print data from a folder. The data will be printed to two files with suffices of `_5` and `_15` as a result of different parameters.
- `test_data_import.py`: a Python script of unit tests for `data_import.py`
- `func_test_data_import.sh`: a shell script of functional tests for `data_import.py`
- `smallData`: a folder which contains `.csv` file

## Installation
All the Python scripts are written in Python 3 and the packages required to run the codes include: `csv`, `dateutil.parser`, `os`, `argparse`, `datetime`, `math`, `copy`, `sys` and `time`.

## Usage
To run `data_import.py` using linear searching method, align the data on `ref.csv` in the folder `data_folder` and output `result_5.csv` and `result_15.csv`, run:
```
python data_import.py -f [data_folder] -o [result] -s [ref.csv] -l
```
To run `data_import.py` using binary searching method, align the data on `ref.csv` in the folder `data_folder` and output `result_5.csv` and `result_15.csv`, run:
```
python data_import.py -f [data_folder] -o [result] -s [ref.csv]
```
To run function tests for `data_import.py`, run:
```
bash func_test_data_import.sh
```
To run unit tests for `data_import.py`, run:
```
python test_data_import.py
```
### `ImportData` Class
* Parameters: the filename of a `.csv file` which contains columns of data named `time` and `value`
* Attributes:
  * `_time`: a list containing datetimes
  * `_value`: a list containing values associated with datetimes in `_time`
  * `_type`: the type of method to hand the data, as explained in the section of `roundTimeArray`
* Action: The initialization function import time and value entries from the `.csv` file.
* Returns: None (but could be instantiate as an object)
* Methods:
  * `linear_search_value`:
    * Returns a list of value(s) associated with key_time using a linear approach. If the list is empty, return -1 and error
  * `binary_search_value`:
    * Returns a list of value(s) associated with key_time using a binary approach.

### `roundTimeArray(obj, res)`
* Parameterss: `obj` (`ImportData` Object) and `res` (rounding resoultion of time)
* Action:
  * Creates a list of datetime entries and associated values with the times rounded to the nearest rounding resolution (res).
  * Ensures no duplicated times
  * Handles duplicated values for a single timestamp in the following manner:
    * Activity - sum the values
    * Bolus - sum the values
    * Meal - sum the values
    * Smbg - average the values
    * Hr - average the values
    * Cgm - average the values
    * Basal - average the values
* Returns: iterable zip object of the two lists

### `printArray(data_list, annotation_list, base_name, key_file)`
* Parameterss​: 
  * `​data_list` ​a list of zip objects of data (time, value) pairs.
  * `annotation_list` ​a list of strings with column labels for the data value
  * `base_name` ​the file name you want to print as
  * `key_file` ​the name from annotation_list you want to align the data on
* Action​: Creates a `csv` which aligns the data in the given list of zip objects based on key_file. The first column is time, and the second column is the data from `key_file`, the remaining headings is the same as the one created by `os.listdir`.
* Returns: None, but two `.csv` files will be produced

## Changes made upon the starter code of Assignment 5
- Developed data processing methods in `data_import.py`, including `__init__`, `linear_search_value`, `binary_search_value`, `roundTimeArray`, and `printArray`.
- Developed unit tests for all the methods in `data_import.py`, including `test_init_import`, `test_init_replace`, `test_linear_search`, `test_binary_search`, `test_roundtime`, `test_printarray`.
- Developed functional tests for `data_import.py`, including tests to:
  - Check if the right searching method was used
  - Check if the exception handling works properly
  - Check if the code works properly in general

## Extra credit: benchmarking of the generation of `result_5.csv` and `result_15.csv`
In the method `roundTimeArray`, two different searching methods are available, including `linear_search_value` and `binary_search_value`. The result of benchmarking is shown below:
- Linear searching method - `linear_search_value`:
  - `result_5.csv`: 4.4560558795928955 seconds
  - `result_15.csv`: 1.6259894371032715 seconds
- Binary searching method - `binary_search_value`:
  - `result_5.csv`: 0.9054098129272461 seconds
  - `result_15.csv`: 0.48976874351501465 seconds
