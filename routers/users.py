from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db import database, users
from models import UserCreate, User

# Создание экземпляра APIRouter
router = APIRouter()

# Функция для получения объекта базы данных
def get_db():
    db = None
    try:
        db = database
        yield db
    finally:
        if db is not None:
            db.close()

# Создание пользователя
@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    query = users.insert().values(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
    )
    last_record_id = await db.execute(query)
    return {**user.dict(), "id": last_record_id}

# Получение информации о пользователе по его ID
@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    query = users.select().where(users.c.id == user_id)
    user = await db.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Получение списка пользователей
@router.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = users.select().offset(skip).limit(limit)
    return await db.fetch_all(query)

# Обновление информации о пользователе по его ID
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    query = users.update().where(users.c.id == user_id).values(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
    )
    await db.execute(query)
    return {**user.dict(), "id": user_id}

# Удаление пользователя по его ID
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    query = users.delete().where(users.c.id == user_id)
    await db.execute(query)
    return {"message": "User deleted successfully"}
