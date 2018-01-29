from tzlocal import get_localzone
import pytz
import hashlib
from datetime import datetime


def _get_unique_hash(self, *args):
	'''
	Use hash of the date str, category, note
	of row to index it rather than where and and and thing
	which would be inefficient
	'''
	m = hashlib.md5()
	for arg in args:
		m.update(arg.encode('utf8'))
	return m.hexdigest()


def str2bool(arg):
    return str(arg).lower() in ["true", 1, "1", "ok"]


def bool2str(arg):
    if arg:
        return "True"
    else:
        return "False"


def get_utc_now():
    return pytz.utc.localize(datetime.utcnow())


def dt2str(dt):
    '''
    Convert a datetime obj to string with format '%Y-%m-%d %H:%M'
    (saves a little typing, given we always use this format)
    '''
    return dt.strftime('%Y-%m-%d %H:%M')


def localstr2utc(localstr, time_zone, date_format='%Y-%m-%d %H:%M'):
    '''
    Take a string in format <date_format> representing a datetime
    in time zone <time_zone>. Parse it to naive datetime obj, then localize
    it using the pytz timezone's localize method creating an aware datetime
    in the given <time_zone>.
    Now convert this to an aware datetime in the UTC timezone

    Note that datetime.now(tz) and datetime.now().replace(tzinfo=tz)
    can be different. The pytz docs notes that the tzinfo arg of standard
    datetime constructors does not work with pytz for many timezones
    (It didnt work in Costa Rica!)
    However it's safe for utc datetimes. DO NOT USE IT OTHERWISE!!
    More generally, the principle to abide by is covert to utc asap, do work,
    and only out local to users.
    Could also consider arrow package to simplify life
    '''
    aware_dt = time_zone.localize(datetime.strptime(localstr, date_format))
    utc_aware_dt = aware_dt.astimezone(pytz.UTC)
    return utc_aware_dt


def utcstr2local(utcstr, time_zone, date_format='%Y-%m-%d %H:%M'):
    '''
    In brief, convert a utc datetime str in format <date_format> to local timezone datetime obj
    '''
    utc_aware_dt = pytz.utc.localize(datetime.strptime(utcstr, date_format))
    local_aware_dt = utc_aware_dt.astimezone(time_zone)
    return local_aware_dt
