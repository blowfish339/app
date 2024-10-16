import aioredis
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
import uvicorn
from schemas import User
from aioredis import ConnectionPool

@asynccontextmanager
async def get_redis(app: FastAPI):
    try:
        app.state.redis = await aioredis.from_url(url='redis://127.0.0.1', encoding='utf-8', decode_responses=True)
        yield
    finally:
        await app.state.redis.close()

app = FastAPI(lifespan=get_redis)

@app.get('/users/{user_email}', response_model=User)
async def get_users(user_email: str):
    user_password = await app.state.redis.get(user_email)
    if not user_password:
        raise HTTPException(status_code=404, detail='User not found')
    user = User(email=user_email, password=user_password)
    return user

@app.post('/users/')
async def create_user(user: User):
    await app.state.redis.set(user.email, user.password)
    return {'message': 'User created successfully'}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)