from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_httpauth import HTTPDigestAuth
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from oauthlib.oauth2 import WebApplicationClient
import requests
import os

# Access Google credentials
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError("Google credentials are not set in the .env file.")


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError("Google credentials are not set in the .env file.")


# Flask application
app = Flask(__name__)
app.secret_key = "supersecretkey"

# HTTP Digest Authentication setup
auth = HTTPDigestAuth()
users = {
    "user1": "password1",
    "user2": "password2",
}

@auth.get_password
def get_pw(username):
    return users.get(username)

# Google OAuth 2.0 setup
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth_client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Login form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the authentication demo! Navigate to /login, /digest, or /google-login"

# Login via form
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username] == password:
            return jsonify({"message": "Login successful!", "username": username})
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    return render_template("login.html", form=form)

# HTTP Digest Authentication
@app.route("/digest")
@auth.login_required
def digest_auth():
    return jsonify({"message": f"Hello, {auth.username()}! You are authenticated."})

# Google Login
@app.route("/google-login")
def google_login():
    # Get Google's authorization endpoint
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Create the authorization URL
    request_uri = oauth_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for("google_callback", _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/google-callback")
def google_callback():
    # Get authorization code Google sent back
    code = request.args.get("code")

    # Get Google's token endpoint
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare token request
    token_url, headers, body = oauth_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=url_for("google_callback", _external=True),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    oauth_client.parse_request_body_response(token_response.text)

    # Get user info
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = oauth_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    userinfo = userinfo_response.json()
    return jsonify({"message": "Google login successful!", "userinfo": userinfo})

if __name__ == "__main__":
    app.run(debug=True)
