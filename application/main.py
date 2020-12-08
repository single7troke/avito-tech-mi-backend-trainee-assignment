from parser import get_locationId, take_count
from get_count import get_count_statistic, get_top_five
from validation import time_validation, region_validation, already_in_db, locationId_already_in_db, search_id_not_in_db
from response_models import AddResponse, StatResponse, Top5Response

from pydantic import BaseModel, Field
from fastapi import Depends, FastAPI, HTTPException, Query, BackgroundTasks
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


def first_count_update(locationId, search_phrase, owner_id, db):
    count = take_count(locationId, search_phrase)
    first_search_count = Statistics(count=count, owner_id=owner_id)
    db.add(first_search_count)
    db.commit()


class Add(BaseModel):
    search_phrase: str = Field(..., example="Микроволновая печь")
    region: str = Field(...,  example="moskva")


@app.post("/add", response_model=AddResponse, tags=["add"])
def add(input_data: Add, background: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Сохраняет количество объявлений по поисковой фразе.
    """
    region = region_validation(input_data.region)
    if region == 404:
        raise HTTPException(status_code=404, detail="Invalid region")

    if already_in_db(input_data.search_phrase, region, db):
        raise HTTPException(status_code=422, detail="combination of '{input_data.search_phrase} + {region}' already in db")

    locationId = get_locationId(region)
    if type(locationId) != int:
        raise HTTPException(status_code=404, detail=f"avito.ru unavailable, error code = {locationId.status_code}")
    locationId_already_in_db(locationId, region, db)

    location = db.query(Location).filter(Location.locationId == locationId).first()
    new_search = AvitoSearch(search_phrase=input_data.search_phrase, region=region, location_id=location.locationId)
    db.add(new_search)
    db.commit()
    db.refresh(new_search)

    background.add_task(first_count_update, locationId, input_data.search_phrase, new_search.id, db)

    return {"id": new_search.id}


@app.get("/stat", response_model=StatResponse, tags=["statistic"])
def stat(search_id: int = Query(..., example="id связки search_phrase + region"),
         start: str = Query(None, example="время в формате '%Y-%m-%dT%H'", max_length=13),
         stop: str = Query(None, example="время в формате '%Y-%m-%dT%H'", max_length=13),
         db: Session = Depends(get_db)):
    """
    Возвращает счетчики и соответствующие им временные метки (timestamp) в заданном промежутке времени.
    """

    if search_id_not_in_db(search_id, db):
        raise HTTPException(status_code=404, detail="id not found")
    valid_start = time_validation(start)
    valid_stop = time_validation(stop)
    if valid_start == "error" or valid_stop == "error":
        raise HTTPException(status_code=422, detail="time does not match format '%Y-%m-%dT%H'")
    statistic_data = get_count_statistic(search_id, valid_start, valid_stop, db)

    result: dict = {}
    for item in statistic_data:
        result.update({str(item.timestamp): item.count})
    return {"statistic": result}


@app.get("/top5", response_model=Top5Response, tags=["statistic"])
def top_five(search_id: int = Query(..., example="id связки search_phrase + region"),
             time: str = Query(..., example="время в формате '%Y-%m-%dT%H'", max_length=13),
             db: Session = Depends(get_db)):
    """
    Возвращает список со ссылками на первые пять объявлений по данному запросу.
    """

    if search_id_not_in_db(search_id, db):
        raise HTTPException(status_code=404, detail="id not found")
    valid_time = time_validation(time)
    if valid_time == "error":
        raise HTTPException(status_code=422, detail="time does not match format '%Y-%m-%dT%H'")

    data = get_top_five(search_id, valid_time, db)
    if len(data) == 2:
        timestamp, urls = data
        return {"timestamp": timestamp, "urls": urls}
    else:
        raise HTTPException(status_code=404, detail=data["message"])
