# 💍 Wedding Betting Game

A fun and interactive betting game for wedding guests to predict the answers to questions throughout your wedding day.

## Features

- 🔍 Guest search with autocomplete (90 guests)
- 📊 5-10 customizable questions with number/time-based answers
- 🎯 Interactive sliders and number inputs for easy answer selection
- 📱 QR code generation for sharing/scanning answers
- 📈 Real-time leaderboard with accuracy-based scoring
- 👨‍💼 Admin interface to update actual answers from phone
- 💾 Local SQLite database (no internet required)
- 🎮 Touch-optimized UI for tablet display

## System Requirements

- **Python 3.7+** installed on your computer/tablet
- **Google Pixel Tablet** (or any Android/Windows tablet)
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

Edit `data/guests.csv` and replace the sample names with your actual 90 guests:

```csv
first_name,last_name
John,Smith
Jane,Doe
Robert,Johnson
...
```

**Important**: Use exactly the spelling your guests expect (first name and last name in separate columns).

### 3. Configure Questions

Edit `config.py` and update the `QUESTIONS` list (currently 8 questions):

```python
QUESTIONS = [
    {
        "text": "Your question here?",
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

1. **Find tablet's IP address**:
   - Windows: Open Command Prompt and type `ipconfig`
   - Look for IPv4 Address (e.g., `192.168.1.100`)

2. **Update `config.py`** with the tablet's IP:
   ```python
   BASE_URL = 'http://192.168.1.100:5000'
   ```

3. **Double-click `start.bat`** (Windows) or run `python app.py`

4. **Access from guests' phones**:
   - Guests visit: `http://192.168.1.100:5000` (or scan QR code in corner)

5. **Admin interface** (groomsman):
   - Visit: `http://192.168.1.100:5000/admin` from their phone
   - Login with your admin password
   - Update actual answers as events happen
   - Check leaderboard in real-time

## How It Works

### Guest Flow

1. **Home Screen**: Tap "Start"
2. **Search**: Find your name by typing
3. **Questions**: Answer 5-10 questions (one at a time)
   - Use slider or direct number entry
   - Time questions in HH:MM format (e.g., 20:30)
4. **Review**: Check all answers before submitting
5. **Submit**: Confirm final submission
6. **QR Code**: Scan with phone to see your answers
7. **Leaderboard**: Check your ranking (once answers are revealed)

### Admin Flow

1. Navigate to: `http://[tablet-ip]:5000/admin`
2. Login with admin password
3. **Dashboard**: Update actual answers as events happen
4. **Leaderboard**: View real-time rankings
5. **Responses**: Detailed view of all guest answers per question

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
    "type": "number" or "time",
    "unit": "unit name (minutes, photos, etc)",
    "order": 1-10 (display order),
    "min": 0,           # Optional, for number questions
    "max": 1000,        # Optional, for number questions
    "input_hint": "0"   # Optional, placeholder text
}
```

### Colors & Styling

Edit `static/css/style.css` to customize:
- Colors (primary: `#d4a574`, secondary: `#8b6f47`)
- Button styles
- Card styling
- Responsive breakpoints

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
1. Re-spell their name in the search (e.g., "Jon" instead of "John")
2. Add them to `data/guests.csv` before event
3. Manual entry feature (coming soon)

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

### Automated Backups

Database backups are created in `data/backups/` every 15 minutes during operation.

### Manual Export

From admin dashboard, use "Export Data" to download CSV of all responses.

### Restore from Backup

Copy backup file from `data/backups/` to `data/wedding.db`:
```bash
copy data/backups/wedding_backup_[timestamp].db data/wedding.db
```

## Wedding Day Setup Checklist

### One Week Before
- [ ] Load actual 90 guests into `data/guests.csv`
- [ ] Finalize all 5-10 questions in `config.py`
- [ ] Test with 5 mock guests on your computer
- [ ] Update admin password if desired

### Day Before
- [ ] Connect tablet to power
- [ ] Test WiFi signal at venue
- [ ] Download and save this README on tablet
- [ ] Print admin password on card for groomsman

### Day Of (30 minutes before guests arrive)
- [ ] Find tablet's IP address with `ipconfig`
- [ ] Update `BASE_URL` in `config.py` with tablet IP
- [ ] Start server: Double-click `start.bat` (Windows) or `python app.py`
- [ ] Test one complete guest submission
- [ ] Place tablet on stand at entrance
- [ ] Give groomsman:
  - Admin URL: `http://[tablet-ip]:5000/admin`
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

```
wedding-game/
├── app.py                    # Main Flask application
├── database.py               # Database operations
├── config.py                 # Configuration & questions
├── requirements.txt          # Python dependencies
├── start.bat                 # Windows startup script
├── README.md                 # This file
├── data/
│   ├── wedding.db           # SQLite database (auto-created)
│   ├── guests.csv           # Guest list (edit this)
│   ├── qr_codes/            # Generated QR codes
│   └── backups/             # Database backups
├── static/
│   ├── css/style.css        # Styling
│   ├── js/guest-flow.js     # Guest interface logic
│   └── qr_codes/            # Served QR code images
└── templates/
    ├── base.html             # Base template
    ├── home.html             # Start screen
    ├── search.html           # Guest search
    ├── question.html         # Question display
    ├── summary.html          # Answer review
    ├── confirmation.html     # QR code display
    ├── guest_answers.html    # View answers (QR)
    ├── admin_login.html      # Admin login
    ├── admin_dashboard.html  # Admin interface
    ├── leaderboard.html      # Live scores
    ├── admin_responses.html  # All responses
    ├── admin_stats.html      # Event statistics
    ├── 404.html              # Page not found
    └── 500.html              # Server error
```

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

## Future Enhancements

Possible features for future versions:
- Anonymous vs named leaderboard
- Tie-breaker question
- Sound effects/animations
- Mobile app for easier submission
- Statistical analysis dashboard
- Real-time WebSocket updates
- Guest photos with submissions
- Prize wheel for winner

## Credits

Built with ❤️ for your special day!

Technologies used:
- Python Flask
- SQLite
- Bootstrap 5
- QR Code library
- Vanilla JavaScript

---

**Enjoy your wedding! 💍✨**

Questions? Check the troubleshooting section above or review the code comments in `app.py` and `database.py`.

Last updated: 2025-01-29
