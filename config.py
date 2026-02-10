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
    # 15 per question, randomly selected. Mix of styles: some with name, some without
    QUESTION_QUIPS = {
        1: [  # Total Photos
            "Go on then {name}, take your best shot!",
            "This one's all about the numbers.",
            "How snap-happy will the photographer be?",
            "Every click of the shutter counts!",
            "Think big on this one, {name}!",
            "A picture's worth a thousand words...",
            "The cameras won't stop all day.",
            "Hundreds? Thousands? You tell us.",
            "Right, {name} — how many clicks?",
            "The photographer will be busy...",
            "Say cheese! But how many times?",
            "Careful with this one!",
            "Don't be shy with the numbers.",
            "The big photo question!",
            "Tricky one to start with.",
        ],
        2: [  # Ceremony Start
            "Fashionably late or right on time?",
            "Think the bride will keep everyone waiting?",
            "Place your bets on punctuality!",
            "How well do you know Fran, {name}?",
            "On time or Peak District time?",
            "The clock is ticking...",
            "Tick tock! When's the grand entrance?",
            "Trust your gut on this one.",
            "Will there be a fashionable delay?",
            "No peeking at the schedule!",
            "Time to test those psychic powers.",
            "This is anyone's guess, really.",
            "Punctuality — not everyone's strong suit!",
            "Right then, when's it kicking off?",
            "Bold predictions welcome, {name}!",
        ],
        3: [  # Speech Duration
            "How long-winded will they be?",
            "Short and sweet or a full saga?",
            "Will there be tears or just laughs?",
            "Quick toast or full TED talk?",
            "Think anyone will waffle on a bit?",
            "The best man's been rehearsing for weeks...",
            "Bring a tissue or a pillow?",
            "Speeches — brief or legendary?",
            "This one's harder than it sounds.",
            "Depends how emotional they get!",
            "Over-under on the speech length?",
            "Time to predict the waffle factor!",
            "Nervous speakers tend to rush...",
            "Let's see what you reckon, {name}.",
            "Minutes matter here!",
        ],
        4: [  # First Dance Time
            "When will they hit the dance floor?",
            "Early movers or fashionably late?",
            "Time to bust a move — but when?",
            "Before or after dessert?",
            "When does the music kick in?",
            "The big dance moment!",
            "Early evening or late night vibes?",
            "Before sunset or under the stars?",
            "When does the romance peak, {name}?",
            "The dance floor is waiting...",
            "Think the DJ's warming up yet?",
            "Everyone loves the first dance!",
            "This one depends on the speeches...",
            "Set the scene — what time?",
            "Not as obvious as you'd think!",
        ],
        5: [  # First Dance Length
            "Quick shuffle or full routine?",
            "Think they've been practising?",
            "Short and sweet or a show-stopper?",
            "Are they going for the lift?!",
            "Dirty Dancing or a gentle sway?",
            "Strictly material or a slow waltz?",
            "Seconds count here!",
            "Will it be a marathon or a sprint?",
            "Think they'll dip at the end?",
            "Short burst or the full song?",
            "How brave are the happy couple?",
            "Twinkle toes or two left feet?",
            "Interesting one this, {name}!",
            "Could go either way...",
            "Everyone will be watching!",
        ],
        6: [  # Cake Cutting Time
            "Let them eat cake! But when?",
            "When does the knife come out?",
            "Early slice or a late-night treat?",
            "Think they can resist the cake?",
            "The cake is calling!",
            "Before or after the dancing?",
            "Cake o'clock — when is it?",
            "The layers won't cut themselves!",
            "A moment of delicious anticipation!",
            "Icing on the cake — but when?",
            "Sweet predictions only, {name}.",
            "Everyone's eyeing the cake already.",
            "How long can they hold off?",
            "Time for the big slice!",
            "This is harder than choosing a flavour.",
        ],
        7: [  # Thank You Count
            "How grateful do you think they'll be?",
            "Count the thank yous!",
            "Think they'll remember everyone?",
            "Gratitude overload or short and sweet?",
            "How many shout-outs will there be?",
            "Will anyone get forgotten?",
            "Manners cost nothing!",
            "Every thank you counts here.",
            "The gratitude meter is running!",
            "Place your bets on politeness!",
            "Last question, {name} — make it count!",
            "Nearly done! One more prediction.",
            "They've got a lot of people to thank...",
            "Who's counting? You are!",
            "Depends how emotional it gets!",
        ],
    }

    # Quips for the review/summary page
    SUMMARY_QUIPS = [
        "Sure about these, {name}?",
        "Confident in your answers?",
        "Last chance to change your mind!",
        "Happy with those predictions?",
        "No pressure!",
        "Feeling brave?",
        "Lock it in!",
        "Second thoughts?",
        "Going once, going twice...",
        "Think you've nailed it?",
        "Trust your instincts!",
        "Ready to commit, {name}?",
        "Any last changes?",
        "Bold predictions there!",
        "Final answer?",
    ]
