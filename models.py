import pytz
from datetime import datetime
from utils import smart_truncate
# SQLALCHEMY
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.ext.hybrid import hybrid_property
Base = declarative_base()

# Notes:
# Make the actual tables
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# session.add(...)
# session.addall(...)
# (view session.new and session.dirty to see things waiting for commit)
# session.commit()

# All reminders in a given category, e.g. 'Work'
# session.query(Reminder).filter(Reminder.categories.any(Category.category_name=='Work')).all()
# No categories
# session.query(Reminder).filter(~Reminder.categories.any()).all()
# All reminders
# reminders = session.query(Reminder).all()
# All categories
# categories = session.query(Category).all()
# Many-to-many relationship between reminders and categories
# (one reminder may be in many categories, and one category may have many
# reminders


association_table = Table('association', Base.metadata,
                          Column('category_id', Integer, ForeignKey('categories.category_id')),
                          Column('reminder_id', Integer, ForeignKey('reminders.reminder_id'))
                          )


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False, unique=True)
    reminders = relationship('Reminder', secondary=association_table,
                             back_populates='categories')

    def __repr__(self):
        return '<Category %s>' % self.category_name


class Reminder(Base):
    __tablename__ = 'reminders'
    __table_args__ = (UniqueConstraint('due', 'note', name='_due_note_uc'),)

    reminder_id = Column(Integer, primary_key=True)
    due = Column(String, nullable=False)
    note = Column(String, nullable=False)
    complete = Column(Boolean, nullable=False, default=False)
    categories = relationship('Category', secondary=association_table, back_populates='reminders')

    def _get_utc_aware_datetime(self, date_format='%Y-%m-%d %H:%M'):
        return pytz.utc.localize(datetime.strptime(self.due, date_format))

    # @hybrid_property
    # def unique_hash(self):
    #     '''
    #     Use hash of the due date and note
    #     of row to index it rather than where and and and thing
    #     which would be inefficient
    #     '''
    #     m = hashlib.md5()
    #     m.update(self.due.encode('utf8'))
    #     m.update(self.note.encode('utf8'))
    #     return m.hexdigest()

    def __repr__(self):
        return '<Reminder due %s note %s>' % (self.due, smart_truncate(self.note, 100))
