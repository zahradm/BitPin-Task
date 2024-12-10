# BitPin Task

## 📖 Overview
This project is a web application that provides an API for managing **users** and **posts**. It includes features such as **user authentication** and **post scoring**.

---

## 🛠️ Technologies Used

- ![Python](https://img.shields.io/badge/Python-3.11-blue)
- ![Django](https://img.shields.io/badge/django-3.8.1-blue)
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
- ![Docker](https://img.shields.io/badge/Docker-26.0-blue)

---

## ⚙️ Setup and Installation

### 🚧 Development Setup

To set up the application for development, execute the following command:

```bash
docker compose up -d --build
```
This will build the necessary containers and start the application in development mode.

### 🏭 Production Setup
To set up the application for production, follow these steps:

Run the following command to start the application in production mode:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```
Once the containers are up and running, execute the migrations:

```bash
docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```
This will apply the database migrations for production.

### 📂 API Endpoints
| Endpoint                     | Method | Request Body                                                              | Description                                                       |
|------------------------------|--------|---------------------------------------------------------------------------|-------------------------------------------------------------------|
| `api/user/register-superuser/` | POST   | `{ "username": "test",  "email": "test@example.com", "password": "1234" }` | This endpoint creates superuser (just superuser can create post). |
| `api/user/register/`         | POST   | `{ "username": "test",  "email": "test@example.com", "password": "1234" }`  | This endpoint creates user.                                       |
| `api/user/token/`            | POST   | `{ "username": "test", "password": "1234" }`                              | This endpoint returns a token for authenticated requests.         |
| `api/post/list/`             | GET    | N/A                                                                       | This endpoint retrieves a list of posts.                          |
| `api/posts/rate/1/`          | POST   | `{ "score": 5 }`                                                          | This endpoint allows submitting a score for post with ID 1.       |