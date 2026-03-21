# The Hancox Wedding Sweepstake

A fun and interactive betting game for wedding guests to predict the answers to questions throughout your wedding day.

## Features

- 🔍 Guest search with fuzzy autocomplete
- 📊 4 customizable questions with number/time-based answers
- 🎯 2x2 grid layout with interactive sliders for fast throughput (~1.5 min/guest)
- 📱 QR code generation per guest for scanning their own answers
- 📈 Real-time leaderboard with accuracy-based scoring (APE)
- 👨‍💼 Admin interface to enter actual answers and view all guest QR codes
- 💾 Local SQLite database — no internet required on wedding day
- 🎮 Touch-optimized UI for tablet kiosk (Fully Kiosk Browser)
- 📲 Installable as a PWA (standalone, no browser chrome)

## System Requirements

- **Python 3.7+** installed on your computer/tablet
- **Android tablet** (or Windows tablet) running **Fully Kiosk Browser** (F-Droid)
- **WiFi** available at your venue
- **Port 5000** available on your device

## Installation

### 1. Install Python Dependencies

Open a terminal in the `wedding-game` directory and run:

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** - Web framework
- **qrcode** - QR code generation
- **Pillow** - Image processing
- **python-dotenv** - Environment configuration

### 2. Prepare Guest List

Edit `data/guests.csv` and replace the sample names with your actual guests:

```csv
first_name,last_name
John,Smith
Jane,Doe
Robert,Johnson
...
```

**Important**: Use exactly the spelling your guests expect (first name and last name in separate columns).

### 3. Configure Questions

Edit `config.py` and update the `QUESTIONS` list (currently 4 questions — ceremony start, speech duration, thank-you count, cake cutting):

```python
QUESTIONS = [
    {
        "text": "Your question here?",
        "short_label": "Short Label",
        "type": "number",  # or "time"
        "unit": "minutes",
        "order": 1,
        "min": 0,
        "max": 120
    },
    # ... more questions
]
```

### 4. Set Admin Password (Optional but Recommended)

Edit `config.py` and change the `ADMIN_PASSWORD`:

```python
ADMIN_PASSWORD = 'YourSecurePassword'
```

## Running the Application

### On Your Computer (Testing)

```bash
python app.py
```

Then open your browser to: `http://localhost:5000`

### On Wedding Day (Tablet)

The server auto-detects its local IP — no manual config needed.

1. **Start the server**:
   - Windows: Double-click `start.bat`
   - Android (Termux): `bash start.sh`

2. **Open Fully Kiosk Browser** → point at `http://localhost:5000`
   - FKB hides status bar, time, WiFi, battery for a clean kiosk look
   - Tip: Settings → Web Content → disable "Show Loading Progress Bar"

3. **QR codes for guests' phones** point to `http://[tablet-local-ip]:5000/answers/[token]`
   — the IP is detected automatically at startup

4. **Admin interface** (groomsman's phone):
   - Visit: `http://[tablet-ip]:5000/admin/login`
   - Login with your admin password
   - Update actual answers as events happen
   - View guest QR codes and their answers
   - Check leaderboard in real-time

## How It Works

### Guest Flow

1. **Home Screen**: Tap "Start"
2. **Search**: Find your name by typing
3. **Questions**: Answer 4 questions on a 2x2 grid (all visible at once)
   - Adjust sliders with nudge buttons for fine control
   - Toggle to "one at a time" mode if preferred
4. **Submit**: Tap "Submit Answers" → inline confirmation modal shows chosen values
5. **QR Code**: Scan with phone to save your answers
6. **Leaderboard**: Check your ranking (once answers are revealed)

### Admin Flow

1. Navigate to: `http://[tablet-ip]:5000/admin/login`
2. Login with admin password (session lasts 24 hours)
3. **Dashboard**: Update actual answers as events happen
4. **Guest List**: View all guests, QR codes, and each guest's submitted answers
5. **Leaderboard**: View real-time rankings
6. **Responses**: Detailed view of all guest answers per question

## Scoring System

**Lower score = Better (Closer to actual answer)**

Score = Average Percentage Error

For each question:
- Error = |Your Guess - Actual Answer| / Actual Answer × 100%
- Final Score = Average of all question errors

Example:
- Question 1: Your guess 30, Actual 25 → Error = 20%
- Question 2: Your guess 150, Actual 100 → Error = 50%
- Final Score = (20% + 50%) / 2 = 35%

## Customization

### Questions

All questions can be customized in `config.py`. Options:

```python
{
    "text": "Question text here?",
    "short_label": "Short Label",  # Shown on grid cards
    "type": "number" or "time",
    "unit": "unit name (minutes, mentions, etc)",
    "order": 1-4 (display order),
    "min": 0,           # Min slider value (or "HH:MM" for time)
    "max": 1000         # Max slider value (or "HH:MM" for time)
}
```

### Colors & Styling

Edit `static/css/style.css` CSS variables at `:root` to customize:
- Primary (Dark Teal): `#348686`
- Accent (Confetti Dark): `#540f3b`
- Dark mode is the default; light mode via `prefers-color-scheme: light`

### Admin Password

Edit `config.py`:
```python
ADMIN_PASSWORD = 'YourNewPassword'
```

## Troubleshooting

### "Module not found" errors

**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt
```

### Database file not created

**Solution**: First run initializes database automatically. If issues persist:
```bash
python database.py
```

### Tablet can't access the game

**Solution**:
1. Make sure tablet and groomsman's phone are on same WiFi
2. Check tablet IP with `ipconfig`
3. Update `BASE_URL` in `config.py`
4. Restart with `python app.py`

### Guest not in list

**Options**:
1. Re-spell their name in the search — fuzzy search will find close matches
2. Use **manual entry**: type any name in the search box and select "Enter manually as [name]"
3. Add them to `data/guests.csv` and restart before the event

### QR codes don't scan

**Solution**:
1. Increase brightness on tablet
2. Try different phones to test
3. Ensure `BASE_URL` in config matches tablet IP

### Admin password forgotten

**Solution**:
1. Edit `config.py`
2. Change `ADMIN_PASSWORD` to new value
3. Restart server with `python app.py`

## Backup & Recovery

### Manual Backup

Copy the database file while the server is not running:
```bash
copy data\wedding.db data\Backups\wedding_backup_%date%.db
```

### Restore

Copy any backup back to `data/wedding.db` (with the server stopped):
```bash
copy data\Backups\wedding_backup_[date].db data\wedding.db
```

## Wedding Day Setup Checklist

### One Week Before
- [ ] Load all guests into `data/guests.csv`
- [ ] Finalize all 4 questions in `config.py`
- [ ] Test with 5 mock guests on your computer
- [ ] Update admin password if desired

### Day Before
- [ ] Connect tablet to power
- [ ] Test WiFi signal at venue
- [ ] Download and save this README on tablet
- [ ] Print admin password on card for groomsman

### Day Of (30 minutes before guests arrive)
- [ ] Start server: Double-click `start.bat` (Windows) or `bash start.sh` (Termux)
- [ ] Open Fully Kiosk Browser → `http://localhost:5000`
- [ ] Test one complete guest submission
- [ ] Place tablet on stand at entrance
- [ ] Give groomsman:
  - Admin URL: `http://[tablet-ip]:5000/admin/login`
  - Admin password
  - Instructions card

### During Event
- [ ] Groomsman updates actual answers as events happen
- [ ] Monitor submission count on dashboard
- [ ] Check leaderboard periodically

### After Event
- [ ] Export final data: Admin Dashboard → Export Data
- [ ] Save CSV with all guest answers
- [ ] Announce winner from leaderboard

## File Structure

<!-- AUTO-GENERATED from codebase — do not edit this section manually -->
```
wedding-game/
├── app.py                    # Main Flask application, all routes
├── database.py               # All SQLite operations (no raw SQL in app.py)
├── config.py                 # Config constants, QUESTIONS, quips, credentials
├── requirements.txt          # Python dependencies
├── start.bat                 # Windows startup script
├── start.sh                  # Android/Termux startup script
├── README.md                 # This file
├── CLAUDE.md                 # AI assistant context
├── SETUP_GUIDE.md            # Detailed setup walkthrough
├── TROUBLESHOOTING.md        # Common issues
├── data/
│   ├── wedding.db            # SQLite database (auto-created on first run)
│   ├── guests.csv            # Guest list (edit before wedding)
│   ├── qr_codes/             # Generated QR code images
│   └── Backups/              # Manual database backups
├── static/
│   ├── css/style.css         # Styling — dark palette, CSS variables, animations
│   ├── css/bootstrap.min.css # Bootstrap 5.3 (bundled locally)
│   ├── js/                   # bootstrap.bundle.min.js, fuse.min.js (bundled)
│   ├── fonts/                # Cormorant Garamond, Outfit, Cinzel (bundled)
│   ├── images/               # PWA icons (icon-192.png, icon-512.png)
│   ├── manifest.json         # PWA manifest (display: standalone)
│   └── sw.js                 # Service worker for PWA installability
└── templates/                # 18 Jinja2 templates, all extend base.html
    ├── base.html             # Shared layout, logout modal, service worker reg
    ├── home.html             # Start screen with guest QR codes modal
    ├── search.html           # Guest search (Fuse.js fuzzy + manual entry)
    ├── questions_all.html    # 2x2 grid mode (default) — all 4 sliders at once
    ├── question.html         # One-at-a-time mode with dot progress indicator
    ├── summary.html          # Answer review (one-at-a-time mode)
    ├── confirmation.html     # Thank you + confetti + QR code
    ├── guest_answers.html    # Answer view via QR scan token
    ├── qr_codes.html         # QR code menu
    ├── qr_code_display.html  # Single guest QR display
    ├── admin_login.html      # Admin login
    ├── admin_dashboard.html  # Admin — update actual answers
    ├── admin_guests.html     # Admin — guest list, QR codes, submitted answers
    ├── leaderboard.html      # Live scores
    ├── admin_responses.html  # All responses per question
    ├── admin_stats.html      # Event statistics
    ├── 404.html              # Page not found
    └── 500.html              # Server error
```
<!-- END AUTO-GENERATED -->

## Commands Reference

<!-- AUTO-GENERATED from requirements.txt, start.bat, start.sh -->
| Command | Platform | Description |
|---------|----------|-------------|
| `pip install -r requirements.txt` | All | Install Python dependencies |
| `python app.py` | All | Run the server on 0.0.0.0:5000 |
| `python database.py` | All | Initialise / reset the database |
| `start.bat` | Windows | One-click server start |
| `bash start.sh` | Android/Termux | Start server on tablet |

**Dependencies** (`requirements.txt`):

| Package | Version | Purpose |
|---------|---------|---------|
| `Flask` | 3.0.0 | Web framework |
| `qrcode[pil]` | 7.4.2 | QR code generation (includes Pillow) |
| `python-dotenv` | 1.0.0 | `.env` file support |
<!-- END AUTO-GENERATED -->

## Advanced Configuration

### Changing Server Port

Edit `config.py`:
```python
PORT = 8080  # Instead of 5000
```

### Debug Mode

Edit `config.py` (NOT for wedding day):
```python
DEBUG = True  # Shows detailed error messages
```

### Session Timeout

Edit `config.py`:
```python
SESSION_TIMEOUT = 14400  # 4 hours in seconds
```

## Support & Troubleshooting

If you encounter issues:

1. Check the terminal/console for error messages
2. Look at `wedding_game.log` for detailed logs
3. Verify all files are present and not corrupted
4. Try restarting the server
5. Verify Python and dependencies are installed correctly

## Tips for Success

✅ **Do:**
- Test thoroughly before the event
- Have a backup battery for the tablet
- Keep admin password written down safely
- Update actual answers frequently
- Check leaderboard periodically

❌ **Don't:**
- Change files while the server is running
- Disable WiFi during the event
- Forget to update admin answers
- Run multiple servers on same port
- Edit database while server is running

## Credits

Built for the Hancox wedding (11 April 2026).

Technologies: Python Flask · SQLite · Bootstrap 5.3 · Vanilla ES6 · Fuse.js · Cormorant Garamond / Outfit / Cinzel fonts

---

**Enjoy your wedding! 💍✨**

Last updated: 2026-03-21
