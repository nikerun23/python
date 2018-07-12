import unittest
import datetime
import rnd_crawler.utility_v2 as util


class UtillityTestCase(unittest.TestCase):

    # 제목 정제 테스트
    def test_title(self):
        src_title = '2018년도「부천시 중소ㆍ중견기업 지원사업」 모집공고조회128'
        result_title = '2018년도「부천시 중소ㆍ중견기업 지원사업」 모집공고'

        self.assertEqual(result_title, util.valid_title(src_title))
        self.assertEqual(result_title, util.valid_title(result_title))



    # 날짜 정제 테스트
    def test_valid_date(self):

        date_temp = [
            '2017-01-01',
            '2017/01/01',
            ' 2017/01/01/ ',
            '  2017-01-01   ',
            '2017,01,01',
            '2017.01.01',
            '2017.01.01.',
            '2017. 01. 01.',
            '2017. 01.01',
            '2017. 1.01.',
            '2017.1.1',
            '2017. 1. 1',
            '2017-1-1 ~ 2017-2-2',
            '2018.01.01~2018.03.19',
            '''2018-01-01 ~ 2018-02-27

                        / 오늘 마감''',
            '''2017-1-01
               ~
               2018-12-31''',
            '2017.01.01 12:00',
            '2017.1.1 12:00',
            '2017.1.1 2:00',
            '2017.1.1 2시',
            ' 2017-01-01 12시 ',
            '2017-01-01 12시마감 ',
            '2017-01-01 12시 마감',
            '2017-1-1 마감'
        ]
        for dt in date_temp:
            self.assertEqual(datetime.date, util.valid_date(dt, None).__class__)
            print(util.valid_date(dt, None))
        self.assertIsNone(util.valid_date('마감일', None))
        self.assertIsNone(util.valid_date('    ', None))
        self.assertIsNone(util.valid_date('''  
            
                   ''', None))
        self.assertIsNone(util.valid_date('', None))
        self.assertIsNone(util.valid_date(None, None))
        self.assertEqual(datetime.date, util.valid_date('''작성일 : 
09
18.04''', 'DD/nYY.MM').__class__)

    # 날짜 수정 테스트
    def test_modify_date(self):
        date_fm = 'DD/nYY.MM'
        date_str = '''작성일 : 
                26
                18.02
                '''
        self.assertEqual('2018-02-26', util.modify_date(date_str, date_fm))
        date_str = ''' 작성일 : 
                        26
                        18.02 '''
        self.assertEqual('2018-02-26', util.modify_date(date_str, date_fm))
        date_str = ''' 26
                        18.02 '''
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
                     '2018-04-25~2018-05-08 진행중',
                     '''2018-04-25~2018-05-08 
                        진행중 ''',
                     '2018-04-25 ~ 2018-05-08 / 접수마감까지 7일 남음',
                     '2018-4-25~2018-5-8',
                     '2018.4.25~2018.5.8',
                     '2018-04-25~2018-05-08',
                     '2018-04-25 12:00 ~ 2018-05-08 24:00',
                     '2018-04-25 ~ 2018-05-08 24:00',
                     '2018.4.25 ~ 2018.5.8 24:00',
                     '2018.4.25 ~ 5.8',
                     '2018.4.25 ~ 5.8 12시까지 마감',
                     '2018/04/25 ~ 2018/05/08',
                     '2018-04-25 ~ 2018-05-08',
                     '''  
                         2018/04/25 ~ 2018/05/08
                        접수중
                        '''
                     }

        for dt in date_list:
            self.assertEqual('2018-04-25', util.valid_start_end_date(2, dt, 'YYYY-MM-DD~YYYY-MM-DD'))
            self.assertEqual('2018-05-08', util.valid_start_end_date(3, dt, 'YYYY-MM-DD~YYYY-MM-DD'))

        self.assertEqual('', util.valid_start_end_date(3, '  ', 'YYYY-MM-DD~YYYY-MM-DD'))
        self.assertEqual('2018-04-25', util.valid_start_end_date(3, ''' 
			    2018-04-25
			    ''', 'YYYY-MM-DD~YYYY-MM-DD'))
        self.assertEqual('2017-11-15', util.valid_start_end_date(2, '2017-11-15 ~ 2018-01-31', 'YYYY-MM-DD~YYYY-MM-DD'))

