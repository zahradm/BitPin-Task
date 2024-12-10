# BitPin-task


## Overview

This project is a web application that provides an API for managing users and posts. It includes functionality for user authentication and scoring posts.

## Technologies Used

This project uses the following technologies:

- ![Python](https://img.shields.io/badge/Python-3.11-blue)
- ![Django](https://img.shields.io/badge/django-3.8.1-blue)
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue)
- ![Docker](https://img.shields.io/badge/Docker-20.10-blue)

## Setup and Installation

### Development Setup

To set up the application for development, run the following command:

```bash
docker-compose up -d --build
```
This will build the necessary containers and start the application in development mode.

### Production Setup
To set up the application for production, follow these steps:

Run the following command to start the application in production mode:

```bash

docker-compose -f docker-compose.prod.yml up -d --build
```
Once the containers are up and running, execute the migrations:

```bash

docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
```
This will apply the database migrations for production.

### API Endpoints
| Endpoint                 | Method | Request Body                              | Description                                               |
|--------------------------|--------|--------------------------------------------|-----------------------------------------------------------|
| `/user/token`            | POST   | `{ "username": "test", "password": "1234" }` | This endpoint returns a token for authenticated requests. |
| `/api/posts`             | GET    | N/A                                        | This endpoint retrieves a list of posts.                  |
| `/api/posts/1/`          | POST   | `{ "score": 5 }`                           | This endpoint allows submitting a score for post with ID 1. |