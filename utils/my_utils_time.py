# coding: utf-8

import isodate
import datetime

# ----------------------------------------------------------------------------#
def convert_duration_to_work_days(iso_duration):
	"""Convert an ISO 8601 string to number of work days (8H). Return -1 if invalid format"""
	duration = -1
	try:
		duration = float(isodate.parse_duration(iso_duration) / datetime.timedelta(hours=8))
	except:
		duration = -1
	return duration

# ----------------------------------------------------------------------------#
def from_datetime_to_zulu_string(day: datetime) -> str:
    return day.astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z")