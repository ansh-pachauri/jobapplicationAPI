# Job Application API

A small Django REST API for job postings and applications. This repository uses Django, Django REST Framework, and Simple JWT for token-based authentication.

This README covers local setup, running the development server, running tests, and examples for obtaining JWT tokens and using the `apply` endpoint. Commands are tailored for Windows PowerShell (your environment).

---

## Prerequisites

- Python 3.11+ / 3.12 / 3.13 (project tested with Python 3.13 in this workspace)
- Git (optional)
- (Recommended) A virtual environment (venv)

The repository already includes a virtual environment at `env/` in this workspace. If you prefer to create a new one, see the steps below.

---

## Quick setup (recommended)

Open PowerShell and run the following from the project root (the folder that contains `manage.py` — `jobApi`):

```pwsh


# If you don't have the virtualenv and want to create one instead:
# python -m venv env
# & .\env\Scripts\Activate.ps1

# Install dependencies (if you don't have them installed already)
# If you have a requirements.txt, use:
# pip install -r requirements.txt

# Otherwise install the main packages used by this project:
pip install django djangorestframework djangorestframework-simplejwt

# Apply migrations
python manage.py migrate

# (Optional) Create a superuser to access Django admin
python manage.py createsuperuser

# Start the dev server
python manage.py runserver
```

The server should be available at `http://127.0.0.1:8000/`.

---

## Running tests

To run all tests in the `api` app:

```pwsh
# from project root
python manage.py test api
```

---
