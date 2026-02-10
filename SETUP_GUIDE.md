# Wedding Betting Game - Setup Guide

## Quick Start

### 1. First Run - Initialize Everything
```bash
python app.py
```

This will:
- Create the SQLite database
- Load all 87 guests from `data/guests.csv`
- Load all 8 questions from `config.py`
- Start the server on http://localhost:5000

**The app is ready!**

### 2. Access on Your Computer
Open your browser and go to: `http://localhost:5000`

### 3. Testing the Search
Try searching for:
- **Fran** - should find "Fran Hancox"
- **Liam** - should find "Liam Hancox"
- **Hancock** - should find all Hancox family members
- **Austin** - should find both Austin guests

## Customizing Your Wedding

### Change Background Image
Replace the file: `static/images/background.jpg`
- Any image size works (will scale automatically)
- Supported formats: JPG, PNG, WebP
- Recommended: 1920x1080 or wider

### Edit Guest List
Edit: `data/guests.csv`
- Format: `first_name,last_name`
- One guest per line
- Example: `John,Smith`

### Change Questions
Edit: `config.py` → QUESTIONS section
```python
QUESTIONS = [
    {
        "text": "Your question here?",
        "type": "number",  # or "time"
        "unit": "minutes",
        "order": 1,
        "min": 0,
        "max": 100
    },
    # Add more questions...
]
```

### Change Admin Password
Edit: `config.py`
```python
ADMIN_PASSWORD = 'YourNewPassword'
```

### Change Footer Text
Edit: `templates/base.html`
Find the footer section and change:
```html
<p class="mb-0">Fran & Liam Hancox 11/04/2026</p>
```

## Running on Wedding Day

### On Your Tablet
1. Open Command Prompt
2. Navigate to the game folder
3. Run: `python app.py`
4. Or double-click: `start.bat`

### Getting Tablet IP
```bash
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

### Update Base URL
In `config.py`, find:
```python
BASE_URL = 'http://localhost:5000'
```
Change to:
```python
BASE_URL = 'http://192.168.1.100:5000'
```

### Guest Access
Guests visit: `http://192.168.1.100:5000` (or scan QR code from tablet)

### Admin Access
You/Groomsman visit: `http://192.168.1.100:5000/admin`
Login with your admin password

## Troubleshooting

### Search Not Finding Names
1. The database loads on first server start
2. If you added new names to CSV after first run, restart the server
3. Clear browser cache (Ctrl+Shift+Del)

### Background Image Not Showing
1. Check file exists: `static/images/background.jpg`
2. Try a different image format (PNG instead of JPG)
3. Check browser console for errors (F12)

### Server Won't Start
1. Make sure Python is installed: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Check port 5000 is not in use

### Tablet Can't Access
1. Check tablet and computer are on same WiFi
2. Verify IP address is correct
3. Try: `http://192.168.1.100:5000` in tablet browser
4. Check Windows Firewall isn't blocking Python

## File Guide

| File | Purpose |
|------|---------|
| `app.py` | Main server code |
| `config.py` | Questions, admin password, settings |
| `database.py` | Database operations |
| `data/guests.csv` | Guest list (edit this) |
| `static/images/background.jpg` | Home page background (replace) |
| `static/css/style.css` | Colors and styling |
| `templates/` | HTML pages |

## Color Scheme

Your wedding colors are set to:
- **Primary (Dark Teal):** #02403d
- **Secondary (Dark Blue):** #143850
- **Accent (Mauve):** #754956
- **Light (Cyan):** #b9d5d5
- **Light Alt (Pink):** #f9d5d5

To change colors, edit `static/css/style.css` CSS variables at the top.

## Backup Your Data

### During Wedding
Every time you want to save a backup:
1. Go to: `http://192.168.1.100:5000/admin`
2. Click: "Export Data"
3. Save the CSV file

### Auto Backup
Database file: `data/wedding.db`
- Contains all responses
- Safe if server crashes
- Back it up after event!

## Day-of Checklist

- [ ] Test server start: `python app.py`
- [ ] Test search (try "Fran" and "Liam")
- [ ] Load background image
- [ ] Update admin password
- [ ] Update BASE_URL in config.py
- [ ] Test on tablet
- [ ] Test with mock guest
- [ ] Verify QR codes scan
- [ ] Print admin password
- [ ] Have USB backup ready

---

Enjoy your wedding! 💍✨
