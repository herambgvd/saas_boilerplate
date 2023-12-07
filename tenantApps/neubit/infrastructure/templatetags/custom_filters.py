import datetime

from django import template

register = template.Library()


@register.filter
def timestamp_to_date(timestamp):
	try:
		return datetime.datetime.fromtimestamp(timestamp / 1000)  # Dividing by 1000 to convert milliseconds to seconds
	except ValueError:
		return None


@register.filter
def format_duration(duration):
	seconds = duration / 1000  # Convert to seconds if it's in milliseconds
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
