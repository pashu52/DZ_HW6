import databases
import sqlalchemy

# URL для подключения к базе данных SQLite
DATABASE_URL = "sqlite:///./database.db"

# Создание объекта базы данных
database = databases.Database(DATABASE_URL)

# Создание объекта метаданных
metadata = sqlalchemy.MetaData()

# Определение таблицы "users"
users = sqlalchemy.Table(
    "users",  # Имя таблицы в базе данных
    metadata,  # Метаданные, которые определяют структуру таблицы
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),  # Первичный ключ
    sqlalchemy.Column("first_name", sqlalchemy.String(50)),  # Имя пользователя
    sqlalchemy.Column("last_name", sqlalchemy.String(50)),  # Фамилия пользователя
    sqlalchemy.Column("email", sqlalchemy.String(50)),  # Электронная почта пользователя
    sqlalchemy.Column("password", sqlalchemy.String(50)),  # Пароль пользователя
)

# Определение таблицы "products"
products = sqlalchemy.Table(
    "products",  # Имя таблицы в базе данных
    metadata,  # Метаданные, которые определяют структуру таблицы
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),  # Первичный ключ
    sqlalchemy.Column("name", sqlalchemy.String(100)),  # Название продукта
    sqlalchemy.Column("description", sqlalchemy.Text),  # Описание продукта
    sqlalchemy.Column("price", sqlalchemy.Float),  # Цена продукта
)

# Определение таблицы "orders"
orders = sqlalchemy.Table(
    "orders",  # Имя таблицы в базе данных
    metadata,  # Метаданные, которые определяют структуру таблицы
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),  # Первичный ключ
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),  # Внешний ключ на таблицу "users"
    sqlalchemy.Column("product_id", sqlalchemy.ForeignKey("products.id")),  # Внешний ключ на таблицу "products"
    sqlalchemy.Column("order_date", sqlalchemy.DateTime),  # Дата заказа
    sqlalchemy.Column("status", sqlalchemy.String(50)),  # Статус заказа
)

# Создание движка для работы с базой данных
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создание таблиц в базе данных на основе определенных метаданных
metadata.create_all(engine)
