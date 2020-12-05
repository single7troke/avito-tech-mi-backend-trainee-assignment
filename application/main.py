import parser
import requests

from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import AvitoSearch, Statistics, Location, TopFive


app = FastAPI()
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Add(BaseModel):
    search_phrase: str = Field(..., example="Микроволновая печь")
    region: str = Field(..., example="moskva")


class Stat(BaseModel):
    search_id: int = Field(..., example=1)
    start: str = Field(None, example="2020-12-12T00")
    stop: str = Field(None, example="2020-12-12T23")


class Top5(BaseModel):
    search_id: int = Field(..., example=1)
    time: str = Field(None, example="2020-12-12T03")


@app.post("/add")
def add(input_data: Add, db: Session = Depends(get_db)):
    region = input_data.region.lower()
    if requests.get(f"https://www.avito.ru/{region}").status_code == 404:
        raise HTTPException(status_code=404, detail="Invalid region")

    locationId = parser.Parser().get_locationId(region)
    count = parser.Parser().take_count(locationId, input_data.search_phrase)
    locationId_already_in_db = db.query(Location.locationId).filter_by(locationId=locationId).scalar()

    if not locationId_already_in_db:
        new_location = Location(locationId=locationId, region_name=region)
        db.add(new_location)
        db.commit()
        db.refresh(new_location)

    location = db.query(Location).filter(Location.locationId == locationId).first()
    new_search = AvitoSearch(search_phrase=input_data.search_phrase, region=region, location_id=location.locationId)
    db.add(new_search)
    db.commit()
    db.refresh(new_search)

    first_search_count = Statistics(count=count, owner_id=new_search.id)
    db.add(first_search_count)
    db.commit()

    return {"id": new_search.id}


@app.post("/stat")
def stat(input_data: Stat, db: Session = Depends(get_db)):
    result: dict = {}
    search_id_in_db = db.query(AvitoSearch).filter_by(id=input_data.search_id).scalar()
    if not search_id_in_db:
        raise HTTPException(status_code=404, detail="Invalid id")

    if input_data.start and input_data.stop:
        try:
            start_time = datetime.strptime(input_data.start, "%Y-%m-%dT%H")
            stop_time = datetime.strptime(input_data.stop, "%Y-%m-%dT%H") + timedelta(hours=1)
        except ValueError:
            return {"error": "time data does not match format '%Y-%m-%dT%H'"}

        searches = db.query(Statistics).filter(Statistics.owner_id == input_data.search_id,
                                               Statistics.timestamp >= start_time,
                                               Statistics.timestamp <= stop_time)

    elif input_data.start and not input_data.stop:
        try:
            start_time = datetime.strptime(input_data.start, "%Y-%m-%dT%H")
        except ValueError:
            return {"error": "time data does not match format '%Y-%m-%dT%H'"}
        searches = db.query(Statistics).filter(Statistics.owner_id == input_data.search_id,
                                               Statistics.timestamp >= start_time)

    elif not input_data.start and input_data.stop:
        try:
            stop_time = datetime.strptime(input_data.stop, "%Y-%m-%dT%H") + timedelta(hours=1)
        except ValueError:
            return {"error": "time data does not match format '%Y-%m-%dT%H'"}
        searches = db.query(Statistics).filter(Statistics.owner_id == input_data.search_id,
                                               Statistics.timestamp <= stop_time)
    else:
        searches = db.query(Statistics).filter_by(owner_id=input_data.search_id)

    for i in searches:
        result.update({i.timestamp: i.count})

    return result


@app.post("/top5")
def get_top_five(input_data: Top5, db: Session = Depends(get_db)):
    top_urls = []
    search_id_in_db = db.query(AvitoSearch).filter_by(id=input_data.search_id).scalar()

    if not search_id_in_db:
        raise HTTPException(status_code=404, detail="Invalid id")

    try:
        search_time = datetime.strptime(input_data.time, "%Y-%m-%dT%H")
        top = db.query(TopFive).filter(TopFive.owner_id == input_data.search_id, TopFive.timestamp >= search_time).first()
        for id_from_top in top.topfive:
            top_urls.append(f"https://www.avito.ru/{id_from_top}")
        return {"top five": top_urls}
    except AttributeError:
        return {}
    except ValueError:
        return {"error": "time data does not match format '%Y-%m-%dT%H'"}
