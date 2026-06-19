# WallSpace

WallSpace is a collaborative sticky-note web application built with Django and Django REST Framework. It enables users to create digital walls, organize notes, and collaborate with others through a role-based permission system. The application supports both a session-based web interface and a JWT-protected REST API, making it suitable for both browser and API clients.

## Features

* **Collaborative Walls**: Create, rename, update, and delete personal walls.
* **Sticky Notes**: Add, edit, move, resize, recolor, and delete notes on a wall.
* **Role-Based Collaboration**: Invite users as **Viewer** or **Editor**, with the owner having full control over wall management.
* **REST API**: Complete CRUD APIs for users, walls, notes, and member management secured using JWT authentication.
* **Session Optimization with Redis**: Frontend user sessions are stored in Redis (Upstash) for faster authentication and reduced database load.
* **Production Deployment**: Deployed on Render using Neon PostgreSQL as the primary database.

## Tech Stack

* **Backend:** Django 6, Django REST Framework
* **Frontend:** HTML, CSS, Bootstrap, JavaScript
* **Database:** PostgreSQL (Neon)
* **Caching:** Redis (Upstash)
* **Authentication:** Django Sessions, JWT (SimpleJWT)
* **Deployment:** Render

## Installation

1. Clone the repository.

```bash
git clone <repository-url>
cd wallspace
```

2. Create and activate a virtual environment.

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Install the required packages.

```bash
pip install -r requirements.txt
```

4. Configure the required environment variables.

```env
SECRET_KEY=
DATABASE_URL=
REDIS_URL=
DEBUG=
```

5. Apply migrations and start the development server.

```bash
python manage.py migrate
python manage.py runserver
```

## REST API

The project exposes REST APIs for:

* User Registration
* JWT Authentication
* User Profile
* Wall Management
* Note Management
* Member Invitation
* Role Management

## Project Structure

* `users/` – Authentication and user management
* `walls/` – Wall creation and collaboration features
* `notes/` – Sticky note functionality
* `templates/` – HTML templates
* `static/` – CSS, JavaScript, and images
* `sql/` – PostgreSQL database schema
* `requirements.txt` – Python dependencies

## Database

The project uses **Neon PostgreSQL** as the production database. A SQL schema export is available in:

```text
sql/wallspace_schema.sql
```

## Deployment

* **Application:** Render
* **Database:** Neon PostgreSQL
* **Session Cache:** Upstash Redis

## Author

**Prithvish Mohanty**

Developed as part of a Full Stack Application Development Internship.
