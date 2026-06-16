from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel, field_validator
import random
from enum import Enum # 허용할 값을 미리 정해놓는 것

app = FastAPI(
    title='점심 메뉴 추천 API',
    description='오늘 뭐 먹을지 고민될 때 사용하는 메뉴 추천 API입니다!.',
    version='1.1.0',
)

# Enum: 카테고리 허용값 제한
#   str을 상속하면 응답에서 "한식" 이라는 문자열로 출력된다. 보기가 좋다!
class CategoryEnum(str,Enum):
    한식 = "한식",
    일식 = "일식",
    중식 = "중식",
    양식 = "양식"

# Pydantic 모델: 저장소(DB 역할)에 사용할 메뉴 스키마
#   요청과 응답 모두 동일한 구조로 일관성 유지
class Menu(BaseModel):
    id:int
    name:str
    category:CategoryEnum   # Enum으로 허용값 제한
    price: int
    like: int = 0 # 기본값 0

# 요청 바디(Body) 메뉴 생성 스키마 정의 - pydantic 모델
class MenuCreateRequest(BaseModel):
    name:str 
    category: CategoryEnum 
    price: int

# field_validator: 추가 유효성 검사 -> price가 0이하면 의미없는 데이터이므로 차단
@field_validator('price')
@classmethod
def price_must_be_positive(cls,v):
    if v <= 0:
        raise ValueError('가격은 0보다 커야 합니다!')
    return v

# 요청 바디(Body) 메뉴 수정 스키마 정의 -Pydantic 모델
class MenuUpdateRequest(BaseModel):
    name: str | None=None
    category:CategoryEnum | None=None
    price: int | None=None

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('가격은 0보다 커야합니다!')
        return v