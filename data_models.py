import random, hashlib, logging, datetime
from string import letters
from db.base import *
from assets.validators import valid_name, valid_phone, valid_email
from options import FINE

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(email, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(email + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(email, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(email, password, salt)

class Admin(Base, BaseModel):
	__tablename__ = 'admin'

	id = Column(Integer, primary_key=True)
	username = Column(String(250))
	pw_hash = Column(String(250))
	password = None

	@classmethod
	def add(self, username, pw):
		if not username:
			return 'invalid username'
		if not pw:
			return 'invalid password'
		if self.by_username(username):
			return "User exists"
		pw_hash = make_pw_hash(username, pw)
		self = self(username=username, pw_hash=pw_hash)
		return self.put()

	def update(self):
		if not self.password:
			return 'invalid password'
		self.pw_hash = make_pw_hash(self.username, self.password)
		with self.session() as session:
			entity = session.query(type(self)).filter(type(self).id==self.id)
			entity.update({'pw_hash':self.pw_hash})
			session.commit()
			session.expunge_all()
			return self

	@classmethod
	def delete(self, id):
		try:
			entity = self.by_id(id)
			with self().session() as session:
				session.delete(entity)
				session.commit()
				return True
		except Exception as e:
			logging.error(e)
			return

	@classmethod
	def by_id(self, id):
		with self().session() as session:
			try:
				q = session.query(self).filter(self.id==id).one()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return

	@classmethod
	def by_username(self, username):
		with self().session() as session:
			try:
				q = session.query(self).filter(self.username==username).one()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return

	@classmethod
	def login(self, username, pw):
		u = self.by_username(username)
		if u and valid_pw(username, pw, u.pw_hash):
			return u

	@classmethod
	def get_all(self, count=False, aid=None, username=None):
		filters = []
		if aid: filters.append(self.id==aid)
		if username: filters.append(self.username==username)
		with self().session() as session:
			try:
				admins = session.query(self)
				for f in filters:
					admins = admins.filter(f)
				if count:
					return admins.count()
				admins = admins.order_by(self.id).all()
				session.expunge_all()
				return admins
			except Exception as e:
				logging.error(e)
				return []


class Member(Base ,BaseModel):
	__tablename__ = 'member'

	id = Column(Integer, primary_key=True)
	name = Column(String(250))
	email = Column(String(250))
	mob = Column(String(250))
	fine = Column(String(250), default='0')

	@classmethod
	def add(self, name, email=None, mob=None):
		if not valid_name(name):
			return 'invalid name'
		if email and not valid_email(email):
			return 'invalid email'
		if email and self.by_email(email):
			return "email exists"
		if mob and not valid_phone(mob):
			return 'invalid mob no.'
		if mob and self.by_mob(mob):
			return "mob no. exists"
		self = self(name=name, email=email, mob=mob)
		return self.put()

	def update(self, name=None, email=None, mob=None, fine=None):
		if name and not valid_name(name):
			return 'invalid name'
		if email and self.by_email(email):
			return "email exists"
		if email and not valid_email(email):
			return 'invalid email'
		if mob and self.by_mob(mob):
			return "mob exists"
		if mob and not valid_phone(mob):
			return 'invalid mob no.'
		edits = {}
		edits['name'] = name if name else self.name
		edits['email'] = email if email else self.email
		edits['mob'] = mob if mob else self.mob
		edits['fine'] = fine if fine else self.fine
		with self.session() as session:
			entity = session.query(type(self)).filter(type(self).id==self.id)
			entity.update(edits)
			session.commit()
			session.expunge_all()
			return self

	@classmethod
	def delete(self, id):
		try:
			entity = self.by_id(id)
			with self().session() as session:
				session.delete(entity)
				session.commit()
				return True
		except Exception as e:
			logging.error(e)
			return

	@classmethod
	def by_id(self, id):
		with self().session() as session:
			try:
				q = session.query(self).filter(self.id==id).one()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return

	@classmethod
	def by_email(self, email):
		with self().session() as session:
			try:
				q = session.query(self).filter(self.email==email).one()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return

	@classmethod
	def by_mob(self, mob):
		with self().session() as session:
			try:
				q = session.query(self).filter(self.mob==mob).one()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return

	@classmethod
	def by_name(self, name, n=10, s=0):
		with self().session() as session:
			try:
				q = session.query(self).order_by(self.id).filter(self.name.like(u'%{}%'.format(name))).offset(s).limit(n).all()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return []

	@classmethod
	def get_all(self, count=False, mid=None, name=None, email=None, mob=None):
		filters = []
		if mid: filters.append(self.id==mid)
		if name: filters.append(self.name.like(u'%{}%'.format(name)))
		if email: filters.append(self.email==email)
		if mob: filters.append(self.mob==mob)
		with self().session() as session:
			try:
				members = session.query(self)
				for f in filters:
					members = members.filter(f)
				if count:
					return members.count()
				members = members.order_by(self.id).all()
				session.expunge_all()
				return members
			except Exception as e:
				logging.error(e)
				return []



class Book(Base ,BaseModel):
	__tablename__ = 'book'
	# create primary key column as default
	id = Column(Integer, primary_key=True)
	title = Column(String(250))
	author = Column(String(250))
	publisher = Column(String(250))
	copies = Column(Integer, default=1)
	available = Column(Boolean, default=True)

	def update(self, title=None, author=None, publisher=None, copies=None, available=None):
		if title and not valid_name(title):
			return 'invalid title'
		if author and not valid_name(author):
			return 'invalid author'
		if publisher and not valid_name(publisher):
			return 'invalid publisher'
		if not isinstance(copies, int):
			return 'invalid copies no.'
		edits = {}
		edits['title'] = title if title else self.title
		edits['author'] = author if author else self.author
		edits['publisher'] = publisher if publisher else self.publisher
		edits['copies'] = copies if isinstance(copies, int) else self.copies
		edits['available'] = available if isinstance(available, bool) else self.available
		with self.session() as session:
			entity = session.query(type(self)).filter(type(self).id==self.id)
			entity.update(edits)
			session.commit()
			session.expunge_all()
			return self

	@classmethod
	def delete(self, id):
		try:
			entity = self.by_id(id)
			with self().session() as session:
				session.delete(entity)
				session.commit()
				return True
		except Exception as e:
			logging.error(e)
			return

	@classmethod
	def by_id(self, id):
		with self().session() as session:
			try:
				q = session.query(self).filter(self.id==id).one()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return

	@classmethod
	def by_title(self, title, n=10, s=0):
		with self().session() as session:
			try:
				q = session.query(self).order_by(self.id).filter(self.title.like(u'%{}%'.format(title))).offset(s).limit(n).all()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return []

	@classmethod
	def by_author(self, author, n=10, s=0):
		with self().session() as session:
			try:
				q = session.query(self).order_by(self.id).filter(self.author.like(u'%{}%'.format(author))).offset(s).limit(n).all()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return []

	@classmethod
	def by_publisher(self, publisher, n=10, s=0):
		with self().session() as session:
			try:
				q = session.query(self).order_by(self.id).filter(self.publisher.like(u'%{}%'.format(publisher))).offset(s).limit(n).all()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return []

	@classmethod
	def get_all(self, count=False, bid=None, title=None, author=None, publisher=None, available=None):
		filters = []
		if bid: filters.append(self.id==bid)
		if title: filters.append(self.title.like(u'%{}%'.format(title)))
		if author: filters.append(self.author.like(u'%{}%'.format(author)))
		if publisher: filters.append(self.publisher.like(u'%{}%'.format(publisher)))
		if isinstance(available, bool): filters.append(self.available==available)
		with self().session() as session:
			try:
				books = session.query(self)
				for f in filters:
					books = books.filter(f)
				if count:
					return books.count()
				books = books.order_by(self.id).all()
				session.expunge_all()
				return books
			except Exception as e:
				logging.error(e)
				return []



class Borrow(Base ,BaseModel):
	__tablename__ = 'borrow'
	# create primary key column as default
	id = Column(Integer, primary_key=True)
	book_id = Column(Integer)
	book_title = Column(String)
	member_id = Column(Integer)
	member_name = Column(String)
	start = Column(Date)
	end = Column(Date)
	active = Column(Boolean, default=True)

	@classmethod
	def add(self, book_id, member_id, start, end, active=True):
		book = Book.by_id(book_id)
		if not book:
			return 'invalid book id'
		book_title = book.title
		member = Member.by_id(member_id)
		if not member :
			return 'invalid member id'
		member_name = member.name
		if not isinstance(start, datetime.date):
			return 'invalid start date'
		if not isinstance(end, datetime.date):
			return 'invalid end date'
		if start >= end:
			return 'end must be after start'
		if not isinstance(active, bool):
			return 'invalid active value'
		active_borrows = self.get_all(count=True, book_id=book.id, active=True)
		if active_borrows >= book.copies:
			return 'too many active borrows for this book'
		self = self(book_id=book_id, book_title=book_title, member_id=member_id, member_name=member_name, start=start, end=end, active=active)
		return self.put()


	def update(self, book_id=None, member_id=None, start=None, end=None, active=True):
		book_title = None
		member_name = None
		if book_id:
			book = Book.by_id(book_id)
			if book:
				book_title = book.title
			else:
				return 'invalid book id'
		if member_id:
			member = Member.by_id(member_id)
			if member:
				member_name = member.name
			else:
				return 'invalid member id'
		if start and not isinstance(start, datetime.date):
			return 'invalid start date'
		if end and not isinstance(end, datetime.date):
			return 'invalid end date'
		if not isinstance(active, bool):
			return 'invalid active value'
		edits = {}
		edits['book_id'] = book_id if book_id else self.book_id
		edits['book_title'] = book_title if book_title else self.book_title
		edits['member_id'] = member_id if member_id else self.member_id
		edits['member_name'] = member_name if member_name else self.member_name
		edits['start'] = start if start else self.start
		edits['end'] = end if end else self.end
		if edits['start'] >= edits['end']:
			return 'end must be after start'
		edits['active'] = active if isinstance(active, bool) else self.active
		with self.session() as session:
			entity = session.query(type(self)).filter(type(self).id==self.id)
			entity.update(edits)
			session.commit()
			session.expunge_all()
			return self

	@classmethod
	def delete(self, id):
		try:
			entity = self.by_id(id)
			with self().session() as session:
				session.delete(entity)
				session.commit()
				return True
		except Exception as e:
			logging.error(e)
			return

	@classmethod
	def by_id(self, id):
		with self().session() as session:
			try:
				q = session.query(self).filter(self.id==id).one()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return

	@classmethod
	def by_book_id(self, book_id, n=10, s=0):
		with self().session() as session:
			try:
				q = session.query(self).order_by(self.id).filter(self.book_id==book_id).offset(s).limit(n).all()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return []

	@classmethod
	def by_member_id(self, member_id, n=10, s=0):
		with self().session() as session:
			try:
				q = session.query(self).order_by(self.id).filter(self.member_id==member_id).offset(s).limit(n).all()
				session.expunge_all()
				return q
			except Exception as e:
				logging.error(e)
				return []


	@classmethod
	def get_all(self, count=False, bid=None, book_id=None, book_title=None, member_id=None, member_name=None, start=None, end=None, active=None, from_date=None, to_date=None):
		if book_id and not isinstance(book_id, int):
			return 'invalid book id'
		if member_id and not isinstance(member_id, int):
			return 'invalid member id'
		if start and not isinstance(start, datetime.date):
			return 'invalid start date'
		if end and not isinstance(end, datetime.date):
			return 'invalid end date'
		if active and not isinstance(active, bool):
			return 'invalid active value'
		if from_date and not isinstance(from_date, datetime.date):
			return 'invalid from_date'
		if to_date and not isinstance(to_date, datetime.date):
			return 'invalid to_date'
		filters = []
		if bid: filters.append(self.id==bid)
		if start: filters.append(self.start==start)
		if end: filters.append(self.end==end)
		if book_id: filters.append(self.book_id==book_id)
		if book_title: filters.append(self.book_title.like(u'%{}%'.format(book_title)))
		if member_id: filters.append(self.member_id==member_id)
		if member_name: filters.append(self.member_name.like(u'%{}%'.format(member_name)))
		if isinstance(active, bool): filters.append(self.active==active)
		if from_date: filters.append(self.end >= from_date)
		if to_date: filters.append(self.start <= to_date)
		with self().session() as session:
			try:
				borrows = session.query(self)
				for f in filters:
					borrows = borrows.filter(f)
				if count:
					return borrows.count()
				borrows = borrows.order_by(self.id).all()
				session.expunge_all()
				return borrows
			except Exception as e:
				logging.error(e)
				return []

	@classmethod
	def calc_fines(self):
		logging.info('calclating members fines .....')
		today = datetime.datetime.now().date()
		filters = [self.active==True]
		filters.append(self.end < today)
		borrows = []
		with self().session() as session :
			try:
			 	borrows = session.query(self)
			 	for f in filters:
			 		borrows = borrows.filter(f)
			 	borrows = borrows.all()
			 	session.expunge_all()
			except Exception as e:
			 	logging.error(e)
			 	return
		for b in borrows:
			try:
				fine = today - b.end
				fine = fine.days * FINE
				member = Member.by_id(b.member_id)
				#fine += int(member.fine) if member.fine.isdigit() else 0
				member.update(fine=fine)
			except Exception as e:
				logging.error(e)
		logging.info('members fines calculated')




if __name__ == '__main__':
	pass
	#init_db()
	#b = Admin.by_id(3)
	#print b.username
	#print b.pw_hash
	#a = Control.by_id(Admin, 2)
	#print a.pw_hash
	# test cmds
	#######
	#book= Book(title="frenga2", author="hoda2")
	#book.put()
	#Control.put(Book, title="frenga5", author="hoda5")
	#book= Control.by_id(Book,2)
	#print book.title