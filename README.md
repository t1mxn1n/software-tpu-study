# О проекте #

Проект по дисциплине "Технологии по разработке ПО". **Цель разработки** - 
создать веб-платформу по размещению обучающих курсов и обеспечить возможность 
записи на предложенные курсы.


# Запуск приложения

### Требования к запуску
> Python 3.11

Склонируйте репозиторий: `git clone https://github.com/t1mxn1n/software-tpu-study.git`

Перейдите в каталог проекта: `cd software-tpu-study`

Создайте переменную окружения: `python -m venv venv`

Активируйте переменную окружения: `.\venv\Scripts\activate`

Установите необходимые зависимости: `pip install -r requirements.txt`

Выполните миграции базы данных: `python .\study\manage.py migrate`

Запустите веб-приложение: `python .\study\manage.py runserver`

Для доступа к админ-панели создайте супер пользователя: `python .\study\manage.py createsuperuser`