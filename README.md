<div align="center">

# 🍋 Little Lemon — Django REST API

> *Meta Back-End Developer Certificate · Course 6: APIs*

![DjangoREST](https://img.shields.io/badge/Django-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Django](https://img.shields.io/badge/Django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

---

## 📖 About

This is the final project for **Course 6: APIs** of the Meta Back-End Developer Certificate on Coursera. It is a fully functional REST API for **Little Lemon**, a fictional restaurant, built with Django REST Framework. The API handles menu items, orders, and user management.

---

## 🗂 Project Structure

```
META-DjangoAPI-Final-Project/
├── LittleLemon/        # Django project settings & config
├── LittleLemonAPI/     # REST API app (views, models, serializers, urls)
├── manage.py
├── Pipfile
└── db.sqlite3
```

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/menu-items` | List all menu items |
| GET/POST | `/api/menu-items/{id}` | Retrieve or create a menu item |
| GET | `/api/orders` | List orders |
| POST | `/api/orders` | Place a new order |
| GET/PATCH/DELETE | `/api/orders/{id}` | Manage a specific order |

---

## ⚙️ Setup & Installation

```bash
# Clone the repository
git clone https://github.com/RamzMA/META-DjangoAPI-Final-Project.git
cd META-DjangoAPI-Final-Project

# Install dependencies
pipenv install
pipenv shell

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Use **Postman** or **Insomnia** to interact with the API at `http://127.0.0.1:8000/api/`.

---

## 🛠 Tech Stack

- **Framework:** Django REST Framework
- **Language:** Python
- **Database:** SQLite
- **Dependency Management:** Pipenv

---

<div align="center">

*Part of the [Meta Back-End Developer Certificate](https://www.coursera.org/professional-certificates/meta-back-end-developer) on Coursera*

</div>
