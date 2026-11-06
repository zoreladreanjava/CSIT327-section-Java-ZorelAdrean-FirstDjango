# CampusConnect

**Name:** Zorel Adrean Rivera Java

**Section:** G5

## How to run

Requires Python 3.12 or newer. These commands are for Windows.

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py createsuperuser
.venv\Scripts\python manage.py runserver
```

Then open http://127.0.0.1:8000/.

To see the admin panel, go to http://127.0.0.1:8000/admin/, open your superuser account and set **Role** to **Administrator**.

To run the tests:

```powershell
.venv\Scripts\python manage.py test
```

A `.env` file is optional. Without one, the app uses a random secret key and logs everyone out each time the server restarts. See `.env.example` to set a fixed key.
