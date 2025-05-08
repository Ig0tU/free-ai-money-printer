#!/usr/bin/env python3
import os
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
from pump_fun_scraper import CryptoAnalyzer

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Add template context processor for datetime
@app.context_processor
def utility_processor():
    def get_year():
        return datetime.now().year
    return dict(get_year=get_year)


# Simple user model for demo
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# Demo user (replace with database in production)
users = {
    'admin': User(1, 'admin', generate_password_hash('admin'))
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

# Initialize the crypto analyzer
analyzer = CryptoAnalyzer()

@app.route('/')
def index():
    """Redirect to login if not authenticated, otherwise to dashboard."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Display the main dashboard."""
    # Get analysis history
    history = analyzer.ai_handler.get_analysis_history()
    return render_template('dashboard.html', history=history)

@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    """Handle token analysis requests."""
    try:
        token_data = {
            'name': request.form.get('token_name'),
            'symbol': request.form.get('token_symbol'),
            'price': request.form.get('price'),
            'market_cap': request.form.get('market_cap'),
            'volume_24h': request.form.get('volume_24h'),
            'twitter_mentions': request.form.get('twitter_mentions'),
            'telegram_members': request.form.get('telegram_members'),
            'reddit_subscribers': request.form.get('reddit_subscribers')
        }
        
        # Validate input
        if not all([token_data['name'], token_data['symbol']]):
            flash('Token name and symbol are required!', 'error')
            return redirect(url_for('dashboard'))
        
        # Perform analysis
        result = analyzer.analyze_token(token_data)
        
        flash('Analysis completed successfully!', 'success')
        return jsonify(result)
        
    except Exception as e:
        flash(f'Analysis failed: {str(e)}', 'error')
        return jsonify({'error': str(e)}), 500

@app.route('/history')
@login_required
def history():
    """Display analysis history."""
    history = analyzer.ai_handler.get_analysis_history()
    return render_template('history.html', history=history)

@app.template_filter('format_datetime')
def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    """Format datetime for templates."""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value
    return value.strftime(format)

if __name__ == '__main__':
    # Ensure the analysis_results directory exists
    os.makedirs('analysis_results', exist_ok=True)
    
    # Run the Flask application
    app.run(host='0.0.0.0', port=8000)
