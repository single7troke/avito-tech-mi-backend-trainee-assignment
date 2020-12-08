import datetime
import requests

from models import AvitoSearch, Location


def locationId_already_in_db(locationId, region, db):
	in_db = db.query(Location.locationId).filter_by(locationId=locationId).scalar()
	if not in_db:
		new_location = Location(locationId=locationId, region_name=region)
		db.add(new_location)
		db.commit()


def already_in_db(search_phrase, region, db):
	in_db = db.query(AvitoSearch).filter(AvitoSearch.search_phrase == search_phrase, AvitoSearch.region == region).scalar()
	if in_db:
		return True
	return False


def search_id_not_in_db(search_id, db):
	in_db = db.query(AvitoSearch).filter_by(id=search_id).scalar()
	if not in_db:
		return True
	return False


def region_validation(region):
	region = region.lower()
	if requests.get(f"https://www.avito.ru/{region}").status_code == 404:
		return 404
	return region


def time_validation(time):
	if time:
		try:
			valid_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H")
			return valid_time
		except ValueError:
			return "error"
	return time
