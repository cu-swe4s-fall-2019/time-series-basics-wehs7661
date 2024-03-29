#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

# Check PEP8 coding style
run test_pep8_main pycodestyle data_import.py
assert_no_stdout

run test_pep8_unittest pycodestyle test_data_import.py
assert_no_stdout

# Check if the right searching method was used
run test_linear python data_import.py -f smallData -o test -s cgm_small.csv -l
assert_in_stdout "linear"

run test_binary python data_import.py -f smallData -o test -s cgm_small.csv
assert_in_stdout "binary"

# Check if the exception handling works properly
run test_ref python data_import.py -f smallData -o test -s kkk.csv
assert_in_stdout "The reference file is not found in annotation_list!"
assert_exit_code 1

run test_folder python data_import.py -f kkk -o test -s kkk.csv
assert_in_stdout "Folder not found"
assert_exit_code 1

run test_path python data_import.py -f . -o test -s kk.csv
assert_in_stdout "The files in the folder should all be .csv files."
assert_exit_code 1

# Check if the code works properly in general
run test_basics python data_import.py -f smallData -o test -s cgm_small.csv -l
assert_stdout 
assert_exit_code 0
