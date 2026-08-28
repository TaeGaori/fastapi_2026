from fastapi import FastAPI, status, HTTPException
from train import train
import pickle
import joblib
from pydantic import BaseModel

class Featureinput(BaseModel)

app = FastAPI(
    title='펭귄 예측'
)


# 모델링으로 만든 pkl파일 불러오기
MODEL_PATH = 'penguin_model.pkl'
try:
    model = joblib.load(MODEL_PATH)
    print('로드 성공')
except Exception as e:
    print('로드 실패 ')
    model = None

@app.get("/")
def root():
    return{'message': '서버 실행'}   


@app.get('/model-info/')
def input_model(
    
)
