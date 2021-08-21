![example workflow](https://github.com/InaraShalfei/foodgram-project-react/actions/workflows/main.yml/badge.svg)

**Проект foodram-project-react** 


Cайт Foodgram, «Продуктовый помощник». 
На этом сервисе пользователи могут публиковать рецепты,
подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», 
а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.


## Локальный запуск проекта:
Чтобы запустить проект локально необходимо выполнить следующие команды:
- cd infra/
- docker-compose up
Для заполнения проекта начальными данными выполнить следующую команду:
- docker-compose exec web bash python manage.py loaddata <file.name>


## IP проекта:
foodgram-project-react: http://193.32.218.214/


## Логин и пароль для входа от имени администратора:
login:inara@example.com
password:123456
