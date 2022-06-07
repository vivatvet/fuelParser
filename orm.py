from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session
import env

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)


class Orm:

    def __init__(self):
        self.engine = create_engine(f"sqlite:///{env.database}")
        Base.metadata.create_all(self.engine)

    def add_user(self, user_id: int):
        ed_user = User(user_id=user_id)
        session = Session(bind=self.engine)
        session.add(ed_user)
        session.commit()
        session.close()

    def find_user(self, user_id: int):
        session = Session(bind=self.engine)
        find_user = session.query(User.user_id).filter(User.user_id == user_id).first()
        session.close()
        return find_user

    def get_users(self):
        session = Session(bind=self.engine)
        users = session.query(User.user_id).order_by(User.id).all()
        session.close()
        return users
