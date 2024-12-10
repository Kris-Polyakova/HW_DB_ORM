import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import get_dsn, create_tables, add_data_from_file, get_shops

engine = sq.create_engine(get_dsn())
Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)
add_data_from_file(session, 'tests_data.json')

session.commit()

if __name__ == '__main__':
    input_data = input('Введите имя или айди пyблииста')
    get_shops(session, input_data)

session.close()


