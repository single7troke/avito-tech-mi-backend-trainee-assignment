import time
import requests

import models
from database import db


session = requests.Session()
session.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/87.0.4280.67 Safari/537.36",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7"
        }


def take_count(locationId: int, search_phrase: str, countonly: int = 1) -> int:
    url = f"https://avito.ru/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&limit=5&locationId={locationId}&countOnly={countonly}&query={search_phrase}"

    response = session.get(url)
    count = response.json()["result"]["count"]
    return int(count)


def take_top_five(locationId: int, search_phrase: str) -> list:
    top_five: list = []
    url = f"https://www.avito.ru/api/9/items?&key=ZaeC8aidairahqu2Eeb1quee9einaeFieboocohX&limit=5&locationId={locationId}&query={search_phrase}"
    response = session.get(url)
    lots = response.json()
    for lot in lots["result"]["items"]:
        lot_id = lot["value"]["id"]
        top_five.append(int(lot_id))
    return top_five


def update():
    searches = db.query(models.AvitoSearch).all()
    try:
        for search in searches:
            count = take_count(locationId=search.location_id, search_phrase=search.search_phrase)
            count_update = models.Statistics(count=count, owner_id=search.id)
            db.add(count_update)
            db.commit()
    except:
        db.close()
        return "count update Error"
    db.close()


def top_five_update():
    searches = db.query(models.AvitoSearch).all()
    try:
        for search in searches:
            topfive = take_top_five(locationId=search.location_id, search_phrase=search.search_phrase)
            top_update = models.TopFive(topfive=topfive, owner_id=search.id)
            db.add(top_update)
            db.commit()
    except:
        db.close()
        return "count update Error"
    db.close()


def loop(loop_time: int):
    while True:
        remain = int(loop_time - time.time() % 3600)
        if remain > 0:
            time.sleep(remain)
        update()
        top_five_update()


if __name__ == "__main__":
    loop(3610)
