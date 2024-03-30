from pydantic import BaseModel


# Определение базовой модели данных для пользователя
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


# Определение модели данных для создания нового пользователя
class UserCreate(UserBase):
    pass


# Определение модели данных для пользователя с учетом идентификатора
class User(UserBase):
    id: int

    # Конфигурация модели для возврата данных из ORM
    class Config:
        orm_mode = True


# Определение базовой модели данных для продукта
class ProductBase(BaseModel):
    name: str
    description: str
    price: float


# Определение модели данных для создания нового продукта
class ProductCreate(ProductBase):
    pass


# Определение модели данных для продукта с учетом идентификатора
class Product(ProductBase):
    id: int

    # Конфигурация модели для возврата данных из ORM
    class Config:
        orm_mode = True


# Определение базовой модели данных для заказа
class OrderBase(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    status: str


# Определение модели данных для создания нового заказа
class OrderCreate(OrderBase):
    pass


# Определение модели данных для заказа с учетом идентификатора
class Order(OrderBase):
    id: int

    # Конфигурация модели для возврата данных из ORM
    class Config:
        orm_mode = True
