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

    # Quips per question — {name} will be replaced with guest's first name
    # 15 per question, randomly selected so no two guests see the same one
    QUESTION_QUIPS = {
        1: [  # Total Photos
            "Fancy yourself a sharp shooter, {name}?!",
            "How snap-happy do you think the photographer will be, {name}?",
            "Feeling lucky with the numbers, {name}?",
            "Every picture tells a story, {name}!",
            "Think big, {name} — or go home!",
            "Channel your inner photographer, {name}!",
            "How trigger-happy will the camera be, {name}?",
            "Say cheese, {name}!",
            "Cameras at the ready, {name}!",
            "Time to count the clicks, {name}!",
            "Got your calculator ready, {name}?",
            "A picture is worth a thousand words, {name}!",
            "Don't be shy with the numbers, {name}!",
            "The big photo question, {name}!",
            "Go on then {name}, take your best shot!",
        ],
        2: [  # Ceremony Start
            "Fashionably late or right on time, {name}?",
            "Think the bride will keep us waiting, {name}?",
            "Place your bets on punctuality, {name}!",
            "Will it start on time? Over to you, {name}!",
            "The clock is ticking, {name}!",
            "Any guesses on the grand entrance, {name}?",
            "On time or Peak District time, {name}?",
            "How well do you know the bride, {name}?",
            "Tick tock, {name}!",
            "Trust your gut, {name}!",
            "Will there be a fashionable delay, {name}?",
            "Set your watch, {name}!",
            "Time to test your psychic powers, {name}!",
            "Got a feeling about this one, {name}?",
            "No peeking at the schedule, {name}!",
        ],
        3: [  # Speech Duration
            "How long-winded do you reckon they'll be, {name}?",
            "Short and sweet or a full saga, {name}?",
            "Will there be tears or just laughs, {name}?",
            "Got your stopwatch ready, {name}?",
            "Think anyone will waffle on, {name}?",
            "Speechwriters or improv, {name}? You decide!",
            "Will the best man ramble, {name}?",
            "Bring a tissue or a pillow, {name}?",
            "How much talking can we handle, {name}?",
            "The speeches — brief or legendary, {name}?",
            "Quick toast or full TED talk, {name}?",
            "Have you sat through many speeches, {name}?",
            "Time to predict the waffle factor, {name}!",
            "Over-under on the speech length, {name}?",
            "Speechifying — how long will it last, {name}?",
        ],
        4: [  # First Dance Time
            "When will they hit the dance floor, {name}?",
            "Early birds or late movers, {name}?",
            "Time to bust a move — but when, {name}?",
            "Will they dance before or after dessert, {name}?",
            "When do you reckon the music kicks in, {name}?",
            "Got your dancing shoes prediction ready, {name}?",
            "The big dance moment — when is it, {name}?",
            "What time does the magic happen, {name}?",
            "Clock's ticking towards the first dance, {name}!",
            "Early evening or late night vibes, {name}?",
            "Think the DJ is warming up yet, {name}?",
            "Before sunset or under the stars, {name}?",
            "When does the romance peak, {name}?",
            "Set the scene, {name} — what time?",
            "The dance floor awaits, {name}!",
        ],
        5: [  # First Dance Length
            "Quick shuffle or full routine, {name}?",
            "Think they've been practising, {name}?",
            "Short and sweet or a show-stopper, {name}?",
            "Are they going for the lift, {name}?",
            "Dirty Dancing or a gentle sway, {name}?",
            "Strictly material or a slow waltz, {name}?",
            "How long can they keep it up, {name}?",
            "Will it be a marathon or a sprint, {name}?",
            "Seconds count here, {name}!",
            "Think they'll dip at the end, {name}?",
            "Got your timing right, {name}?",
            "Short burst or the full song, {name}?",
            "How brave are the happy couple, {name}?",
            "Will they keep us entertained, {name}?",
            "Twinkle toes or two left feet, {name}?",
        ],
        6: [  # Cake Cutting Time
            "Let them eat cake! But when, {name}?",
            "Sweet tooth activated, {name}?",
            "When does the knife come out, {name}?",
            "Early slice or a late-night treat, {name}?",
            "Think they can resist the cake long, {name}?",
            "The cake is calling, {name}!",
            "Will they cut it before the dancing, {name}?",
            "How long can you wait for cake, {name}?",
            "Time for the big slice, {name}!",
            "Cake o'clock — when is it, {name}?",
            "When do the layers get divided, {name}?",
            "Got a sweet prediction, {name}?",
            "The cake won't cut itself, {name}!",
            "A moment of delicious anticipation, {name}!",
            "Icing on the cake, {name} — but when?",
        ],
        7: [  # Thank You Count
            "How grateful do you think they'll be, {name}?",
            "Count the thank yous, {name}!",
            "Think they'll remember everyone, {name}?",
            "Gratitude overload or short and sweet, {name}?",
            "How many shout-outs will there be, {name}?",
            "Will anyone get forgotten, {name}?",
            "The thank you round-up — your guess, {name}?",
            "How appreciative are the happy couple, {name}?",
            "Think they've got a long list, {name}?",
            "Manners cost nothing — how many, {name}?",
            "Every guest counts, {name}! Or do they?",
            "The gratitude meter is running, {name}!",
            "Place your bets on politeness, {name}!",
            "Who's counting the thank yous? You are, {name}!",
            "Don't forget the thank yous, {name}!",
        ],
    }

    # Quips for the review/summary page
    SUMMARY_QUIPS = [
        "Are you sure about these, {name}?",
        "Confident in your answers, {name}?",
        "Last chance to change your mind, {name}!",
        "Happy with those predictions, {name}?",
        "No pressure, {name}!",
        "Feeling brave, {name}?",
        "Lock it in, {name}!",
        "Second thoughts, {name}?",
        "Going once, going twice, {name}!",
        "Think you've nailed it, {name}?",
        "Trust your instincts, {name}!",
        "Ready to commit, {name}?",
        "Any last changes, {name}?",
        "Bold predictions there, {name}!",
        "Final answer, {name}?",
    ]
