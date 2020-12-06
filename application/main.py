from parser import get_locationId, take_count
from get_count import get_count_statistic, get_top_five
from validation import time_validation, region_validation, already_in_db, locationId_already_in_db, search_id_not_in_db

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
    region: str = Field(..., example="moskva")


@app.post("/add")
def add(input_data: Add, background: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Метод добавляет в базу данных связку search_phrase + region\n

    :param input_data:
    - search_phrase: (str) = поисковая фраза
    - region: (str) =  регион поиска (регион вводится транслитом москва = moskva, россия = rossiya)\n
    :param background: запускает функцию first_count_update\n
    :return: (dict) =  {"id": id созданной связки}\n
    """
    region = region_validation(input_data.region)
    if region == 404:
        raise HTTPException(status_code=404, detail="Invalid region")

    if already_in_db(input_data.search_phrase, region, db):
        return {"message": f"combination of '{input_data.search_phrase} + {region}' already in db"}

    locationId = get_locationId(region)
    locationId_already_in_db(locationId, region, db)

    location = db.query(Location).filter(Location.locationId == locationId).first()
    new_search = AvitoSearch(search_phrase=input_data.search_phrase, region=region, location_id=location.locationId)
    db.add(new_search)
    db.commit()
    db.refresh(new_search)

    background.add_task(first_count_update, locationId, input_data.search_phrase, new_search.id, db)

    return {"id": new_search.id}


@app.get("/stat")
def stat(search_id: int = Query(..., example=1),
         start: str = Query(None, example="2020-12-12T00"),
         stop: str = Query(None, example="2020-12-12T23"),
         db: Session = Depends(get_db)):
    """
    Метод возвращает счётчики и соответствующие им временные метки (timestamp) в определенном промежутке времени,\n
    в зависимости от аргументов start и stop\n

    :param search_id: (int) = id связки search_phrase + region\n
    :param start: (str) = время в формате '%Y-%m-%dT%H' (необязательный)\n
    :param stop: (str) = время в формате '%Y-%m-%dT%H' (необязательный)\n
    :return: (dict) = {"timestamp": count}
    """

    if search_id_not_in_db(search_id, db):
        raise HTTPException(status_code=404, detail="Invalid id")

    try:
        start, stop = time_validation(start, stop)
    except ValueError:
        return {"error": "time data does not match format '%Y-%m-%dT%H'"}

    statistic_data = get_count_statistic(search_id, start, stop, db)

    result: dict = {}
    for item in statistic_data:
        result.update({item.timestamp: item.count})
    return result


@app.get("/top5")
def top_five(search_id: int = Query(..., example=1),
             time: str = Query(None, example="2020-12-12T03"),
             db: Session = Depends(get_db)):
    """
    Метод возвращает список с сылками(в формате https://www.avito.ru/id_объявления) на топ пять объявлений\n
    временная метка списка болеше или равна значению аргумента time\n

    :param search_id: (int) = id связки search_phrase + region\n
    :param time: (str) = время в формате '%Y-%m-%dT%H'\n
    :return: (list) = [https://www.avito.ru/id_объявления]
    """

    if search_id_not_in_db(search_id, db):
        raise HTTPException(status_code=404, detail="Invalid id")

    response = get_top_five(search_id, time, db)
    return response
