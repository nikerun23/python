import unittest
import datetime
from ..utility import valid_date
from ..utility import modify_date


class UtillityTestCase(unittest.TestCase):

    def test_data(self):
        self.assertIsNone(valid_date(''))
        self.assertIsNone(valid_date(None))
        dateTemp = [
            '2017-01-01',
            '2017/01/01',
            '2017-01-01',
            '2017,01,01',
            '2017.01.01',
            '2017.01.01.',
            '2017. 01. 01.',
            '2017. 01.01',
            '2017. 1.01.',
            '2017.1.1',
            '2017-1-1 ~ 2017-2-2',
            '2018.02.20~2018.03.19',
            '''2018-02-20 ~ 2018-02-27

                        / 오늘 마감''',
            '''2017-12-07
               ~
               2018-12-31'''
        ]
        for dt in dateTemp:
            self.assertEqual(datetime.date, valid_date(dt).__class__)

    def test_modify_date(self):
        date_fm = 'DD/nYY.MM'
        date_str = '''작성일 : 
        26
        18.02
        '''
        self.assertEqual('2018-02-26',modify_date(date_fm, date_str))


