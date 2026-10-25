# Fuel Tank API

A Django REST API and Vue dashboard for tracking fuel tank volumes and the sales they imply. I wrote this in 2024.

## The problem

Gas stations record tank volume readings throughout the day. The project has three parts:

1. **Model the data.** Tanks, volume readings, and daily sales, with full CRUD through a REST API.
2. **Derive sales from readings.** When a volume reading is created or edited, calculate the change from the previous reading (that day, or the last reading of the day before) and record it as sales.
3. **Report on it.** A running four-week average of sales for a tank as of a given date, plus a lookup of volume readings by date or exact timestamp.

After the API was done I added a small Vue 3 dashboard to browse volumes and daily sales and to look up the running average.

## Stack

- **Backend:** Python 3.10+, Django 5, Django REST Framework, SQLite
- **Frontend:** Vue 3, Vite, Axios, Bootstrap 5

## Running it

Backend, from the repo root:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata tanks_data.json   # sample tanks, readings, and sales
python manage.py runserver
```

The API is at http://localhost:8000/api/. DRF's browsable API lets you click through it.

Frontend, in a second terminal:

```sh
cd tank_fe
npm install
npm run dev
```

Then open http://localhost:5173. It expects the API on port 8000.

Tests:

```sh
python manage.py test tankapi
```

## Endpoints

| Method | Path | What it does |
|---|---|---|
| CRUD | `/api/tanks/` | Tanks |
| CRUD | `/api/tank-volumes/` | Volume readings. Creating or editing one recalculates sales. |
| CRUD | `/api/daily-tank/` | Derived sales records |
| GET | `/api/tanks/<id>/average-sales/<YYYY-MM-DD>/` | Running four-week average sales for a tank as of a date |
| GET | `/api/tank-volume-lookup/?date=YYYY-MM-DD` | Readings on a date (or `?datetime=` for an exact timestamp) |

## What I'd do differently now

I've spent the two and a half years since this writing production Rails, test-first. Looking back at it:

- **Put the sales calculation in the model layer, not the viewset.** Right now sales are only derived when a reading comes in through the API. A reading saved from the admin or a shell skips it.
- **Write the tests first, and test the behavior instead of calling viewset methods by hand.** The tests here still have debugging prints in them.
- **Make the grain of the sales table explicit.** It stores one row per reading interval, so "daily" sales and the running average's denominator don't quite mean what the names say. I'd roll it up to one row per tank per day, or rename it.
- **Use `DecimalField` for volumes and `timezone.now` for timestamps** instead of floats and naive datetimes.
- **Name the foreign keys `tank` rather than `tank_id`,** since Django already appends `_id` to the column.
- **Move the secret key, CORS settings, and the frontend's API URL into environment config** instead of hard-coding them for localhost.
