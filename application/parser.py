import bs4 as bs
import requests


session = requests.Session()
session.headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.67 Safari/537.36",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7"
    }


def get_locationId(region: str):
    locationId = ""
    url = f"https://avito.ru/{region}"
    response = session.get(url)
    if response.status_code != 200:
        return response
    soup = bs.BeautifulSoup(response.text, "lxml")
    string = soup.find(rel="alternate").get("href")
    for i in string[::-1]:
        if i.isdigit():
            locationId += i
        elif i == "=":
            return int(locationId[::-1])


def take_count(locationId: int, search_phrase: str):
    url = f"https://avito.ru/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&limit=5&locationId={locationId}&countOnly=1&query={search_phrase}"
    response = session.get(url)
    count = response.json()["result"]["count"]
    return int(count)
