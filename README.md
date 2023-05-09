# ToDo-tracker
Web-сервис и телеграм бот для контроля и напоминаний о регулярных задачах

----
## Настройка виртуального окружения

Перед запуском переименовать/скопировать `.env.example` в `.env`

```
cp .env.example .env
```

и исправить значения на необходимые

----

## Создание базы
`flask db upgrade`

----
## Запуск web-сервера

### Командная строка Windows
`run.bat`
### PowerShell
`.\run.ps1`
### linux
Выполните в консоли команду `chmod +x run.sh` - это сделает файл исполняемым.
Теперь для запуска проекта нужно писать `./run.sh`

----

## Запуск бота
`python bot_app`

----

## Запуск Celery
### Windows
`set FORKED_BY_MULTIPROCESSING=1 && celery -A celery_tasks worker --loglevel=info`

### linux
`celery -A celery_tasks worker --loglevel=info`

Чтобы запуск задач по расписанию работал, необходимо запустить celery-beat. Он следит за расписанием и отправлять задачи worker-ам. Beat нужно запускать отдельно, поэтому понадобится еще одно окно терминала

`celery -A celery_tasks beat`

Есть и более простой вариант, который можно использовать на очень маленьких проектах

`celery -A celery_tasks worker -B --loglevel=INFO`
