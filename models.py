import hashlib
import pytz
from datetime import datetime
from qtierna_exceptions import DbIntegrityError


class ReminderManager(object):
    '''
    Thanks Django
    https://docs.djangoproject.com/en/2.0/topics/db/managers/
    '''

    def __init__(self, connection):
        self.connection = connection

    def all(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT id, unique_hash, notified, due, category, reminder'
                           ' FROM reminderstable;')
            result_list = []
            for row in cursor.fetchall():
                r = Reminder(due=row[3], category=row[4], reminder=row[5],
                             id=row[0], unique_hash=row[1], notified=row[2])
                result_list.append(r)
            return result_list

    # def get(self, unique_hash):
    #     with self.connection.cursor() as cursor:
    #         cursor.execute('SELECT id, unique_hash, notified, due, category, reminder'
    #                        ' FROM reminderstable where unique_hash=?;' (unique_hash, ))
    #         row = cursor.fetchone()


class Reminder(object):
    '''
    A model representing a reminder
        due - A string representing the due date in UTC timezone
        category - A string for which category the reminder belongs to
        reminder - A string representing the actual reminder note
        notified - A bool representing if we have already notified user
    '''

    objects = ReminderManager()

    def __init__(self, due, category, reminder, id=None, unique_hash=None, notified=False):
        self.id = id
        self.unique_hash = unique_hash
        # UTC
        self.due = due
        self.category = category
        self.reminder = reminder
        self.notified = notified

    def _get_utc_aware_datetime(self, date_format='%Y-%m-%d %H:%M'):
        return pytz.utc.localize(datetime.strptime(self.due, date_format))

    def _get_unique_hash(self):
        '''
        Use hash of the date str, category, note
        of row to index it rather than where and and and thing
        which would be inefficient
        '''
        m = hashlib.md5()
        m.update(self.due.encode('utf8'))
        m.update(self.category.encode('utf8'))
        m.update(self.reminder.encode('utf8'))
        return m.hexdigest()

    def _write_to_db(self, dbCursor, update=False):
        # First check if this instance already stored in db
        unique_hash = self._get_unique_hash()
        dbCursor.execute('SELECT EXISTS(SELECT 1 FROM reminderstable WHERE unique_hash = ?);',
                         (self._get_unique_hash(), ))
        exists = dbCursor.fetchone()
        if exists[0]:
            if not update:
                # Cannot insert already existing
                raise DbIntegrityError('An entry already exists cannot insert row.')
            else:
                # Already exists, update
                parameters = (int(self.notified), self.due, self.category, self.reminder, unique_hash)
                dbCursor.execute('UPDATE reminderstable SET notified=?, due=?, category=?, reminder=?'
                                 ' WHERE unique_hash=?', parameters)
        else:
            # Doesn't exist, insert
            parameters = (None, unique_hash, int(self.notified), self.due,
                          self.category, self.reminder)
            dbCursor.execute('''INSERT INTO reminderstable VALUES (?, ?, ?, ?, ?, ?)''',
                             parameters)
        dbCursor.connection.commit()

    def _delete_from_db(self, dbCursor):
        '''Removes reminder from the db'''
        dbCursor.execute("""DELETE FROM reminderstable WHERE unique_hash=?""",
                         (self._get_unique_hash()))
        dbCursor.connection.commit()
