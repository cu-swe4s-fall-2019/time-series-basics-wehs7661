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

    def test_init_replace(self):
        """
        A function to check if the replacement of the strings "low" and "high" are handled properly
        """
        f = open('test.csv', 'w')
        f.write("Id,time,value\n1134,3/19/18 22:18,low")
        f.close()
        obj = data_import.ImportData('test.csv', replace=True)
        self.assertEqual(40, obj._value[0])
        os.remove('test.csv')


if __name__ == '__main__':
    unittest.main()
