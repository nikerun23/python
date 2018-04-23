# -*- coding: utf-8 -*-
import rnd_crawler.utility as util
import re

# body_text = "3. 입찰일정 가. 입찰 제안서 제출마감 일시 및 장소 : 2018.1.23 ~ 2018.4.23(월), 17:00 환경부 운영지원과(6동 604호) 나. 사업자선정 일시 및 장소 : 제안서 제출 마감 후 업체별 유선통보 다. 제안요청서 설명회 : 생략(필요시 업체별 유선통보)    "
# body_text = "3. 입찰일정 가. 입찰 제안서 제출마감 일시 및 장소 : 2018.1.23 ~ 2018.4.23.(월), 17:00 환경부 운영지원과(6동 604호) 나. 사업자선정 일시 및 장소 : 제안서 제출 마감 후 업체별 유선통보 다. 제안요청서 설명회 : 생략(필요시 업체별 유선통보)    "
# body_text = "3. 입찰일정 가. 입찰 제안서 제출마감 일시 및 장소 : 2018.4.23.(월), 17:00 환경부 운영지원과(6동 604호) 나. 사업자선정 일시 및 장소 : 제안서 제출 마감 후 업체별 유선통보 다. 제안요청서 설명회 : 생략(필요시 업체별 유선통보)    "
# body_text = "3. 입찰일정 가. 입찰 제안서 제출마감 일시 및 장소 : 2018.4.2 17:00 환경부 운영지원과(6동 604호) 나. 사업자선정 일시 및 장소 : 제안서 제출 마감 후 업체별 유선통보 다. 제안요청서 설명회 : 생략(필요시 업체별 유선통보)    "
# body_text = "3. 입찰일정 가. 입찰 제안서 제출마감 일시 및 장소 : 2018. 4. 2 17:00 환경부 운영지원과(6동 604호) 나. 사업자선정 일시 및 장소 : 제안서 제출 마감 후 업체별 유선통보 다. 제안요청서 설명회 : 생략(필요시 업체별 유선통보)    "
# body_text = "수요조사 기간 2018. 3. 23.(금) ~ 5. 31.(목)"
# body_text = "접수기간 : 2018. 4. 2(월) ~ 4. 27(금) "
# body_text = "입찰등록 마감일시:  '18. 4. 23.(월), 15시까지"
# body_text = " 제출기한 : 2018년 3월 26일(월) 오후 5시까지 "
# body_text = "접수기간 : 2017. 8. 31(목) - 2017. 9. 11(월), 18:00까지 (12일간)"
# body_text = "공고 및 신청기간 : 2018. 3. 30(금) ~ 2018. 4. 13(금) 18:00까지"
# body_text = "입찰등록 마감일시와 장소 (우편ㆍ택배접수 불가)   - 2018. 04. 06(금요일) 14:00시 까지 도착분에 한함(산업연구원 1119호 예산실)"
# body_text = "가. 마감일시: 2018년 4월 16일(월) 15:00시까지 우편 또는 이메일 접수"
# body_text = "입찰참가 기한 및 장소 ○ 2018. 4. 26.(목) 16:00, 고용노동부 청년고용기획과(일괄 접수함) "
# body_text = "공모기간 : 2018. 1. 22(월) ~ 1.29(월)"
# body_text = "가. 입찰 제안서 제출마감 일시 및 장소 : 2018.4.26.(목) 17:00 환경부 운영지원과(6동 604호)"
# body_text = "- 제출마감일: '18.4.27(금), 18:00"
body_text = "제출기한 : 2018. 04. 28. (토) 14:00까지"


# """" 공고 시작일, 마감일을 정제하여 반환합니다 """
def valid_start_end_date(date_type, date_str, content_DateFormat):
    # date_str = date_str.replace('\n','')
    if re.match('(.*)[0-9]+', date_str, re.DOTALL) is None:  # 숫자가 없으면 return ''
        print('########## 숫자가 없습니다 :',date_str)
        return ''
    date_str = date_str.strip().replace('.','-').replace('/','-')
    date_str = re.sub('[^0-9~/시:\s-]', '', date_str)  # 2017-12-29~2018-01-03
    if 'YYYY-MM-DD~YYYY-MM-DD' == content_DateFormat:
        if 2 == date_type:  # content_StartDate : 2
            date_str = date_str[:date_str.find('~')]
        elif 3 == date_type:  # content_EndDate : 3
            year_str = date_str[:date_str.find('-')].strip()
            date_str = date_str[date_str.find('~')+1:]
            if year_str not in date_str:  # 마감일에 연도 없을 경우 시작일의 연도를 붙여준다
                date_str = year_str + '-' + date_str.strip()
    print('date_str :',date_str, '시작일' if date_type == 2 else '마감일')
    print('result :', util.valid_date(date_str, None).strftime('%Y-%m-%d'))
    return util.valid_date(date_str, None).strftime('%Y-%m-%d')

# valid_start_end_date()

end_date_index = body_text.find('마감')
print('end_date_index :',end_date_index)

end_str = body_text[end_date_index:end_date_index+50]
print(end_str)

end_str = re.sub('[^0-9~.-:/\s]','',end_str).strip()
print('re.sub :',end_str)

# result = util.valid_start_end_date(3,end_str,'YYYY-MM-DD~YYYY-MM-DD')
# print(result)


test = '2018. 3. 2 09시'
# test = '2018 - 3 - 2 09시'
# test = '2018-3-2 09시'

print(test.rfind(' '))
print(test[:test.rfind(' ')])
