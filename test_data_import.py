import unittest
import os
import datetime
import data_import

class TestDataImport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.csv_file = './smallData/meal_small.csv'
        cls.obj = data_import.ImportData(cls.csv_file)

    def test_init_import(self):
        """
        A testing function for checking the data types and the length of the data
        """
        self.assertEqual(len(self.obj._time), len(self.obj._value))
        self.assertEqual("<class 'float'>", str(type(self.obj._value[0])))
        self.assertEqual("<class 'datetime.datetime'>", str(type(self.obj._time[0])))

    def test_init_replace(self):
        """
        A function to check if the replacement of the strings "low" and "high" are handled properly
        """
        f = open('test.csv', 'w')
        f.write("Id,time,value\n1134,3/19/18 22:18,low")
        f.close()
        obj_init = data_import.ImportData('test.csv', replace=True)
        self.assertEqual(40, obj_init._value[0])
        os.remove('test.csv')

    def test_linear_search(self):
        """
        A testing function for linear_search_value
        """
        time1 = datetime.datetime(2018, 3, 16, 8, 42)
        time2 = datetime.datetime(2020, 3, 12, 0, 0)
        val1 = self.obj.linear_search_value(time1)
        val2 = self.obj.linear_search_value(time2)
        self.assertEqual(val1, [60])
        self.assertEqual(val2, -1)

    def test_binary_search(self):
        """
        A testing function for binary_search_value.
        """
        time1 = datetime.datetime(2018, 3, 16, 8, 42)
        time2 = datetime.datetime(2020, 3, 12, 0, 0)
        val1 = self.obj.binary_search_value(time1)
        val2 = self.obj.binary_search_value(time2)
        self.assertEqual(val1, [60])
        self.assertEqual(val2, -1)

    def test_roundtime(self):
        """
        A testing function for rounTimeArray
        """
        obj_test1 = data_import.ImportData('./smallData/cgm_small.csv')
        output = data_import.roundTimeArray(obj_test1, 30)
        for (time, val) in output:
            self.assertEqual(time.minute, 0)
            self.assertEqual(val, (131 + 138 + 144)/3)
            break

        obj_test2 = data_import.ImportData('./smallData/activity_small.csv')
        output = data_import.roundTimeArray(obj_test2, 40)
        for (time, val) in output:
            self.assertEqual(time.minute, 0)
            self.assertEqual(val, (3 + 7 + 76 + 6 + 7))
            break

    def test_printarray(self):
        """
        A testing function for printArray
        """
        file_list = os.listdir('./smallData')
        data_list = []
        for i in range(len(file_list)):
            obj = data_import.ImportData('./smallData/' + file_list[i])
            data_list.append(data_import.roundTimeArray(obj, 5))

        result = data_import.printArray(data_list, file_list, 'test_printarray', 'meal_small.csv')
        self.assertNotEqual(result, -1)
        self.assertTrue(os.path.exists('test_printarray.csv'))
        os.remove('test_printarray.csv')


if __name__ == '__main__':
    unittest.main()