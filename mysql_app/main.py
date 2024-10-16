import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from models import Base, User
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import UserCreate
import schemas

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
        db_user = User(email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id==user_id).first()
    if user is None:
         raise HTTPException(status_code=404, detail="User not found")
    return user

if __name__ == "__main__":
     uvicorn.run(app, host="127.0.0.1", port=8000)





