import psycopg2
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from models import *

# Переменные подключения
bd = 'postgresql'
bd_adress = 'localhost'
bd_port = 5432
bd_name = 'books_db'
bd_user = 'postgres'
bd_password = 'postgres'

file_data = 'data.json'

if __name__ == "__main__":

    DSN = f'{bd}://{bd_user}:{bd_password}@{bd_adress}:{bd_port}/{bd_name}'
    engine = sa.create_engine(DSN)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Создание и наполнение таблиц БД данными из файла
    create_tables(engine)
    push_data(session, file_data)

    # Выполнение запроса
    search = search_publisher()
    subq = session.query(Book).join(Publisher.books).filter(search.get('column') == search.get('value')).subquery()

    for c in session.query(Shop).join(Stock.shop).join(subq, Stock.id_book == subq.c.id).all():
        print(c)

    session.close()