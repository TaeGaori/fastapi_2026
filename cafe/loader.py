import os
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from database import engine, get_session
from models import Menu, Order

BASE_DIR = os.getcwd()
Menu_PATH = os.path.join(BASE_DIR, 'input', 'menu.csv')
Order_PATH = os.path.join(BASE_DIR, 'input', 'orders.csv')


def prepare_chunk(path:pd.DataFrame) -> list[dict]:
    db = pd.read_csv(path, encoding='utf-8-sig')
    db = get_session()
    success, failed = 0,0

    for _, row in db.iterrows():
        try:
            m = Menu(
                메뉴코드 = str(row['메뉴코드']),
                메뉴명 = str(row['메뉴명']),
                가격 = int(row['가격'])
            )
            db.merge(m)
            db.commit()
            success += 1

        except Exception as e:
            db.rollback()
            failed += 1
            print(f'적재 실패 - {row.get("정류소명")} / {e}')

    db.close()
    print(f'적재 완료 - 성공: {success:,}건 / 실패: {failed:,}건') 