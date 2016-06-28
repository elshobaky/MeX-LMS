import os, sys
from contextlib import contextmanager
# import sql Alchemy classes and modules
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Boolean, Unicode, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

# init database if not exist
Base = declarative_base()
engine = create_engine('sqlite:///mexlms.db')
Base.metadata.create_all(engine)

def init_db():
	global Base, engine
	engine = create_engine('sqlite:///mexlms.db')
	Base.metadata.create_all(engine)


class BaseModel():
	"""
	Base db Model
	"""
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


class Control(BaseModel):
	"""
	DB control class
	class methods takes a table class as first argument
	then specific arguments for the method 
	"""
	@classmethod
	def put(self, cls, **kw):
		"commit data to data base"
		with self().session() as session:
			if kw:
				entity = cls(**kw)
			else:
				entity = cls
			session.add(entity)
			session.commit()
			session.expunge_all()
			return entity

	@classmethod
	def by_id(self, cls, id):
		with self().session() as session:
			try:
				q = self().session.query(cls).filter(cls.id==id).one()
				session.expunge_all()
				return q
			except:
				return
if __name__ == '__main__':
	init_db()