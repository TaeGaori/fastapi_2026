'''
home_library_v0 / models.py
------------------------------
예광탄 방식을 활용한 아주 얇은 코드
스키마, 테이블 만들기 (ORM)
'''

from datetime import datetime
# sqlalchemy의 String --> 최대 길이를 지정해야 한다. 짧고 정해진 범위의 문자열에 적합하다.
#           DB 쪽에서 길이 초과 시 에러가 나서 실수로 너무 긴 값이 들어가는 것을 막아주는 안전장치 역할
# sqlalchemy의 Text --> 길이 제한이 없다. DB가 허용하는 최대치까지
#           라뷰 본문처럼 얼마나 길어질지 예측하기 어려운 긴 글에 적합하다.
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped,mapped_column, relationship
from database import Base

# ----------------------------------------------
# Book table
# ----------------------------------------------
