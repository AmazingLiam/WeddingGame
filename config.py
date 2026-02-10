import os
import socket

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'wedding-game-secret-key-change-this'
    DATABASE_PATH = 'data/wedding.db'

    # Server settings
    HOST = '0.0.0.0'  # Accessible on local network
    PORT = 5000
    DEBUG = False  # Set to False for wedding day!

    # Admin settings
    ADMIN_PASSWORD = '260411F&L'  # Change this before wedding!
    SESSION_TIMEOUT = 14400  # 4 hours in seconds

    # Guest settings
    MAX_GUESTS = 100
    GUESTS_CSV_PATH = 'data/guests.csv'

    # QR Code settings
    QR_CODE_DIR = 'static/qr_codes'
    # Auto-detect local IP for QR codes so phones can access
    LOCAL_IP = get_local_ip()
    BASE_URL = f'http://{LOCAL_IP}:{PORT}'

    # Questions (5-10 questions)
    # You can modify these before the wedding
    # short_label is used on mobile for compact display
    QUESTIONS = [
        {
            "text": "How many photographs will the photographer(s) take during the entire day?",
            "short_label": "Total Photos",
            "type": "number",
            "unit": "photos",
            "order": 1,
            "min": 100,
            "max": 3000
        },
        {
            "text": "What time will the ceremony actually start?",
            "short_label": "Ceremony Start",
            "type": "time",
            "unit": "HH:MM",
            "order": 2,
            "min": "13:00",
            "max": "14:00"
        },
        {
            "text": "What is the total combined duration of all speeches in minutes?",
            "short_label": "Speech Duration",
            "type": "number",
            "unit": "minutes",
            "order": 3,
            "min": 10,
            "max": 120
        },
        {
            "text": "What time will the first dance begin?",
            "short_label": "First Dance Time",
            "type": "time",
            "unit": "HH:MM",
            "order": 4,
            "min": "18:30",
            "max": "20:30"
        },
        {
            "text": "How long will the first dance last in seconds?",
            "short_label": "First Dance Length",
            "type": "number",
            "unit": "seconds",
            "order": 5,
            "min": 60,
            "max": 600
        },
        {
            "text": "What time will the bride and groom cut the cake?",
            "short_label": "Cake Cutting Time",
            "type": "time",
            "unit": "HH:MM",
            "order": 6,
            "min": "17:00",
            "max": "21:00"
        },
        {
            "text": "How many thank you mentions will be made across all speeches?",
            "short_label": "Thank You Count",
            "type": "number",
            "unit": "mentions",
            "order": 7,
            "min": 5,
            "max": 50
        }
    ]
