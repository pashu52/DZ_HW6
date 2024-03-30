from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import database, products
from models import ProductCreate, Product

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

# Создание продукта
@router.post("/products/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    query = products.insert().values(
        name=product.name,
        description=product.description,
        price=product.price
    )
    last_record_id = await db.execute(query)
    return {**product.dict(), "id": last_record_id}

# Получение информации о продукте по его ID
@router.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    query = products.select().where(products.c.id == product_id)
    product = await db.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Получение списка продуктов с пагинацией
@router.get("/products/", response_model=list[Product])
async def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = products.select().offset(skip).limit(limit)
    return await db.fetch_all(query)

# Обновление продукта по его ID
@router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    query = products.update().where(products.c.id == product_id).values(
        name=product.name,
        description=product.description,
        price=product.price
    )
    await db.execute(query)
    return {**product.dict(), "id": product_id}

# Удаление продукта по его ID
@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    query = products.delete().where(products.c.id == product_id)
    await db.execute(query)
    return {"message": "Product deleted successfully"}
