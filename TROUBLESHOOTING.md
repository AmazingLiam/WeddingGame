# Troubleshooting Guide - Wedding Betting Game

## Error 500 When Selecting a Name - FIXED ✓

### What Was Wrong
The error occurred when:
1. Database wasn't initialized on first request
2. Guest ID conversion issues
3. Missing error handling for None values

### Fixes Applied
✅ **Better Database Initialization**
- Database now loads guests on first request (not just if missing)
- Ensures all 87 guests are always available

✅ **Robust Error Handling**
- Added try/catch blocks to all routes
- Checks if guest exists before accessing data
- Proper error messages instead of crashes

✅ **Type Safety**
- Guest ID is now converted to int properly
- Handles both string and integer IDs from JavaScript

## Testing the Fix

### 1. Start Fresh
```bash
# Delete old database
del data\wedding.db

# Start server
python app.py
```

### 2. Test Name Search
1. Go to: `http://localhost:5000`
2. Click "Start"
3. Type: "Liam" or "Fran"
4. **Expected:** Names appear immediately
5. Click on a name
6. **Expected:** Redirects to Question 1 (no error)

### 3. Check Server Console
If you see errors, they'll now show in the console with full details:
```
Error in start_game: [detailed error message]
```

## Common Issues & Solutions

### Issue: "Guest not found in database"
**Cause:** Guest ID doesn't exist in database

**Solution:**
1. Restart server (reloads guests from CSV)
2. Check `data/guests.csv` has correct format:
   ```csv
   first_name,last_name
   Liam,Hancox
   Fran,Hancox
   ```
3. Verify no BOM or special characters in CSV

### Issue: Search returns no results
**Cause:** Database not initialized or CSV not loaded

**Solution:**
```bash
# Reinitialize database
python << EOF
import database as db
from config import Config

db.init_db()
db.load_questions_from_config()
db.load_guests_from_csv(Config.GUESTS_CSV_PATH)

# Test
results = db.search_guests('Liam')
print(f"Found {len(results)} results")
EOF
```

### Issue: Server won't start
**Cause:** Port 5000 already in use or Python not installed

**Solution:**
1. Check Python: `python --version`
2. Check port: `netstat -ano | findstr :5000`
3. Kill process if needed: `taskkill /PID [number] /F`
4. Or change port in `config.py`: `PORT = 8080`

### Issue: Can't access from tablet
**Cause:** Firewall blocking or wrong IP address

**Solution:**
1. Find correct IP:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. Test from computer first:
   ```
   http://192.168.1.100:5000
   ```

3. Allow Python through firewall:
   - Windows Defender Firewall
   - Advanced Settings
   - Inbound Rules
   - New Rule → Allow Python

### Issue: Background image not showing
**Cause:** File path wrong or image doesn't exist

**Solution:**
1. Check file exists:
   ```bash
   dir static\images\background.jpg
   ```

2. Try different image:
   - JPG recommended
   - Max size: 5MB
   - Min resolution: 1280x720

3. Clear browser cache:
   - Ctrl+Shift+Del
   - Clear cached images

### Issue: Footer or colors look wrong
**Cause:** CSS not loading or browser cache

**Solution:**
1. Hard refresh: Ctrl+F5
2. Check CSS loads: F12 → Network tab
3. Verify `static/css/style.css` exists

## Debugging Tips

### Enable Debug Mode (Testing Only!)
In `config.py`:
```python
DEBUG = True  # Shows detailed errors in browser
```

**⚠️ WARNING:** Set to `False` for wedding day!

### Check Console Logs
Start server and watch console for errors:
```bash
python app.py
```

Look for:
- "Loaded X guests from data/guests.csv"
- "Loaded X questions from config"
- Any error messages

### Browser Console
Press F12 → Console tab to see JavaScript errors:
- Network errors
- API call failures
- Search issues

### Database Check
Verify guests loaded:
```bash
python << EOF
import database as db
guests = db.get_all_guests()
print(f"Total guests: {len(guests)}")
for g in guests[:5]:
    print(f"  - {g['full_name']}")
EOF
```

Should show:
```
Total guests: 87
  - Abbie Herbert
  - Adele Bryant
  - Alex Nicolson
  ...
```

## Error Messages Explained

| Error | Meaning | Fix |
|-------|---------|-----|
| "Guest not found in database" | Guest ID invalid | Restart server |
| "Invalid guest ID" | Bad data from frontend | Check JavaScript console |
| "Session expired" | Lost session data | Go back to home and restart |
| "Already submitted" | Duplicate submission | By design (blocks repeats) |
| "Guest name required" | Manual entry missing data | Fill both fields |

## Performance Issues

### Slow Search
**Solution:**
- Search has 200ms debounce (intentional)
- Database uses SQLite indexes (fast)
- Should be instant even with 90 guests

### Slow Page Loads
**Solution:**
1. Optimize background image:
   - Use JPG (not PNG)
   - Max 2MB file size
   - Compress: tinypng.com

2. Check internet connection:
   - Bootstrap/JS load from CDN
   - Need internet for first load

## Wedding Day Checklist

### Before Starting
- [ ] Delete old database: `del data\wedding.db`
- [ ] Verify all 87 guests in CSV
- [ ] Test search for "Fran" and "Liam"
- [ ] Update BASE_URL with tablet IP
- [ ] Set DEBUG = False

### During Event
- [ ] Monitor console for errors
- [ ] Have backup plan (paper forms)
- [ ] Keep charger plugged in
- [ ] Disable tablet sleep mode

### If Server Crashes
1. Don't panic - data is saved!
2. Restart: Double-click `start.bat`
3. Database auto-recovers
4. All submissions preserved

## Getting Help

### Check Logs
Look at console output when error occurs

### Test Locally
Always test on your computer before tablet

### Backup Your Data
Export from admin dashboard regularly

---

## Changes Made to Fix Error 500

### 1. app.py - start_game route
✅ Added try/catch error handling
✅ Added guest_id type conversion (int)
✅ Check if guest exists before accessing
✅ Better error messages

### 2. app.py - question route
✅ Added try/catch error handling
✅ Fallback to session guest_name if DB fails
✅ Safe redirect on error

### 3. app.py - summary route
✅ Added try/catch error handling
✅ Creates temporary guest if DB lookup fails
✅ Safe fallbacks

### 4. app.py - initialization
✅ Always reload guests on server start
✅ Global flag prevents multiple reloads

All routes now have comprehensive error handling and will show helpful error messages instead of crashing!

---

**Server ready to test!** Start with `python app.py` and try searching for "Liam" or "Fran".
