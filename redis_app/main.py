import aioredis
from fastapi import FastAPI, Request, Depends
from contextlib import asynccontextmanager
import uvicorn

@asynccontextmanager
async def get_redis(app: FastAPI):
    try:
        db = await aioredis.from_url(url='redis://127.0.0.1', encoding='utf-8', decode_responses=True)
        yield 
    finally:
        await db.close()

db = aioredis.from_url(url='redis://127.0.0.1', encoding='utf-8', decode_responses=True)
app = FastAPI()

@app.get('/users/{user_email}')
async def get_users(user_email: str):
    user_password = await db.get(user_email)
    return user_password

@app.post('/users/')
async def create_user(user_email: str, user_password: str):
    await db.set(user_email, user_password)
    pwd = await db.get(user_email)
    return pwd
    # return {'message': 'User created successfully'}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)