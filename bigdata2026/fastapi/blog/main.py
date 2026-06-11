from blog.schema.response import Postresponse
from blog.schema.request import PostCreateRequest, PostUpdateRequest
from fastapi import FastAPI, status, HTTPException

app = FastAPI()

posts = [
    {'id':1, 'title':'파이썬', 'content':'python'},
    {'id':2, 'title':'자바', 'content':'Java'}
]

# 전체 데이터 조회
@app.get(
    '/',
    response_model=list[Postresponse],
    status_code=status.HTTP_200_OK    
)
def get_posts_handler():
    return posts

# 단일 데이터 조회
@app.get(
    '/{post_id}',
    response_model=Postresponse,
    status_code=status.HTTP_200_OK
)
def get_post_handler(post_id: int):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

# 포스트 생성
@app.post(
    '/',
    response_model=Postresponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo_handler(body: PostCreateRequest):
    new_post = {
        'id': len(posts) + 1,
        'title': body.title,
        'content': body.content,
    }
    posts.append(new_post)
    return new_post # 생성된(추가된) 데이터가 응답으로 반환된다.


# 포스트 수정
@app.patch(
    '/{post_id}',
    response_model=Postresponse,
    status_code=status.HTTP_200_OK
)
def update_post_handler(post_id: int, body: PostUpdateRequest):
    for post in posts:
        if post['id'] == post_id:
            if body.title is not None:
                post['title'] = body.title
            if body.content is not None:
                post['content'] = body.content     
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')


# 포스트 삭제
@app.delete(
    '/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post_handler(post_id: int):
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)