# ================================
# storage_subway_busapi/02_bus/verify.py
# 
# 보스노선 적재 검증
#       - 필수 컬럼 NULL 여부
#       - 대구 좌표 범위
#       - 위치구분 값 분포 점검
# 
# 커넥션(connection) ??
# - 파이썬 프로그램과 PostgreSQL 서버 사이에 맞어지는 연결 통로
# - 계속 SQL을 주고 받으려면 이 연결부터 먼저 맺는다.
#   - 연결 생성 -> 쿼리 실행 -> 연결 종료 -> 낭비
# 
# DB 커넥션 풀(Cnnection Pool)??
# -  프로그램이 시작될 때(create_engine(...) 호출 시점) 연결 여러개를 미리 만들어서 "풀(pool, 저장소)"에 담아둔다
# - engine.connect()를 호출하면, 새로 연결을 만드는 게 아니라 풀에서 이미 만들어진 연결을 잠깐 빌려온다.
# - 다 쓰고 나면 (with 블록이 끝나면) 연결을 끊는게 아니라 풀에 다시 반납해서, 다음 번 요청이 그 연결을 재사용할 수 있게 한다.
# ================================
from sqlalchemy import text
from database import engine

# 대구 구,군 + '기타'(경계 밖 지역) 허용값 목록
GU_LIST = {'북구', '중구', '동구', '서구', '남구', '수성구', '달성군', '달서구', '기타'}

def verify():
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM bus_stop")).scalar()

        # 위도 / 경도 NULL 개수를 한 번의 쿼리로 동시에 집계
        null_check = conn.execute(text("""
            SELECT  COUNT(*) FILTER (WHERE 위도 IS NULL) AS null_lat,
                    COUNT(*) FILTER (WHERE 경도 IS NULL) AS null_lon
            FROM bus_stop
        """)).fetchone() # 딱 한 행만

        # 대구 대략적인 경계값을 벗어나는 좌표 건수 확인
        #   (위도, 경도 중 하나라도 범위를 벗어나면 or 조건으로 카운트)
        out_of_range = conn.execute(text("""
            SELECT COUNT(*) FROM bus_stop
            WHERE 위도 NOT BETWEEN 35.7 AND 36.0
                OR 경도 NOT BETWEEN 128.4 AND 128.8
     """)).scalar() # 결과가 값 1개 일 때
        
    # 위치구분 컬럼에 들어있는 고유값들을 모두 가져와서 GU_LIST에 없는 값들만 걸러낸다
    gu_values = conn.execute(text(
        "SELECT DISTINCT 위치구분 FROM bus_stop"
    )).fetchall() # 결과가 값 1개 일 때
    invalid_gu = []
    for g in gu_values:
        if g[0] not in GU_LIST:
            invalid_gu.append(g[0])

    print('=== 적재 검증 결과 ===')
    print(f'전체 건수 : {total:,}')
    print(f'위도 NULL 건수 : {null_check[0]}')
    print(f'경도 NULL 건수 : {null_check[1]}')
    print(f'좌표 범위 이탈 건수 : {out_of_range}')
    print(f'위치구분 이상값 : {invalid_gu if invalid_gu else "없음"}')

    ok = (null_check[0] == 0 and null_check[1] == 0 and out_of_range == 0 and not invalid_gu)
    print(f'검증 결과 : PASS {ok}')
    return ok

if __name__ =='__main__':
    verify()