import datetime


def structure_date(date):
	str_day = None
	if(is_today(date)):
		str_day = 'Today'
	elif is_tomorrow(date):
		str_day = 'Tomorrow'
	elif is_yesterday(date):
		str_day = 'Yesterday'
	else:
		str_day = date.strftime('%A')

	d = str_day + ' ' + date.strftime('%d') + ' ' + date.strftime('%b') + ' ' + date.strftime('%Y') + ' '
	t = date.strftime('%I') + ':' + date.strftime('%H') + ' PM'
	return  d + t


def is_today(date):
	return date.date() == datetime.datetime.today().date()


def is_tomorrow(date):
	return (date.date() - datetime.timedelta(days=1)) == datetime.datetime.today().date()


def is_yesterday(date):
	return (date.date() + datetime.timedelta(days=1)) == datetime.datetime.today().date()


def enumerate_month(str_month):
	months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
		'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
	return months[str_month]