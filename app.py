import os
import random
import secrets
import qrcode
from io import BytesIO
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, send_from_directory

from config import Config
import database as db

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Ensure directories exist
os.makedirs(Config.QR_CODE_DIR, exist_ok=True)
os.makedirs('data', exist_ok=True)

# Template filter to format minutes as HH:MM
@app.template_filter('format_time')
def format_time_filter(minutes):
    """Convert minutes to HH:MM format for time input"""
    try:
        total_minutes = int(float(minutes))
        hours = total_minutes // 60
        mins = total_minutes % 60
        return f"{hours:02d}:{mins:02d}"
    except (ValueError, TypeError):
        return ""

# Initialize database on startup (only once)
_db_initialized = False

@app.before_request
def initialize():
    global _db_initialized
    if not _db_initialized:
        db.init_db()
        db.load_questions_from_config()
        db.load_guests_from_csv(Config.GUESTS_CSV_PATH)
        _db_initialized = True

# ============================================================================
# AUTHENTICATION DECORATOR
# ============================================================================

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# QR CODE GENERATION
# ============================================================================

def generate_guest_qr(guest_id, guest_name):
    """Generate a QR code for a guest's answers"""
    # Create unique token
    token = secrets.token_urlsafe(16)

    # Create QR code URL
    url = f"{Config.BASE_URL}/answers/{token}"

    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save to file
    filename = f"{token}.png"
    filepath = os.path.join(Config.QR_CODE_DIR, filename)
    img.save(filepath)

    qr_code_path = f"qr_codes/{filename}"

    return token, qr_code_path, url

# ============================================================================
# PWA SERVICE WORKER
# ============================================================================

@app.route('/sw.js')
def service_worker():
    """Serve service worker from root path (required for PWA scope)"""
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

# ============================================================================
# GUEST ROUTES
# ============================================================================

@app.route('/')
def home():
    """Home page with start button"""
    return render_template('home.html')

@app.route('/search')
def search():
    """Guest search page"""
    return render_template('search.html')

@app.route('/api/guests/search')
def api_guest_search():
    """API endpoint for guest search"""
    query = request.args.get('q', '').strip()

    if len(query) < 1:
        return jsonify([])

    guests = db.search_guests(query)
    return jsonify(guests)

@app.route('/start-game', methods=['POST'])
def start_game():
    """Start a game session for a guest"""
    try:
        data = request.get_json()
        guest_id = data.get('guest_id')
        guest_name = data.get('guest_name', '')

        # Convert guest_id to int if it's a string
        if guest_id is not None:
            try:
                guest_id = int(guest_id)
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid guest ID format'}), 400

        if guest_id is None:
            return jsonify({'error': 'Guest ID is required'}), 400

        # Handle manual entries (guest_id = -1)
        if guest_id != -1:
            # Check if guest has already submitted
            if db.guest_has_submitted(guest_id):
                return jsonify({'error': 'You have already submitted answers. Thank you!'}), 403

            guest = db.get_guest_by_id(guest_id)
            if not guest:
                return jsonify({'error': 'Guest not found in database'}), 404

            guest_name = guest['full_name']
        else:
            # Manual entry - no database check needed
            if not guest_name:
                return jsonify({'error': 'Guest name required'}), 400

        # Create session
        session['guest_id'] = guest_id
        session['guest_name'] = guest_name
        session['current_question'] = 0
        session['answers'] = {}
        session.modified = True  # Ensure session is saved

        return jsonify({
            'success': True,
            'guest_name': guest_name,
            'total_questions': len(db.get_questions())
        })
    except Exception as e:
        print(f"Error in start_game: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/question/<int:question_num>')
def question(question_num):
    """Display a question"""
    try:
        if 'guest_id' not in session:
            return redirect(url_for('home'))

        questions = db.get_questions()

        # Check if question number is valid
        if question_num < 0 or question_num >= len(questions):
            return redirect(url_for('summary'))

        question = questions[question_num]

        # Merge min/max values from config (not stored in database)
        config_questions = {q['order']: q for q in Config.QUESTIONS}
        if question['order_index'] in config_questions:
            config_q = config_questions[question['order_index']]
            question['min'] = config_q.get('min')
            question['max'] = config_q.get('max')

        # Handle both database guests and manual entries
        if session.get('guest_id') == -1:
            # Manual guest entry
            guest_name = session.get('guest_name', 'Guest')
        else:
            guest = db.get_guest_by_id(session['guest_id'])
            guest_name = guest['full_name'] if guest else session.get('guest_name', 'Guest')

        # Get current answer if it exists
        current_answer = session.get('answers', {}).get(str(question['id']), '')

        # Pick a random quip for this question
        first_name = guest_name.split()[0] if guest_name else 'Guest'
        quips = Config.QUESTION_QUIPS.get(question['order_index'], [])
        quip = random.choice(quips).format(name=first_name) if quips else f"Hi, {first_name}!"

        return render_template('question.html',
                             question=question,
                             question_num=question_num,
                             total_questions=len(questions),
                             guest_name=guest_name,
                             current_answer=current_answer,
                             quip=quip)
    except Exception as e:
        print(f"Error in question route: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('home'))

@app.route('/answer/<int:question_id>', methods=['POST'])
def save_answer(question_id):
    """Save an answer for a question"""
    if 'guest_id' not in session:
        return jsonify({'error': 'Session expired'}), 403

    data = request.get_json()
    answer = data.get('answer', '')

    if not answer:
        return jsonify({'error': 'Please provide an answer'}), 400

    # Store in session temporarily
    if 'answers' not in session:
        session['answers'] = {}

    session['answers'][str(question_id)] = answer
    session.modified = True

    return jsonify({'success': True})

@app.route('/summary')
def summary():
    """Summary page showing all answers"""
    try:
        if 'guest_id' not in session:
            return redirect(url_for('home'))

        guest_id = session['guest_id']
        guest_name = session.get('guest_name', 'Guest')

        # Handle both database guests and manual entries
        if guest_id == -1:
            guest = {'id': -1, 'full_name': guest_name}
        else:
            guest = db.get_guest_by_id(guest_id)
            if not guest:
                # If guest not found in DB, create a temporary one
                guest = {'id': guest_id, 'full_name': guest_name}

        questions = db.get_questions()
        answers = session.get('answers', {})

        # Build summary data
        summary_data = []
        for question in questions:
            answer = answers.get(str(question['id']), '')
            summary_data.append({
                'id': question['id'],
                'text': question['question_text'],
                'answer': answer,
                'unit': question['unit'],
                'type': question['question_type'],
                'order': question['order_index']
            })

        # Pick a random quip for the summary page
        first_name = guest_name.split()[0] if guest_name else 'Guest'
        summary_quip = random.choice(Config.SUMMARY_QUIPS).format(name=first_name)

        return render_template('summary.html',
                             guest=guest,
                             summary=summary_data,
                             summary_quip=summary_quip)
    except Exception as e:
        print(f"Error in summary route: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('home'))

@app.route('/submit-final', methods=['POST'])
def submit_final():
    """Final submission of answers"""
    if 'guest_id' not in session:
        return jsonify({'error': 'Session expired'}), 403

    guest_id = session['guest_id']
    guest_name = session.get('guest_name', 'Guest')

    # For manual entries, create a real guest record so they appear on leaderboard
    if guest_id == -1:
        try:
            # Create a guest record in the database for this manual entry
            new_guest_id = db.create_manual_guest(guest_name)

            # Save all answers to database under the new guest ID
            answers = session.get('answers', {})
            for question_id, answer in answers.items():
                db.save_response(new_guest_id, int(question_id), answer)

            # Generate QR code
            token, qr_path, qr_url = generate_guest_qr(new_guest_id, guest_name)

            # Mark as submitted
            db.mark_guest_submitted(new_guest_id, qr_path, token)

            session.clear()
            return jsonify({
                'success': True,
                'qr_code_path': qr_path,
                'qr_url': qr_url,
                'guest_name': guest_name
            })
        except Exception as e:
            print(f"Error submitting manual entry: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': 'Error saving answers'}), 500

    # Check if already submitted
    if db.guest_has_submitted(guest_id):
        return jsonify({'error': 'Already submitted'}), 403

    # Save all answers to database
    answers = session.get('answers', {})
    try:
        for question_id, answer in answers.items():
            db.save_response(guest_id, int(question_id), answer)

        # Generate QR code
        guest = db.get_guest_by_id(guest_id)
        token, qr_path, qr_url = generate_guest_qr(guest_id, guest['full_name'])

        # Mark guest as submitted
        db.mark_guest_submitted(guest_id, qr_path, token)

        # Clear session
        session.clear()

        return jsonify({
            'success': True,
            'qr_code_path': qr_path,
            'qr_url': qr_url,
            'guest_name': guest['full_name']
        })
    except Exception as e:
        print(f"Error submitting answers: {e}")
        return jsonify({'error': 'Error saving answers'}), 500

@app.route('/confirmation/<int:guest_id>')
def confirmation(guest_id):
    """Confirmation page with QR code (legacy route)"""
    guest = db.get_guest_by_id(guest_id)

    if not guest or not guest['has_submitted']:
        return redirect(url_for('home'))

    qr_code_path = guest['qr_code_path']
    first_name = guest['full_name'].split()[0] if guest['full_name'] else 'Guest'

    return render_template('confirmation.html',
                         first_name=first_name,
                         qr_code_path=qr_code_path)

@app.route('/confirmation-complete')
def confirmation_complete():
    """Confirmation page with QR code passed via URL parameters"""
    qr_code_path = request.args.get('qr', '')
    full_name = request.args.get('name', 'Guest')
    first_name = full_name.split()[0] if full_name else 'Guest'

    return render_template('confirmation.html',
                         first_name=first_name,
                         qr_code_path=qr_code_path)

@app.route('/qr-codes')
def qr_codes_menu():
    """Display list of submitted guests to view their QR codes"""
    submitted_guests = db.get_submitted_guests()
    return render_template('qr_codes.html', guests=submitted_guests)

@app.route('/api/submitted-guests')
def api_submitted_guests():
    """API endpoint to get list of submitted guests"""
    submitted_guests = db.get_submitted_guests()
    return jsonify([{
        'id': g['id'],
        'full_name': g['full_name'],
        'qr_code_path': g['qr_code_path']
    } for g in submitted_guests])

@app.route('/qr-codes/<int:guest_id>')
def qr_code_display(guest_id):
    """Display a specific guest's QR code"""
    guest = db.get_guest_by_id(guest_id)
    if not guest or not guest.get('has_submitted'):
        return redirect(url_for('qr_codes_menu'))
    return render_template('qr_code_display.html', guest=guest)

@app.route('/answers/<token>')
def view_guest_answers(token):
    """View guest's answers via QR code"""
    try:
        guest = db.get_guest_by_token(token)

        if not guest:
            return "Guest not found", 404

        responses = db.get_guest_responses(guest['id'])
        questions = db.get_questions()

        # Create a mapping of question_id to question
        questions_map = {q['id']: q for q in questions}

        # Get short labels from config since database might not have the column
        config_short_labels = {q['order']: q.get('short_label', '') for q in Config.QUESTIONS}

        # Combine responses with questions
        answers_data = []
        for response in responses:
            question = questions_map.get(response['question_id'])
            if question:
                # Get short_label from config as fallback
                short_label = config_short_labels.get(question['order_index'], '') or question['question_text']

                # Format answer based on type
                answer_val = response['answer']
                if question['question_type'] == 'time':
                    # Convert minutes back to HH:MM format
                    try:
                        total_minutes = int(float(answer_val))
                        hours = total_minutes // 60
                        minutes = total_minutes % 60
                        answer_val = f"{hours:02d}:{minutes:02d}"
                    except (ValueError, TypeError):
                        pass
                else:
                    # Remove decimal for integers
                    try:
                        answer_val = int(float(answer_val))
                    except (ValueError, TypeError):
                        pass

                answers_data.append({
                    'question': question['question_text'],
                    'short_label': short_label,
                    'answer': answer_val,
                    'unit': question['unit'],
                    'type': question['question_type'],
                    'order': question['order_index']
                })

        return render_template('guest_answers.html',
                             guest=guest,
                             answers=sorted(answers_data, key=lambda x: x['order']),
                             leaderboard_available=True)
    except Exception as e:
        print(f"Error in view_guest_answers: {e}")
        import traceback
        traceback.print_exc()
        return f"Error loading answers: {str(e)}", 500

# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    admin_url = f"{Config.BASE_URL}/admin/login"

    if request.method == 'POST':
        password = request.form.get('password', '')

        if password == Config.ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid password', admin_url=admin_url)

    return render_template('admin_login.html', admin_url=admin_url)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    questions = db.get_questions()
    submission_count = db.get_submission_count()

    return render_template('admin_dashboard.html',
                         questions=questions,
                         submission_count=submission_count)

@app.route('/admin/qr-code')
def admin_qr_code():
    """Generate QR code for admin login page (for phone access)"""
    from flask import Response
    admin_url = f"{Config.BASE_URL}/admin/login"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(admin_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/admin/update-answer', methods=['POST'])
@admin_required
def admin_update_answer():
    """Update actual answer for a question"""
    data = request.get_json()
    question_id = data.get('question_id')
    actual_answer = data.get('actual_answer')

    if not question_id:
        return jsonify({'error': 'Invalid question ID'}), 400

    db.update_actual_answer(question_id, actual_answer)

    return jsonify({
        'success': True,
        'question_id': question_id,
        'actual_answer': actual_answer
    })

@app.route('/admin/leaderboard')
@admin_required
def admin_leaderboard():
    """Leaderboard view with optional per-question filtering"""
    questions = db.get_questions()
    submission_count = db.get_submission_count()

    # Check if viewing a specific question
    question_id = request.args.get('question', type=int)
    selected_question = None

    if question_id:
        # Get per-question leaderboard
        selected_question = db.get_question_by_id(question_id)
        if selected_question and selected_question.get('actual_answer') is not None:
            leaderboard = db.get_question_leaderboard(question_id)
        else:
            leaderboard = []
    else:
        # Get overall leaderboard
        leaderboard = db.get_leaderboard()

    return render_template('leaderboard.html',
                         leaderboard=leaderboard,
                         submission_count=submission_count,
                         questions=questions,
                         selected_question=selected_question)

@app.route('/api/admin/leaderboard')
@admin_required
def api_admin_leaderboard():
    """API endpoint for leaderboard data"""
    leaderboard = db.get_leaderboard()
    submission_count = db.get_submission_count()

    return jsonify({
        'leaderboard': leaderboard,
        'submission_count': submission_count
    })

@app.route('/admin/responses')
@admin_required
def admin_responses():
    """View all responses"""
    questions = db.get_questions()
    all_responses = {}

    for question in questions:
        all_responses[question['id']] = db.get_all_responses_by_question(question['id'])

    return render_template('admin_responses.html',
                         questions=questions,
                         all_responses=all_responses)

@app.route('/admin/stats')
@admin_required
def admin_stats():
    """Admin statistics page"""
    submission_count = db.get_submission_count()
    leaderboard = db.get_leaderboard()

    return render_template('admin_stats.html',
                         submission_count=submission_count,
                         leaderboard=leaderboard)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("The Hancox Wedding Sweepstake - Server Starting")
    print("=" * 60)
    print(f"Database: {Config.DATABASE_PATH}")
    print(f"Questions: {len(Config.QUESTIONS)}")
    print(f"Admin Password: {Config.ADMIN_PASSWORD}")
    print(f"Base URL: {Config.BASE_URL}")
    print(f"Server: http://{Config.HOST}:{Config.PORT}")
    print("=" * 60)

    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
