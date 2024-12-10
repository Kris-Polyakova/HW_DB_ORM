import json
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os.path
from dotenv import load_dotenv
from sqlalchemy import CheckConstraint
from sqlalchemy import or_

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), nullable=False)
    
class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="books")
    
class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=30), nullable=False)
    
class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    book = relationship(Book, backref='stocks')
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    shop = relationship(Shop, backref='shops')
    count = sq.Column(sq.Integer)
    
class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime(timezone=True))
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    stock = relationship(Stock, backref='stocks')
    count = sq.Column(sq.Integer, nullable=False)
    __table_args__ = (CheckConstraint('count > 0', name='check_count_positive'),)
    
def create_tables(engine):
    Base.metadata.create_all(engine)
    
def get_dsn():
    dotenv_path = 'config.env'
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    database = os.getenv('database_name')
    user = os.getenv('user')
    password = os.getenv('password')
    DSN = f"postgresql://{user}:{password}@localhost:5432/{database}"
    return DSN

def add_data_from_file(session, filename=str):
    with open (filename, 'r', encoding = 'utf-8') as f:
        data = json.load(f)
        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
   
def get_shops(session, input_data):
    query = ((session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
             ).select_from(Shop).join(Stock, Shop.id == Stock.id_shop)
             .join(Book, Stock.id_book == Book.id)
             .join(Publisher, Book.id_publisher == Publisher.id)
             .join(Sale, Stock.id == Sale.id_stock))
    if input_data.isdigit():
       q = query.filter(Publisher.id == input_data).all()
    else:
       q = query.filter(Publisher.name == input_data).all()
    for title, name, prise, date in q: 
        print(f"{title: <40} | {name: <10} | {prise: <8} | {date.strftime('%d-%m-%Y')}")

   


    
             
             
             
             

