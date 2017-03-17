import random
import hashlib
import json
from string import letters
from contextlib import contextmanager
# import sql Alchemy classes and modules
from sqlalchemy import (create_engine,
                        Column,
                        ForeignKey,
                        Integer,
                        String,
                        Boolean,
                        Unicode,
                        Date, DateTime,
                        extract)
from sqlalchemy.types import TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from config import DB_PATH


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(email, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(email + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(email, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(email, password, salt)


class Array(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return Array(self.impl.length)


class Dict(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return Dict(self.impl.length)


class BaseModel():
    """
    Base db Model
    """
    id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    @contextmanager
    def session(self):
        "start database connection session"
        global Base, engine
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def put(self):
        "commit data to data base"
        with self.session() as session:
            session.add(self)
            session.commit()
            session.expunge_all()
            return self


# init database if not exist
Base = declarative_base()
engine = create_engine('sqlite:///{}'.format(DB_PATH))
Base.metadata.create_all(engine)


def init_db():
    global Base, engine
    engine = create_engine('sqlite:///{}'.format(DB_PATH))
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
