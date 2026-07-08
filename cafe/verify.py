from sqlalchemy import text
from database import engine

def verify():
    with engine.connect() as conn:
        # 전체 건수
        total = conn.execute(text("SELECT COUNT(*) FROM menu")).scalar()

        # 가격 0 이하인 행

        # 메뉴명 NULL 여부
        null_check = conn.execte(text(
            "SELECT COUNT(*) FILTER (WHERE 메뉴명 IS NULL) AS null_cafe_name,FROM menu")).fetchone()    

