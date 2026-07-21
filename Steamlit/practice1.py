import streamlit as st
import pandas as pd

# 1. 나만의 자기소개 카드
name = st.text_input(
    '이름을 입력하세요',
    placeholder='예)김코딩',
    max_chars=32
)

years = st.slider('경력 연차를 입력하세요',0, 100, 0)

skills = st.multiselect(
    '관심 있는 기술을 모두 선택하세요',
    ['Python', 'SQL', 'Streamlit', 'FastAPI', '머신러닝']
)


st.divider()

# st.markdown(f'**이름** : {name}')
# st.markdown(f'**경력** : {years}')
# st.markdown(f'**관심 기술** : {",".join(skills)}')


if name:
    # 세로를 1:3 비율로 나눈다 (columns 위젯)
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown(f'''
        <div style="width:60px;height60px;border-radius:50%;
                    background-color:#e6f1fb;
                    display:flex;
                    justify-content:center;
                    font-weight:bold;">{name[0]}</div>
                    ''',
                    unsafe_allow_html=True)


    with col2:
        st.markdown(f'**이름** : {name}')
        st.markdown(f'**경력** : {years}')
        st.markdown(f'**관심 기술** : {",".join(skills)}')
        

else:
    st.info('이름을 입력하면 카드가 생성됩니다.')