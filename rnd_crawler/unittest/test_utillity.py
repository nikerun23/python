import unittest
import datetime
import rnd_crawler.utility as util


class UtillityTestCase(unittest.TestCase):

    # 날짜 정제 테스트
    def test_data(self):
        self.assertIsNone(util.valid_date('', None))
        self.assertIsNone(util.valid_date(None, None))
        date_temp = [
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
        for dt in date_temp:
            self.assertEqual(datetime.date, util.valid_date(dt, None).__class__)

    # 날짜 수정 테스트
    def test_modify_date(self):
        date_fm = 'DD/nYY.MM'
        date_str = '''작성일 : 
                26
                18.02
                '''
        self.assertEqual('2018-02-26', util.modify_date(date_str, date_fm))
        date_str = '''작성일 : 
                        26
                        18.02'''
        self.assertEqual('2018-02-26', util.modify_date(date_str, date_fm))
        date_str = '''26
                        18.02'''
        self.assertEqual('2018-02-26', util.modify_date(date_str, date_fm))

        date_fm = '|YYYY-MM-DD'
        date_str = '''							경영관리팀 
							
								| 
							
							2018-02-26'''
        self.assertEqual('2018-02-26', util.modify_date(date_str, date_fm))

    # 시작일~마감일 데이터 정제 테스트
    def test_start_end_date(self):
        date_list = {' 접수기간  2018-04-25 09시 ~ 2018-05-08 17시  ',
                     ' 접수 2018.04.25 ~ 2018.05.08 ',
                     '2018-04-25~2018-05-08'
                     }

        for dt in date_list:
            self.assertEqual('2018-04-25', util.valid_start_end_date(2, dt,'YYYY-MM-DD~YYYY-MM-DD'))
            self.assertEqual('2018-05-08', util.valid_start_end_date(3, dt, 'YYYY-MM-DD~YYYY-MM-DD'))

