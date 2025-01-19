from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_httpauth import HTTPDigestAuth
from flask_dance.contrib.google import make_google_blueprint, google
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
auth = HTTPDigestAuth()

google_bp = make_google_blueprint(client_id='YOUR_GOOGLE_CLIENT_ID',
                                  client_secret='YOUR_GOOGLE_CLIENT_SECRET',
                                  redirect_to='google_login')
app.register_blueprint(google_bp, url_prefix='/login')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return "Welcome! Choose an authentication method: /login (form), /digest (HTTP Digest), /google (Google OAuth2)"

# Form-based authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return render_template('login.html', message="Login erfolgreich!")
        else:
            message = "Falsche Login-Daten!"
    return render_template('login.html', message=message)

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Hello, {current_user.username}! You are logged in."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# HTTP Digest Authentication
users = {
    "admin": "password123"
}

@auth.get_password
def get_pw(username):
    return users.get(username)

@app.route('/digest')
@auth.login_required
def digest_auth():
    return "You are authenticated via HTTP Digest!"

# Google OAuth2 Authentication
@app.route('/google')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    user_info = resp.json()
    return f"Hello, {user_info['email']}! You are logged in via Google."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Prüfe, ob der Admin-User existiert, und erstelle ihn, falls nicht
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin", password="password123")
            db.session.add(admin_user)
            db.session.commit()
    
    app.run(debug=True)
