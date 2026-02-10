import sqlite3
import csv
import os
from datetime import datetime
from config import Config

# Global database connection
DB_PATH = Config.DATABASE_PATH

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with all tables"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create guests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            full_name TEXT NOT NULL,
            has_submitted BOOLEAN DEFAULT 0,
            submission_time TIMESTAMP,
            qr_code_path TEXT,
            unique_token TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            question_type TEXT NOT NULL,
            order_index INTEGER NOT NULL,
            unit TEXT,
            short_label TEXT,
            actual_answer REAL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Migration: add short_label column if missing (for existing databases)
    try:
        cursor.execute('SELECT short_label FROM questions LIMIT 1')
    except Exception:
        cursor.execute('ALTER TABLE questions ADD COLUMN short_label TEXT')

    # Create responses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (guest_id) REFERENCES guests(id),
            FOREIGN KEY (question_id) REFERENCES questions(id),
            UNIQUE(guest_id, question_id)
        )
    ''')

    # Create admin_config table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def load_guests_from_csv(csv_path):
    """Load guests from CSV file into database"""
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Please create it with first_name and last_name columns.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing guests
    cursor.execute('DELETE FROM guests')

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                first_name = row.get('first_name', '').strip()
                last_name = row.get('last_name', '').strip()
                if first_name and last_name:
                    full_name = f"{first_name} {last_name}"
                    cursor.execute('''
                        INSERT INTO guests (first_name, last_name, full_name)
                        VALUES (?, ?, ?)
                    ''', (first_name, last_name, full_name))
        conn.commit()
        print(f"Loaded guests from {csv_path}")
    except Exception as e:
        print(f"Error loading guests: {e}")
    finally:
        conn.close()

def load_questions_from_config():
    """Load questions from config into database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing questions
    cursor.execute('DELETE FROM questions')

    try:
        for q in Config.QUESTIONS:
            cursor.execute('''
                INSERT INTO questions (question_text, question_type, order_index, unit, short_label)
                VALUES (?, ?, ?, ?, ?)
            ''', (q['text'], q['type'], q['order'], q['unit'], q.get('short_label', '')))
        conn.commit()
        print(f"Loaded {len(Config.QUESTIONS)} questions from config")
    except Exception as e:
        print(f"Error loading questions: {e}")
    finally:
        conn.close()

# Guest operations
def get_guest_by_id(guest_id):
    """Get a guest by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM guests WHERE id = ?', (guest_id,))
    guest = cursor.fetchone()
    conn.close()
    return dict(guest) if guest else None

def get_guest_by_name(first_name, last_name):
    """Get a guest by first and last name"""
    conn = get_db_connection()
    cursor = conn.cursor()
    full_name = f"{first_name} {last_name}"
    cursor.execute('SELECT * FROM guests WHERE full_name = ?', (full_name,))
    guest = cursor.fetchone()
    conn.close()
    return dict(guest) if guest else None

def search_guests(query):
    """Search for guests by name (case-insensitive)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    search_term = f"%{query}%"
    cursor.execute('''
        SELECT * FROM guests
        WHERE first_name LIKE ? OR last_name LIKE ? OR full_name LIKE ?
        ORDER BY full_name
        LIMIT 20
    ''', (search_term, search_term, search_term))
    guests = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return guests

def get_all_guests():
    """Get all guests"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM guests ORDER BY full_name')
    guests = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return guests

def mark_guest_submitted(guest_id, qr_code_path, unique_token):
    """Mark a guest as submitted and store QR code info"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE guests
        SET has_submitted = 1, submission_time = ?, qr_code_path = ?, unique_token = ?
        WHERE id = ?
    ''', (datetime.now().isoformat(), qr_code_path, unique_token, guest_id))
    conn.commit()
    conn.close()

def guest_has_submitted(guest_id):
    """Check if a guest has already submitted"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT has_submitted FROM guests WHERE id = ?', (guest_id,))
    result = cursor.fetchone()
    conn.close()
    return dict(result)['has_submitted'] if result else False

def get_submitted_guests():
    """Get all guests who have submitted, ordered by first name"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM guests
        WHERE has_submitted = 1
        ORDER BY first_name, last_name
    ''')
    guests = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return guests

# Question operations
def get_questions():
    """Get all active questions ordered"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM questions
        WHERE is_active = 1
        ORDER BY order_index
    ''')
    questions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return questions

def get_question_by_id(question_id):
    """Get a question by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
    question = cursor.fetchone()
    conn.close()
    return dict(question) if question else None

def update_actual_answer(question_id, actual_answer):
    """Update the actual answer for a question (admin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Convert to float if it's a number
    try:
        actual_answer = float(actual_answer) if actual_answer else None
    except (ValueError, TypeError):
        actual_answer = None

    cursor.execute('''
        UPDATE questions
        SET actual_answer = ?
        WHERE id = ?
    ''', (actual_answer, question_id))
    conn.commit()
    conn.close()

# Response operations
def save_response(guest_id, question_id, answer):
    """Save or update a guest's response"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Handle time format (HH:MM) by converting to minutes for storage
    if isinstance(answer, str) and ':' in answer:
        try:
            hours, minutes = answer.split(':')
            answer = int(hours) * 60 + int(minutes)  # Store as total minutes
        except (ValueError, TypeError):
            conn.close()
            return False
    else:
        try:
            answer = float(answer)
        except (ValueError, TypeError):
            conn.close()
            return False

    try:
        cursor.execute('''
            INSERT OR REPLACE INTO responses (guest_id, question_id, answer)
            VALUES (?, ?, ?)
        ''', (guest_id, question_id, answer))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving response: {e}")
        conn.close()
        return False

def get_guest_responses(guest_id):
    """Get all responses for a guest"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.*, q.question_text, q.unit, q.question_type, q.order_index
        FROM responses r
        JOIN questions q ON r.question_id = q.id
        WHERE r.guest_id = ?
        ORDER BY q.order_index
    ''', (guest_id,))
    responses = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return responses

def get_all_responses_by_question(question_id):
    """Get all responses for a specific question"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.*, g.full_name
        FROM responses r
        JOIN guests g ON r.guest_id = g.id
        WHERE r.question_id = ?
        ORDER BY r.answer
    ''', (question_id,))
    responses = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return responses

def get_guest_by_token(token):
    """Get guest by their unique QR code token"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM guests WHERE unique_token = ?', (token,))
    guest = cursor.fetchone()
    conn.close()
    return dict(guest) if guest else None

# Statistics
def get_submission_count():
    """Get count of guests who have submitted"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as submitted FROM guests WHERE has_submitted = 1')
    result = cursor.fetchone()
    cursor.execute('SELECT COUNT(*) as total FROM guests')
    total = cursor.fetchone()
    conn.close()

    return {
        'submitted': dict(result)['submitted'],
        'total': dict(total)['total']
    }

def calculate_score(guest_id):
    """Calculate a guest's score (average percentage error)"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT r.answer, q.actual_answer
        FROM responses r
        JOIN questions q ON r.question_id = q.id
        WHERE r.guest_id = ? AND q.actual_answer IS NOT NULL
    ''', (guest_id,))

    responses = cursor.fetchall()
    conn.close()

    if not responses:
        return None

    total_error = 0
    for row in responses:
        guess = row[0]
        actual = row[1]

        if actual == 0:
            error = abs(guess - actual)
        else:
            error = abs(guess - actual) / actual * 100

        total_error += error

    return total_error / len(responses)

def get_leaderboard():
    """Get all submitted guests ranked by score"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, full_name, submission_time
        FROM guests
        WHERE has_submitted = 1
        ORDER BY submission_time
    ''')

    guests = [dict(row) for row in cursor.fetchall()]
    conn.close()

    leaderboard = []
    for guest in guests:
        score = calculate_score(guest['id'])
        if score is not None:
            leaderboard.append({
                'id': guest['id'],
                'name': guest['full_name'],
                'score': round(score, 2),
                'submission_time': guest['submission_time']
            })

    # Sort by score (ascending = best)
    leaderboard.sort(key=lambda x: x['score'])

    # Add rank
    for i, entry in enumerate(leaderboard):
        entry['rank'] = i + 1

    return leaderboard

def get_question_leaderboard(question_id):
    """Get leaderboard for a specific question - ranked by closest answer"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the question's actual answer
    cursor.execute('SELECT actual_answer FROM questions WHERE id = ?', (question_id,))
    question_row = cursor.fetchone()
    if not question_row or question_row['actual_answer'] is None:
        conn.close()
        return []

    actual_answer = question_row['actual_answer']

    # Get all responses for this question with guest names
    cursor.execute('''
        SELECT r.answer, g.id, g.full_name
        FROM responses r
        JOIN guests g ON r.guest_id = g.id
        WHERE r.question_id = ? AND g.has_submitted = 1
    ''', (question_id,))

    responses = cursor.fetchall()
    conn.close()

    # Calculate difference from actual answer
    leaderboard = []
    for row in responses:
        answer = row['answer']
        difference = abs(answer - actual_answer)
        leaderboard.append({
            'id': row['id'],
            'name': row['full_name'],
            'answer': answer,
            'difference': round(difference, 1) if difference != int(difference) else int(difference)
        })

    # Sort by difference (ascending = closest to actual)
    leaderboard.sort(key=lambda x: x['difference'])

    # Add rank
    for i, entry in enumerate(leaderboard):
        entry['rank'] = i + 1

    return leaderboard

# Initialization
if __name__ == '__main__':
    # This script can be run to initialize the database
    print("Initializing database...")
    init_db()
    load_questions_from_config()
    load_guests_from_csv(Config.GUESTS_CSV_PATH)
    print("Database initialized!")
