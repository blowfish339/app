import aioredis
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
import uvicorn
from schemas import User

# @asynccontextmanager
# async def get_redis():
#     try:
#         db = await aioredis.from_url(url='redis://127.0.0.1', encoding='utf-8', decode_responses=True)
#         yield db
#     finally:
#         await db.close()

db = aioredis.from_url(url='redis://127.0.0.1', encoding='utf-8', decode_responses=True)
app = FastAPI()

@app.get('/users/{user_email}', response_model=User)
async def get_users(user_email: str):
    user_password = await db.get(user_email)
    if not user_password:
        raise HTTPException(status_code=404, detail='User not found')
    user = User(email=user_email, password=user_password)
    return user

@app.post('/users/')
async def create_user(user: User):
    await db.set(user.email, user.password)
    return {'message': 'User created successfully'}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)