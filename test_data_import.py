import unittest
import os
import datetime
import data_import

class TestDataImport(unittest.TestCase):
    def test_init_import(self):
        """
        A testing function for checking the data types and the length of the data
        """
        csv_file = './smallData/meal_small.csv'
        obj = data_import.ImportData(csv_file)
        self.assertEqual(len(obj._time), len(obj._value))
        self.assertEqual("<class 'int'>", str(type(obj._value[0])))
        self.assertEqual("<class 'datetime.datetime'>", str(type(obj._time[0])))

if __name__ == '__main__':
    unittest.main()
