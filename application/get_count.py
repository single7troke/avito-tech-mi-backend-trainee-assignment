from datetime import timedelta
from sqlalchemy import extract
from models import AvitoSearch, Statistics, Location, TopFive


def get_count_statistic(search_id, start, stop, db):
	if start and stop:
		data = db.query(Statistics).filter(Statistics.owner_id == search_id,
		                                   Statistics.timestamp >= start,
		                                   Statistics.timestamp <= stop + timedelta(hours=1))
	elif start and not stop:
		data = db.query(Statistics).filter(Statistics.owner_id == search_id,
		                                   Statistics.timestamp >= start)
	elif not start and stop:
		data = db.query(Statistics).filter(Statistics.owner_id == search_id,
		                                   Statistics.timestamp <= stop + timedelta(hours=1))
	else:
		data = db.query(Statistics).filter_by(owner_id=search_id)
	return data


def get_top_five(search_id, time, db):
	top_urls = []
	try:
		top = db.query(TopFive).filter(TopFive.owner_id == search_id,
		                               extract("year", TopFive.timestamp) == time.year,
		                               extract("month", TopFive.timestamp) == time.month,
		                               extract("day", TopFive.timestamp) == time.day,
		                               extract("hour", TopFive.timestamp) == time.hour).first()
		for id_from_top in top.topfive:
			top_urls.append(f"https://www.avito.ru/{id_from_top}")
		return [str(top.timestamp), top_urls]
	except AttributeError:
		return {"message": f"nothing found for the combination of id = {search_id} and time = {time}"}
