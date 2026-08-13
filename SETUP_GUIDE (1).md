# EcoForce — Local Setup Guide

This gets the Django app (`ecoforce/`) running on your machine with the demo data already loaded. For deploying it live, see the "Deploying the Real App" section in `README.md` instead — this guide is local-only.

## Prerequisites

- **Python 3.10–3.12** (check with `python3 --version`)
- **pip** (comes with Python)
- **git** (only needed if you're cloning from GitHub rather than using the zip)

## 1. Get the code

If you have the zip: unzip it, then open a terminal in the `ecoforce/` folder (the one containing `manage.py`).

```bash
cd ecoforce
```

If you're cloning from GitHub instead:

```bash
git clone <your-repo-url>
cd ecoforce
```

## 2. Create and activate a virtual environment

Keeps this project's packages separate from everything else on your system.

```bash
python3 -m venv venv
```

Activate it:

```bash
# macOS / Linux
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

You'll know it worked when your terminal prompt shows `(venv)` at the start of the line. Do this every time you open a new terminal to work on the project.

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs Django, Pillow (image handling), gunicorn, whitenoise, and the other packages listed in `requirements.txt`.

## 4. Set up environment variables (optional for local dev)

Copy the example file:

```bash
cp .env.example .env   # macOS/Linux
copy .env.example .env # Windows
```

For local development you can usually leave the defaults as-is (`DEBUG=True`, no `DATABASE_URL` set — it falls back to the bundled SQLite database). Django doesn't load `.env` files automatically on its own, so either:
- install `python-dotenv` and load it at the top of `manage.py`/`config/settings.py`, or
- just export the variables in your shell before running commands, or
- skip this step entirely — the built-in defaults in `config/settings.py` already work for local dev without any `.env` file.

## 5. Run database migrations

Creates the SQLite database tables (users, requests, categories, ratings, etc.).

```bash
python manage.py migrate
```

## 6. Seed demo data

Populates the database with sample categories, users, volunteers, cleaning requests, and ratings, so the app looks alive right away instead of empty.

```bash
python manage.py seed_data
```

This creates the following login accounts (all with password `password123`):

| Role | Username | Notes |
|---|---|---|
| Administrator | `admin` | `/dashboard/admin/` and `/admin/` |
| Citizen User | `alice_m` | Can post requests & rate volunteers |
| Citizen User | `bob_smith` | Can post requests & rate volunteers |
| Volunteer | `alex_v` | Can accept tasks & update progress |
| Volunteer | `brittany_c` | Can accept tasks & update progress |

**Skip this step if you'd rather start with a completely empty database** — just run `python manage.py createsuperuser` instead (see step 8).

## 7. Collect static files (optional locally, required before deploying)

```bash
python manage.py collectstatic --no-input
```

Django's dev server can serve static files without this, but it's good practice to confirm it works before you deploy.

## 8. (Optional) Create your own admin account

If you skipped seeding or want a personal superuser login:

```bash
python manage.py createsuperuser
```

Follow the prompts for username, email, and password.

## 9. Run the development server

```bash
python manage.py runserver
```

You should see output ending in something like:

```
Starting development server at http://127.0.0.1:8000/
```

Open that URL in your browser.

## Important pages to check

| URL | What's there |
|---|---|
| `/` | Public landing page |
| `/accounts/login/` | Log in |
| `/accounts/register/` | Sign up as a citizen |
| `/accounts/register/volunteer/` | Sign up as a volunteer |
| `/requests/` | Browse & filter cleaning requests |
| `/requests/create/` | Post a request with the Leaflet map pin |
| `/dashboard/user/` | Citizen dashboard |
| `/volunteers/dashboard/` | Volunteer dashboard & feed |
| `/dashboard/admin/` | Admin operational panel & charts |
| `/impact/` | Public big-screen impact dashboard |
| `/admin/` | Django's built-in admin interface |

## Everyday commands (once set up)

```bash
# Activate the virtual environment (every new terminal session)
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate.bat       # Windows

# Run the server
python manage.py runserver

# After changing any models.py file
python manage.py makemigrations
python manage.py migrate

# Reset and reseed demo data from scratch
rm db.sqlite3                   # macOS/Linux — deletes the local database
del db.sqlite3                  # Windows
python manage.py migrate
python manage.py seed_data
```

## Troubleshooting

**`ModuleNotFoundError: No module named 'django'`**
Your virtual environment isn't activated, or dependencies weren't installed. Re-run steps 2 and 3.

**`django.db.utils.OperationalError: no such table`**
Migrations haven't been run yet. Run `python manage.py migrate`.

**Port 8000 already in use**
Run on a different port: `python manage.py runserver 8080`

**Images/photos don't show up**
Make sure `DEBUG=True` locally (the dev server only serves user-uploaded media itself in debug mode) and that you've posted a request with a photo attached after seeding.

**Static files (CSS/icons) look broken**
Run `python manage.py collectstatic --no-input`, then restart the server.

## Project structure at a glance

```
ecoforce/
├── manage.py              # Django's command-line entry point
├── requirements.txt       # Python dependencies
├── db.sqlite3             # Local database (created after migrate)
├── config/                 # Project settings, URLs, WSGI
├── accounts/                # Custom User model, auth views, volunteer profiles
├── requests_app/            # Cleaning requests, categories, task assignments, ratings
├── volunteers/               # Volunteer dashboard & feed
├── dashboard/                # User/admin dashboards + public impact dashboard
├── core/                      # Landing page + the seed_data management command
├── templates/                 # All HTML templates (Tailwind-styled)
├── static/ & staticfiles/     # CSS and collected static assets
└── index.html                 # Standalone static showcase page (for GitHub Pages only —
                                  not part of the Django app)
```

---

Once this is running locally and you're ready to share a live link instead, see the **"Deploying the Real App"** section in `README.md` for the Render deployment steps.
