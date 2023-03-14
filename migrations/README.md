# migration
## Инициализация
- Linux и Mac: `export FLASK_APP=webapp && flask db init`
- CMD Windows: `set FLASK_APP=webapp && flask db init`
- PowerShell: `$env:FLASK_APP="webapp" && flask db init`

## Создние миграции
- Linux и Mac: `export FLASK_APP=webapp && flask db migrate -m "name migration"`
- CMD Windows: `set FLASK_APP=webapp && flask db migrate -m "name migration"`
- PowerShell: `$env:FLASK_APP="webapp" && flask db migrate -m "name migration"`

## Применение миграции
`flask db upgrade`

## Отмена миграции
`flask db downgrade()`

## Чтобы работать с миграциями на существующей базе, нам нужно пометить нашу миграцию как выполненную
`flask db stamp 84cccf62ee91`
