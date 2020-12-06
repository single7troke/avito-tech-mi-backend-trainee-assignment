# avito-tech-mi-backend-trainee-assignment
   Test task for the position of intern-backend


## Описание:
Сервис следит за изменением количества объявлений.<br>
В начале каждого часа сервис добавляет в базу данных количество лотов и топ пять объявлений<br>
по определённому поисковому запросу и региону.

## Ссылка на задание
   [Задание](https://github.com/avito-tech/mi-backend-trainee-assignment)


## Описание методов
   - /add
     - Аргументы<br>
     <b>search_phrase</b> - поисковую фразу<br>
     <b>region</b> - регион (вводится транслитом москва = moskva, россия = rossiya),<br> 
     региструет их в системе, добавляет количество лотов на момент создания.<br>
     Возвращает id этой пары.<br>
          ```
          curl -X POST "http://0.0.0.0:9000/add" \
          -H "accept: application/json" \
          -H  "Content-Type: application/json" \
          -d "{\"search_phrase\":\"Микроволновая печь\",\"region\":\"moskva\"}"
          ```
   - /stat
     - Аргументы<br>
     <b>search_id</b> - id связки поисковая фраза + регион<br>
     Если указан только аргумент <b>search_id</b><br>
     Метод возвращает <b>все</b> счётчики и соответствующие им временные метки (timestamp) по данному id<br><br>
     
     <b>start</b> - время в формате '%Y-%m-%dT%H' (необязательно)<br>
     Если <b>start</b> не указан, метод возвращает все счётчики и соответствующие им временные метки (timestamp),<br> 
     где временные метки <b>меньше или равны stop</b><br><br>
     
     <b>stop</b> - время в формате '%Y-%m-%dT%H' (необязательно)<br>
     Если <b>stop</b> не указан, метод возвращает все счётчики и соответствующие им временные метки (timestamp),<br> 
     где временные метки <b>больше или равны start</b><br><br>
     
     Если указаны все аргументы, метод возвращает все счётчики и соответствующие им временные метки (timestamp),<br>
     где временные метки <b>больше или равны start и меньше или равны stop</b>
     
        ```
         curl -X GET "http://0.0.0.0:9000/stat?search_id=1" -H  "accept: application/json"
        ```
        ```
         curl -X GET "http://0.0.0.0:9000/stat?search_id=1&start=2020-12-4T10&stop=2020-12-4T23" -H  "accept: application/json"
        ```
       <br>
   - /top5
     - Аргументы<br>
     <b>search_id</b> - id связки поисковая фраза + регион<br>
     <b>time</b> - время в формате '%Y-%m-%dT%H'<br> 
     Метод возвращает список с сылками(в формате https://www.avito.ru/id_объявления) на топ пять объявлений<br>
     временная метка списка <b>болеше или равна time</b><br>
          ```
          curl -X GET "http://0.0.0.0:9000/top5?search_id=1&time=2020-12-5T03" -H  "accept: application/json"
          ```
## Запуск приложения (How to run)
   - git clone https://github.com/single7troke/avito-tech-mi-backend-trainee-assignment
   - docker-compose up -d