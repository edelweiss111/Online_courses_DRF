# Online_courses_DRF
Это проект LMS-системы

#### Структура проекта:
config/
1. settings.py - настройки приложений
2. urls.py - файл маршрутизации
3. celery.py - настройки Celery

study/
1. admin.py - настройки админки
2. models.py - модели приложения
3. pagination.py - настройки пагинации
4. permissions.py - настройки прав доступа
5. serializers.py - сериализаторы моделей
6. servises.py - сервисные функции
7. tasks.py - задачи для Celery
8. tests.py - тесты
9. validators.py - настройки валидации
4. urls.py - файл маршрутизации приложения
5. views.py - контроллеры

users/
management/commands
   1. create_user.py - кастомная команда создания пользователя
   2. csu.py - кастомная команда создания суперпользователя

1. admin.py - настройки админки
2. models.py - модели приложения
3. permissions.py - настройки прав доступа
4. serializers.py - сериализаторы моделей
5. tests.py - тесты
6. urls.py - файл маршрутизации приложения
7. views.py - контроллеры


manage.py - точка входа веб-приложения.

pyproject.toml - список зависимостей для проекта.

test_report.txt - результат покрытия тестами.

#### Используется виртуальное окружение poetry

#### Для запуска web-приложения используйте команду "python manage.py runserver" либо через конфигурационные настройки PyCharm.
