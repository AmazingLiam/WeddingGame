# CLAUDE.md

## Project Overview

Wedding Betting Game — a Flask web app where wedding guests predict wedding day events (e.g., ceremony start time, number of photos). Touch-optimized tablet UI with admin controls, leaderboards, QR code answer verification. For Fran & Liam Hancox's wedding (11/04/2026). Runs on local WiFi with no internet required.

## Tech Stack

- **Backend:** Python 3.7+ / Flask 3.0.0 / SQLite3
- **Frontend:** Jinja2 templates, Bootstrap 5.3.0 (bundled locally), Vanilla ES6 JavaScript, Fuse.js (bundled locally)
- **Deployment:** Android tablet via Termux + `start.sh`, or Windows via `start.bat`. Local network (0.0.0.0:5000)
- **Kiosk browser:** **Fully Kiosk Browser** (F-Droid) used on tablet — hides status bar, time, WiFi, battery. Point at `http://localhost:5000`.
- **PWA:** Installable as standalone app (no browser chrome) via `manifest.json` + service worker

## Project Structure

```
app.py           — Main Flask app, routes, session management
database.py      — All SQLite operations, no raw SQL in app.py (includes schema migrations)
config.py        — Config constants, question definitions, credentials
start.bat        — Windows startup script
start.sh         — Android/Termux startup script
data/            — wedding.db (auto-created), guests.csv, qr_codes/, Backups/
static/
  css/           — style.css, bootstrap.min.css (local)
  js/            — bootstrap.bundle.min.js (local), fuse.min.js (local)
  images/        — background.jpg, icon-192.png, icon-512.png (PWA icons)
  manifest.json  — PWA manifest (display: standalone)
  sw.js          — Service worker for PWA installability
templates/       — 17 Jinja2 templates extending base.html (added admin_guests.html)
```

## Commands

```bash
pip install -r requirements.txt   # Install deps (flask, qrcode, python-dotenv)
python app.py                     # Run server (Windows or Termux)
python database.py                # Initialize/reset database
start.bat                         # Windows startup script
bash start.sh                     # Android/Termux startup script
```

## Architecture

- **Three-tier:** Flask routes → database.py abstraction → SQLite
- **Session-based:** Guest progress stored server-side (guest_id, guest_name, current_question, answers dict, admin flag)
- **Route protection:** `@admin_required` decorator for admin routes
- **API pattern:** `/api/*` endpoints return `jsonify()` with `success`/`error` fields
- **Scoring:** Average Percentage Error — lower score wins
- **Template filter:** `@app.template_filter('format_time')` converts minutes to HH:MM
- **PWA:** Service worker served from `/sw.js` route (root scope). Guest screens hide navbar/footer via `{% block navbar %}{% endblock %}` overrides

## Database Schema

Four tables: `guests` (id, name, submission status, QR token), `questions` (text, type, order, short_label, actual_answer), `responses` (guest_id, question_id, answer), `admin_config` (key-value pairs)

**Migration:** `database.py` auto-adds `short_label` column to existing databases via `ALTER TABLE` in `init_db()`.

## Coding Conventions

- **Python:** PEP 8, snake_case functions/variables, UPPERCASE constants, parameterized SQL queries, try/finally for DB connections, section headers with `# ====`
- **HTML:** Jinja2 with Bootstrap 5 grid, all templates extend `base.html`, kebab-case CSS classes, `data-*` attributes for config. Guest templates override `{% block navbar %}` and `{% block footer %}` with empty blocks to hide them
- **CSS:** CSS variables at `:root` for theming, kebab-case selectors, section comments. Comprehensive dark mode support via `@media (prefers-color-scheme: dark)`
- **JS:** Vanilla ES6, camelCase functions, Fetch API with error handling, global functions for HTML onclick, no framework
- **Files:** Python `snake_case.py`, templates `snake_case.html`, single `style.css`

## Key Patterns

- All SQL lives in `database.py` — function naming: `get_*()`, `save_*()`, `search_*()`, `calculate_*()`, `update_*()`
- Client-side + server-side form validation
- Time questions stored as total minutes internally
- QR codes use unique token per guest for answer access
- Console logging for diagnostics on startup and errors
- Consistent JSON API responses with `success`/`error` fields
- CDN dependencies bundled locally in `static/css/` and `static/js/` (no internet required)
- Fullscreen API triggered on guest "Start" button as backup for non-PWA access
- Anti-accidental-exit CSS: `overscroll-behavior: none`, `user-select: none` in standalone mode
- Admin session is permanent (24 h) — `session.permanent = True` + `app.permanent_session_lifetime = timedelta(hours=24)`
- Submitted guests are locked on the search page — `has_submitted` returned by `search_guests()`, grayed out in UI with in-page banner instead of browser alert
- Logout uses a confirmation modal defined in `base.html` (shared by navbar ✖ and dashboard button); functions `showLogoutModal()` / `hideLogoutModal()` are global
- `all_answered` flag passed from question route to template — drives "Back to Review" shortcut button when editing a previously answered question
- `/admin/guests` route + `admin_guests.html` — lists all guests, submitted ones have a View QR modal

## Color Scheme

Primary (Dark Teal) `#02403d`, Secondary (Dark Blue) `#143850`, Accent (Mauve) `#754956`, Light (Cyan) `#b9d5d5`, Light Alt (Pink) `#f9d5d5`

**Dark mode:** Full dark theme via `@media (prefers-color-scheme: dark)` — covers body, cards, forms, buttons, progress bars, sliders, alerts, modals, tables, admin containers. Key dark colours: body `#1a1a1a`, cards `#2d2d2d`, inputs `#3d3d3d`, text `#e0e0e0`, headings `#4dd4c7`. Bootstrap 5 CSS custom properties (`--bs-card-bg`, `--bs-table-bg`) are overridden alongside `background-color !important` to ensure dark backgrounds apply correctly.

## Android Tablet Deployment

1. Install **Termux** from F-Droid
2. In Termux: `pkg update && pkg install python && pip install flask qrcode python-dotenv pillow`
3. Transfer project folder to tablet
4. Run: `bash start.sh` (or `python app.py`)
5. Open **Fully Kiosk Browser** (F-Droid) → point at `http://localhost:5000` — hides status bar fully
6. (Alternative) Open Chrome → `http://localhost:5000` → Chrome menu → "Install app" for standalone PWA mode

## Testing

No automated tests. Manual testing: search, question navigation, answer persistence, admin ops, QR generation/scanning, leaderboard calculation, session expiration. Test dark mode via DevTools → Rendering → prefers-color-scheme: dark.
