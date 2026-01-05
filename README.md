# Образовательная Платформа

Полнофункциональная образовательная платформа на Django с REST API, GraphQL, WebSocket и микросервисной архитектурой.

## Основные возможности

- **Пользователи и роли**: Регистрация, аутентификация JWT, роли (Admin, Instructor, Student)
- **Курсы**: CRUD операции, категории, теги, версии
- **Уроки**: Видео, текст, тесты с порядком прохождения
- **Тесты**: Вопросы с вариантами, подсчет баллов
- **Прогресс**: Отслеживание обучения, сертификаты PDF
- **Платежи**: Интеграция Stripe для реальных платежей
- **Отзывы**: Рейтинги и комментарии
- **Уведомления**: WebSocket для реального времени
- **Поиск**: Elasticsearch для мощного поиска
- **Рекомендации**: Система рекомендаций курсов
- **Email**: Асинхронная отправка через Celery
- **Админ-панель**: Кастомная модель User интегрирована с Django admin

## Технологии

- **Backend**: Django 4.2, Django REST Framework
- **Аутентификация**: JWT, allauth
- **База данных**: PostgreSQL (Docker), Redis для кэша
- **Асинхронность**: Celery + Redis
- **WebSocket**: Channels + Redis
- **GraphQL**: Graphene-Django
- **Платежи**: Stripe
- **Поиск**: Elasticsearch
- **PDF**: ReportLab
- **Контейнеризация**: Docker + docker-compose
- **Безопасность**: Rate limiting, audit log

## Установка и запуск

### Локальная разработка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Создайте файл `.env` на основе `.env.example`
5. Примените миграции:
   ```bash
   python manage.py migrate
   ```
6. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```
7. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

### Docker

1. Создайте файл `.env` с переменными окружения
2. Запустите сервисы:
   ```bash
   docker-compose up --build
   ```

### Дополнительные команды

- **Запуск Celery worker**:
  ```bash
  celery -A head worker -l info
  ```
- **Запуск Celery beat**:
  ```bash
  celery -A head beat -l info
  ```
- **Запуск Elasticsearch** (локально):
  ```bash
  docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.17.0
  ```
- **Создание индексов Elasticsearch**:
  ```bash
  python manage.py search_index --rebuild
  ```

## API Endpoints

### Аутентификация
- `POST /api/v1/auth/register/` - Регистрация
- `POST /api/v1/auth/login/` - Вход
- `GET /api/v1/auth/profile/` - Профиль пользователя

### Курсы
- `GET /api/v1/courses/` - Список курсов
- `POST /api/v1/courses/` - Создать курс
- `GET /api/v1/courses/{id}/` - Детали курса
- `GET /api/v1/courses/search/?q=query` - Поиск через Elasticsearch

### Уроки
- `GET /api/v1/lessons/` - Список уроков
- `POST /api/v1/lessons/` - Создать урок
- `GET /api/v1/lessons/{id}/` - Детали урока

### Тесты
- `GET /api/v1/quizzes/` - Список тестов
- `POST /api/v1/quizzes/{id}/start/` - Начать тест
- `POST /api/v1/quizzes/attempt/{id}/submit/` - Отправить ответы

### Прогресс
- `GET /api/v1/progress/` - Прогресс пользователя
- `POST /api/v1/progress/enroll/{course_id}/` - Записаться на курс
- `POST /api/v1/progress/complete-lesson/{lesson_id}/` - Завершить урок

### Платежи
- `GET /api/v1/payments/` - История платежей
- `POST /api/v1/payments/create-intent/{course_id}/` - Создать платеж Stripe
- `POST /api/v1/payments/confirm/{payment_id}/` - Подтвердить платеж

### Отзывы
- `GET /api/v1/reviews/` - Список отзывов
- `POST /api/v1/reviews/` - Создать отзыв

### Уведомления
- `GET /api/v1/notifications/` - Список уведомлений
- `WebSocket ws://localhost:8000/ws/notifications/` - Реальное время

### Рекомендации
- `GET /api/v1/recommendations/` - Рекомендованные курсы

### GraphQL
- `POST /graphql/` - GraphQL API

### Admin
- `/admin/` - Панель администратора

## Структура проекта

```
education_platform/
├── head/                 # Основное приложение
├── users/                # Пользователи и аутентификация
├── courses/              # Курсы
├── lessons/              # Уроки
├── quizzes/              # Тесты
├── progress/             # Прогресс обучения
├── payments/             # Платежи
├── reviews/              # Отзывы
├── analytics/            # Аналитика
├── notifications/        # Уведомления (WebSocket)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Развертывание

1. Настройте PostgreSQL и Redis
2. Установите переменные окружения
3. Соберите статические файлы:
   ```bash
   python manage.py collectstatic
   ```
4. Запустите Gunicorn:
   ```bash
   gunicorn head.wsgi:application
   ```
5. Настройте Nginx для статических файлов и прокси

## Тестирование

Запустите тесты для всех приложений:
```bash
python manage.py test
```

Запустите тесты для конкретного приложения:
```bash
python manage.py test users
```

## Разработка

- Используйте `flake8` для линтинга
- Запускайте тесты: `python manage.py test`
- Для разработки используйте `DEBUG=True`
- Используйте `python manage.py shell` для интерактивной оболочки

## Особенности реализации

- **Асинхронная обработка**: Email и PDF генерируются через Celery
- **Реальное время**: WebSocket уведомления через Channels
- **Поиск**: Elasticsearch для быстрого поиска курсов
- **Рекомендации**: Коллаборативная фильтрация на основе взаимодействий
- **Безопасность**: JWT токены, rate limiting, аудит логов
- **Масштабируемость**: Docker контейнеры, Redis кэш

## Лицензия

MIT License