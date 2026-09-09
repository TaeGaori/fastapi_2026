'''
langchain_practice/01_hello.llm.py
--------------------------------------------
가장 단순한 호출 - 프롬프트 템플릿 없이 문자열 하나로 바로 질문

이 파일의 목적
- Langchain을 통해 모델을 직접 부르면 어떤 모습인지 확인
- .invoke() --> 질문을 보내고 응답을 받는다.
'''
import os 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model='gemini-3.6-flash',)

response = llm.invoke('안지랑에서 어디 곱창집이 맛있어?')
print(response.content[0]['text'])