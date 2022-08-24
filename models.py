import psycopg2
import json
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)

    def __str__(self):
        return f'Publisher {self.id}: {self.name}'

class Book(Base):
    __tablename__ = 'book'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text, nullable=False)
    id_publisher = sa.Column(sa.Integer, sa.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='books')

    def __str__(self):
        return f'Book {self.id}: {self.title}'

class Shop(Base):
    __tablename__ = 'shop'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)

    def __str__(self):
        return f'Shop {self.id}: {self.name}'

class Stock(Base):
    __tablename__ = 'stock'

    id = sa.Column(sa.Integer, primary_key=True)
    id_book = sa.Column(sa.ForeignKey('book.id'))
    id_shop = sa.Column(sa.ForeignKey('shop.id'))
    count = sa.Column(sa.Integer, nullable=False)

    shop = relationship(Shop, backref='stoks')
    book = relationship(Book, backref='stoks')

class Sale(Base):
    __tablename__ = 'sale'

    id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Numeric, nullable=False)
    date_sale = sa.Column(sa.Date)
    id_stock = sa.Column(sa.ForeignKey('stock.id'))
    count = sa.Column(sa.Integer)

    stock = relationship(Stock, backref='sales')

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def push_data(session, file):
    with open(file, 'r') as f:
        data = json.load(f)

    for i in data:
        model = globals()[i.get('model').capitalize()]
        session.add(model(id=i.get('pk'), **i.get('fields')))
    session.commit()
    return


def search_publisher():
    search = input('Введите id или Имя Издателя: ')
    
    if search.isdigit():
        value = int(search)
        column = Publisher.id
    else:
        value = search
        column = Publisher.name
    return {"column": column, "value": value}