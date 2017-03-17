import logging
import datetime
from base import (init_db, Base, BaseModel,
                  Column, String, Array, Integer, Boolean, Date,
                  make_pw_hash, valid_pw)
from config import FINE
from assets.validators import (valid_name,
                               valid_email,
                               valid_phone)

# internationalization
from PyQt4 import QtCore
translate = QtCore.QCoreApplication.translate


class Admin(Base, BaseModel):
    __tablename__ = 'admin'

    username = Column(String(250))
    pw_hash = Column(String(250))
    roles = Column(Array)
    password = None

    @classmethod
    def add(self, username, pw, roles=None):
        if not username:
            return translate('dbModels', 'invalid username')
        if not pw:
            return translate('dbModels', 'invalid password')
        if not roles:
            return translate('dbModels', 'invalid permissions list')
        if self.by_username(username):
            return translate("User exists")
        pw_hash = make_pw_hash(username, pw)
        self = self(username=username, pw_hash=pw_hash, roles=roles)
        return self.put()

    def update(self, pw=None, roles=None):
        if pw:
            self.password = pw
        if not self.password:
            return translate('dbModels', 'invalid password')
        self.pw_hash = make_pw_hash(self.username, self.password)
        if roles:
            self.roles = roles
        with self.session() as session:
            entity = session.query(type(self)).filter(type(self).id == self.id)
            entity.update({'pw_hash': self.pw_hash,
                           'roles': self.roles})
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
                q = session.query(self).filter(self.id == id).one()
                session.expunge_all()
                return q
            except Exception as e:
                logging.error(e)
                return

    @classmethod
    def by_username(self, username):
        with self().session() as session:
            try:
                q = session.query(self).filter(self.username == username).one()
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
    def get(self, count=False, id=None, username=None, username_like=None, n=None, s=None):
        filters = []
        if id:
            filters.append(self.id == id)
        if username:
            filters.append(self.username == username)
        if username_like:
            filters.append(self.username.like(u'%{}%'.format(username_like)))
        with self().session() as session:
            try:
                admins = session.query(self)
                for f in filters:
                    admins = admins.filter(f)
                if count:
                    return admins.count()
                admins = admins.order_by(self.id)
                if isinstance(s, int):
                    admins = admins.offset(s)
                if isinstance(n, int):
                    admins = admins.limit(n)
                admins = admins.all()
                session.expunge_all()
                return admins
            except Exception as e:
                logging.error(e)
                return []


class Member(Base, BaseModel):
    __tablename__ = 'member'

    name = Column(String(250))
    email = Column(String(250))
    mob = Column(String(250))
    fine = Column(String(250), default='0')
    note = Column(String)

    @classmethod
    def add(self, name, email=None, mob=None, note=None):
        if not valid_name(name):
            return translate('dbModels', 'invalid name')
        if email and not valid_email(email):
            return translate('dbModels', 'invalid email')
        if email and self.by_email(email):
            return translate('dbModels', "email exists")
        if mob and not valid_phone(mob):
            return translate('dbModels', 'invalid mob no.')
        if mob and self.by_mob(mob):
            return translate('dbModels', "mob no. exists")
        self = self(name=name, email=email, mob=mob, note=note)
        return self.put()

    def update(self, name=None, email=None, mob=None, fine=None, note=None):
        if name and not valid_name(name):
            return translate('dbModels', 'invalid name')
        if email and self.by_email(email):
            return translate('dbModels', "email exists")
        if email and not valid_email(email):
            return translate('dbModels', 'invalid email')
        if mob and self.by_mob(mob):
            return translate('dbModels', "mob exists")
        if mob and not valid_phone(mob):
            return translate('dbModels', 'invalid mob no.')
        edits = {}
        edits['name'] = name if name else self.name
        edits['email'] = email if email else self.email
        edits['mob'] = mob if mob else self.mob
        edits['fine'] = fine if fine else self.fine
        edits['note'] = note if note else self.note
        with self.session() as session:
            entity = session.query(type(self)).filter(type(self).id == self.id)
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
                q = session.query(self).filter(self.id == id).one()
                session.expunge_all()
                return q
            except Exception as e:
                logging.error(e)
                return

    @classmethod
    def by_email(self, email):
        with self().session() as session:
            try:
                q = session.query(self).filter(self.email == email).one()
                session.expunge_all()
                return q
            except Exception as e:
                # logging.error(e)
                return

    @classmethod
    def by_mob(self, mob):
        with self().session() as session:
            try:
                q = session.query(self).filter(self.mob == mob).one()
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
    def get(self, count=False, mid=None, name=None, email=None, mob=None):
        filters = []
        if mid:
            filters.append(self.id == mid)
        if name:
            filters.append(self.name.like(u'%{}%'.format(name)))
        if email:
            filters.append(self.email == email)
        if mob:
            filters.append(self.mob == mob)
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


class Cat(Base, BaseModel):
    __tablename__ = 'bookcat'

    name = Column(String(250))
    custom_id = Column(String)

    @classmethod
    def add(self, name=None, custom_id=None):
        if not name:
            return translate('dbModels', 'invalid name')
        new = self(name=name, custom_id=custom_id)
        return new.put()

    def update(self, name=None, custom_id=None):
        edits = {}
        if not name and name is not None:
            return translate('dbModels', 'invalid name')
        edits['name'] = name if name else self.name
        edits['custom_id'] = custom_id if custom_id else self.custom_id
        # add edits from argumens
        with self.session() as session:
            entity = session.query(type(self)).filter(type(self).id == self.id)
            entity.update(edits)
            session.commit()
            session.expunge_all()
        self.update_books_cats()
        return self

    def update_books_cats(self):
        books = Book.get(cat_id=self.id)
        for book in books:
            b = book.update(cat_id=self.id)
            if type(b) in [str, QtCore.QString]:
                logging.error(b)

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
                q = session.query(self).filter(self.id == id).one()
                session.expunge_all()
                return q
            except Exception as e:
                logging.error(e)
                return

    @classmethod
    def get(self, count=False, id=None,
            name=None, custom_id=None,
            n=None, s=None):
        filters = []
        if id:
            filters.append(self.id == id)
        if name:
            filters.append(self.name.like(u"%{}%".format(name)))
        if custom_id:
            filters.append(self.custom_id == custom_id)
        # add filters from arguments
        with self().session() as session:
            try:
                items = session.query(self)
                for f in filters:
                    items = items.filter(f)
                if count:
                    return items.count()
                items = items.order_by(self.id)
                if isinstance(s, int):
                    items = items.offset(s)
                if isinstance(n, int):
                    items = items.limit(n)
                items = items.all()
                session.expunge_all()
                return items
            except Exception as e:
                logging.error(e)
                return []

    @classmethod
    def get_cats_dict(self):
        cats = self.get()
        return [dict(id=cat.id, name=cat.name, custom_id=cat.custom_id) for cat in cats]


class Book(Base, BaseModel):
    __tablename__ = 'book'

    title = Column(String(250))
    author = Column(String(250))
    cat_id = Column(Integer)
    cat_name = Column(String(250))
    cat_custom_id = Column(String)
    cat_order = Column(Integer)
    state = Column(String)
    copies = Column(Integer, default=1)
    available = Column(Boolean, default=True)

    @classmethod
    def add(self, title=None, author=None,
            cat_id=None, cat_order=None, state=None,
            copies=None, available=None):
        cat_name = None
        cat_custom_id = None
        if not title:  # valid_name(title):
            return translate('dbModels', 'invalid title')
        if author and not valid_name(author):
            return translate('dbModels', 'invalid author')
        if cat_id:
            cat = Cat.by_id(cat_id)
            if not cat:
                return translate('dbModels', 'invalid category')
            cat_name = cat.name
            cat_custom_id = cat.custom_id
        if not isinstance(copies, int):
            return translate('dbModels', 'invalid copies no.')
        if not isinstance(available, bool):
            return translate('dbModels', 'invalid available value')
        # code to validate arguments
        new = self(title=title, author=author,
                   cat_id=cat_id, cat_name=cat_name,
                   cat_custom_id=cat_custom_id, cat_order=cat_order,
                   state=state, copies=copies, available=available)
        return new.put()

    def update(self, title=None, author=None,
               cat_id=None, cat_order=None, state=None,
               copies=None, available=None):
        cat_name = None
        cat_custom_id = None
        if title and not valid_name(title):
            return translate('dbModels', 'invalid title')
        if author and not valid_name(author):
            return translate('dbModels', 'invalid author')
        if cat_id:
            cat = Cat.by_id(cat_id)
            if not cat:
                return translate('dbModels', 'invalid category')
            cat_name = cat.name
            cat_custom_id = cat.custom_id
        if copies is not None and not isinstance(copies, int):
            return translate('dbModels', 'invalid copies no.')
        edits = {}
        edits['title'] = title if title else self.title
        edits['author'] = author if author else self.author
        if cat_id:
            edits['cat_id'] = cat_id
            edits['cat_name'] = cat_name
            edits['cat_custom_id'] = cat_custom_id
        elif cat_id is not None:
            edits['cat_id'] = None
            edits['cat_name'] = None
            edits['cat_custom_id'] = None
        if cat_order:
            edits['cat_order'] = cat_order
        elif cat_order is not None:
            edits['cat_order'] = None
        edits['state'] = state if state else self.state
        edits['copies'] = copies if isinstance(copies, int) else self.copies
        edits['available'] = available if isinstance(available, bool) else self.available
        with self.session() as session:
            entity = session.query(type(self)).filter(type(self).id == self.id)
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
                q = session.query(self).filter(self.id == id).one()
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
    def by_category(self, category, n=10, s=0):
        with self().session() as session:
            try:
                q = session.query(self).order_by(self.id).filter(self.category.like(u'%{}%'.format(category))).offset(s).limit(n).all()
                session.expunge_all()
                return q
            except Exception as e:
                logging.error(e)
                return []

    @classmethod
    def get(self, count=False, bid=None, title=None,
            author=None, cat_id=None, cat_name=None,
            cat_custom_id=None, cat_order=None,
            state=None, available=None):
        filters = []
        if bid:
            filters.append(self.id == bid)
        if title:
            filters.append(self.title.like(u'%{}%'.format(title)))
        if author:
            filters.append(self.author.like(u'%{}%'.format(author)))
        if cat_id:
            filters.append(self.cat_id == cat_id)
        if cat_name:
            filters.append(self.cat_name.like(u'%{}%'.format(cat_name)))
        if cat_custom_id:
            filters.append(self.cat_custom_id == cat_custom_id)
        if cat_order:
            filters.append(self.cat_order == cat_order)
        if state:
            filters.append(self.state.like(u'%{}%'.format(state)))
        if isinstance(available, bool):
            filters.append(self.available == available)
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


class Borrow(Base, BaseModel):
    __tablename__ = 'borrow'

    book_id = Column(Integer)
    book_title = Column(String)
    member_id = Column(Integer)
    member_name = Column(String)
    start = Column(Date)
    end = Column(Date)
    active = Column(Boolean, default=True)
    created_by = Column(String)
    updated_by = Column(String)

    @classmethod
    def add(self, book_id, member_id, start, end, active=True, created_by=None):
        book = Book.by_id(book_id)
        if not book:
            return translate('dbModels', 'invalid book id')
        book_title = book.title
        member = Member.by_id(member_id)
        if not member:
            return translate('dbModels', 'invalid member id')
        if self.get(member_id=member_id, active=True):
            return translate('dbModels', 'this member has an already active borrow')
        member_name = member.name
        if not isinstance(start, datetime.date):
            return translate('dbModels', 'invalid start date')
        if not isinstance(end, datetime.date):
            return translate('dbModels', 'invalid end date')
        if start >= end:
            return translate('dbModels', 'end must be after start')
        if not isinstance(active, bool):
            return translate('dbModels', 'invalid active value')
        active_borrows = self.get(count=True, book_id=book.id, active=True)
        if active_borrows >= book.copies:
            return translate('dbModels', 'not enough copies of this book')
        self = self(book_id=book_id, book_title=book_title,
                    member_id=member_id, member_name=member_name,
                    start=start, end=end, active=active,
                    created_by=created_by)
        return self.put()

    def update(self, book_id=None, member_id=None, start=None, end=None, active=True, updated_by=None):
        book_title = None
        member_name = None
        if book_id:
            book = Book.by_id(book_id)
            if book:
                book_title = book.title
            else:
                return translate('dbModels', 'invalid book id')
        if member_id:
            member = Member.by_id(member_id)
            if member:
                member_name = member.name
            else:
                return translate('dbModels', 'invalid member id')
        if start and not isinstance(start, datetime.date):
            return translate('dbModels', 'invalid start date')
        if end and not isinstance(end, datetime.date):
            return translate('dbModels', 'invalid end date')
        if not isinstance(active, bool):
            return translate('dbModels', 'invalid active value')
        edits = {}
        edits['book_id'] = book_id if book_id else self.book_id
        edits['book_title'] = book_title if book_title else self.book_title
        edits['member_id'] = member_id if member_id else self.member_id
        edits['member_name'] = member_name if member_name else self.member_name
        edits['start'] = start if start else self.start
        edits['end'] = end if end else self.end
        if edits['start'] >= edits['end']:
            return translate('dbModels', 'end must be after start')
        edits['active'] = active if isinstance(active, bool) else self.active
        edits['updated_by'] = updated_by if updated_by else self.updated_by
        with self.session() as session:
            entity = session.query(type(self)).filter(type(self).id == self.id)
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
                q = session.query(self).filter(self.id == id).one()
                session.expunge_all()
                return q
            except Exception as e:
                logging.error(e)
                return

    @classmethod
    def by_book_id(self, book_id, n=10, s=0):
        with self().session() as session:
            try:
                q = session.query(self).order_by(self.id).filter(self.book_id == book_id).offset(s).limit(n).all()
                session.expunge_all()
                return q
            except Exception as e:
                logging.error(e)
                return []

    @classmethod
    def by_member_id(self, member_id, n=10, s=0):
        with self().session() as session:
            try:
                q = session.query(self).order_by(self.id).filter(self.member_id == member_id).offset(s).limit(n).all()
                session.expunge_all()
                return q
            except Exception as e:
                logging.error(e)
                return []

    @classmethod
    def get(self, count=False, bid=None, book_id=None, book_title=None, member_id=None, member_name=None, start=None, end=None, active=None, from_date=None, to_date=None):
        if book_id and not isinstance(book_id, int):
            return translate('dbModels', 'invalid book id')
        if member_id and not isinstance(member_id, int):
            return translate('dbModels', 'invalid member id')
        if start and not isinstance(start, datetime.date):
            return translate('dbModels', 'invalid start date')
        if end and not isinstance(end, datetime.date):
            return translate('dbModels', 'invalid end date')
        if active and not isinstance(active, bool):
            return translate('dbModels', 'invalid active value')
        if from_date and not isinstance(from_date, datetime.date):
            return translate('dbModels', 'invalid from_date')
        if to_date and not isinstance(to_date, datetime.date):
            return translate('dbModels', 'invalid to_date')
        filters = []
        if bid:
            filters.append(self.id == bid)
        if start:
            filters.append(self.start == start)
        if end:
            filters.append(self.end == end)
        if book_id:
            filters.append(self.book_id == book_id)
        if book_title:
            filters.append(self.book_title.like(u'%{}%'.format(book_title)))
        if member_id:
            filters.append(self.member_id == member_id)
        if member_name:
            filters.append(self.member_name.like(u'%{}%'.format(member_name)))
        if isinstance(active, bool):
            filters.append(self.active == active)
        if from_date:
            filters.append(self.end >= from_date)
        if to_date:
            filters.append(self.start <= to_date)
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
        logging.info('calculating members fines .....')
        today = datetime.datetime.now().date()
        filters = [self.active == True]
        filters.append(self.end < today)
        borrows = []
        with self().session() as session:
            try:
                borrows = session.query(self)
                for f in filters:
                    borrows = borrows.filter(f)
                # print borrows.count()
                borrows = borrows.all()
                session.expunge_all()
            except Exception as e:
                logging.error(e)
                return
        for b in borrows:
            try:
                fine = today - b.end
                fine = fine.days * FINE
                # print fine
                member = Member.by_id(b.member_id)
                # fine += int(member.fine) if member.fine.isdigit() else 0
                member.update(fine=fine)
            except Exception as e:
                logging.error(e)
        logging.info('members fines calculated')

if __name__ == '__main__':
    init_db()
