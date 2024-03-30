from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import database, orders
from models import OrderCreate, Order

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

# Создание заказа
@router.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    query = orders.insert().values(
        user_id=order.user_id,
        product_id=order.product_id,
        order_date=order.order_date,
        status=order.status
    )
    last_record_id = await db.execute(query)
    return {**order.dict(), "id": last_record_id}

# Получение информации о заказе по его ID
@router.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int, db: Session = Depends(get_db)):
    query = orders.select().where(orders.c.id == order_id)
    order = await db.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Получение списка заказов с пагинацией
@router.get("/orders/", response_model=list[Order])
async def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = orders.select().offset(skip).limit(limit)
    return await db.fetch_all(query)

# Обновление заказа по его ID
@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    query = orders.update().where(orders.c.id == order_id).values(
        user_id=order.user_id,
        product_id=order.product_id,
        order_date=order.order_date,
        status=order.status
    )
    await db.execute(query)
    return {**order.dict(), "id": order_id}

# Удаление заказа по его ID
@router.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    query = orders.delete().where(orders.c.id == order_id)
    await db.execute(query)
    return {"message": "Order deleted successfully"}
