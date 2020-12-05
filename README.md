# avito-tech-mi-backend-trainee-assignment
   Test task for the position of intern-backend


## Описание:
Сервис следит за изменением количества объявлений.<br>
В начале каждого часа сервис добавляет в базу данных<br>
колличество лотов по определённому поисковому запросу и региону,<br>
а также топ пять объявлений.


## Ссылка на задание
   [Задание](https://github.com/avito-tech/mi-backend-trainee-assignment)


## Опиание методов
   - /add
     - принимает на вход<br>
     <b>search_phrase</b> - поисковую фразу<br>
     <b>region</b> - регион,<br> 
     региструет их в системе.<br>Возвращает id этой пары.<br>
          ```
          curl -X POST "http://0.0.0.0:9000/add" \
          -H "accept: application/json" \
          -H  "Content-Type: application/json" \
          -d "{\"search_phrase\":\"Микроволновая\",\"region\":\"moskva\"}"
          ```
   - /stat
     - Принимает на вход<br>
     <b>search_id</b> - id связки поисковая фраза + регион<br>
     <b>start</b> - время в формате '%Y-%m-%dT%H' (необязательно)<br>
     <b>stop</b> - время в формате '%Y-%m-%dT%H' (необязательно)
     
     - Если подать на вход только <b>search_id</b><br>
     Метод возвращает <b>все</b> счётчики и соответствующие им временные метки (timestamp)<br>
     по данному id<br>
         ```
         curl -X POST "http://0.0.0.0:9000/stat" \
         -H  "accept: application/json" \
         -H  "Content-Type: application/json" \
         -d "{\"search_id\":1,\"start\":\"\",\"stop\":\"\"}"
       
         ```
     - Если подать на вход только <b>search_id</b> и <b>start</b><br>
     Метод возвращает все счётчики и соответствующие им временные метки (timestamp),<br> 
     где временные метки <b>больше или равны start</b><br>
        ```
         curl -X POST "http://0.0.0.0:9000/stat" \
         -H  "accept: application/json" \
         -H  "Content-Type: application/json" \
         -d "{\"search_id\":1,\"start\":\"2020-12-04T07\",\"stop\":\"\"}"
       
         ```
     - Если подать на вход только <b>search_id</b> и <b>stop</b><br>
     Метод возвращает все счётчики и соответствующие им временные метки (timestamp),<br> 
     где временные метки <b>меньше или равны stop</b><br>
        ```
         curl -X POST "http://0.0.0.0:9000/stat" \
         -H  "accept: application/json" \
         -H  "Content-Type: application/json" \
         -d "{\"search_id\":1,\"start\":\"\",\"stop\":\"2020-12-05T22\"}"
       
         ```
     - Если подать на вход только <b>search_id</b>, <b>start</b> и <b>stop</b><br>
     Метод возвращает все счётчики и соответствующие им временные метки (timestamp),<br> 
     где временные метки <b>больше или равны start</b><br> и <b>меньше или равны stop</b><br>
        ```
         curl -X POST "http://0.0.0.0:9000/stat" \
         -H  "accept: application/json" \
         -H  "Content-Type: application/json" \
         -d "{\"search_id\":1,\"start\":\"2020-12-04T07\",\"stop\":\"2020-12-05T22\"}"
       
         ```
   - /top5
     - принимает на вход<br>
     <b>search_id</b> - id связки поисковая фраза + регион<br>
     <b>time</b> - время в формате '%Y-%m-%dT%H'<br> 
     Метод возвращает список с сылками(в формате https://www.avito.ru/id_объявления) на топ пять объявлений<br>
     временная метка списка болеше или равна <b>time</b><br>
          ```
          curl -X POST "http://0.0.0.0:9000/top5" \
          -H "accept: application/json" \
          -H  "Content-Type: application/json" \
          -d "{\"search_id\":\"1\",\"time\":\"2020-12-05T03\"}"
          ```
## Запуск приложения (How to run)
   - git clone https://github.com/single7troke/avito-tech-mi-backend-trainee-assignment
   - docker-compose up -d