import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import get_dsn, create_tables, add_data_from_file, get_buying_books

engine = sq.create_engine(get_dsn())
Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)
add_data_from_file(session, 'tests_data.json')

session.commit()

get_buying_books(session, None, 'Pearson')
get_buying_books(session, 1)

session.close()


