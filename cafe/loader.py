import os
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from database import engine, get_session
from todo.models import Menu, Order

BASE_DIR = os.getcwd()
Menu_PATH = os.path.join(BASE_DIR, 'input', 'menu.csv')
Order_PATH = os.path.join(BASE_DIR, 'input', 'orders.csv')


def load_menu(path: str=Menu_PATH) ->dict:
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


def load_order(path: str=Order_PATH) -> list[dict]:
    df = pd.read_csv(path, encoding='utf-8-sig')
    df['주문일시'] = pd.to_datetime(['주문일시'], errors='coerce')
    df = df.dropna(subset=['주문일시', '테이블번호', '메뉴코드', '수량'])

    records = df.dropna(subset=['주문일시', '테이블번호', '메뉴코드', '수량']).to_dict(orient='records')

    if not records:
        return {'success':0, 'skipped_duplicate':0, 'faild':0}

    try:
        with engine.begin() as conn:
            stmt = pg_insert(Order_PATH).values(records)
            stmt = stmt.on_conflict_do_nothing(constraint='uq_oders_key')
            result = conn.execute(stmt)

        inserted = result.rowcount if result.rowcount is not None else 0

        skipped = len(records) - inserted

        print(f'[loder] orders  적재 완료 - 신규 {inserted}건/ 중복스킵 {skipped}건')
        return {'success' : inserted, 'skipped_duplicate': skipped, 'failed': 0}

    except Exception as e:
        print(f'orders 적재 실패: {e}')
        return{'success':0, 'skipped_duplicate':0, 'failed': len(records)}

if __name__ =='__main__':
    load_menu()
    load_order()