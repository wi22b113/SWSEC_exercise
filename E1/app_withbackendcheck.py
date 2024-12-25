from flask import Flask, request, render_template
import random
import string

app = Flask(__name__)

# Predefined alphabet (for demonstration, letters + digits + some special chars)
ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*"


def generate_password(length=8):
    """Generate a single password of given length using ALPHABET."""
    return ''.join(random.choice(ALPHABET) for _ in range(length))


@app.route('/', methods=['GET'])
def index():
    """
    Render the homepage with a form that asks for number of passwords and length per password.
    """
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """
    Receives the form data: number_of_passwords and password_length.
    (In a real-world scenario, you would validate on the server side as well,
    but here we intentionally do not validate to illustrate the bypass.)
    """
    # We are intentionally *not* enforcing a server-side limit here
    number_of_passwords = int(request.form.get('number_of_passwords', 1))
    password_length = int(request.form.get('password_length', 8))

    passwords = [generate_password(password_length) for _ in range(number_of_passwords)]

    # Render the results on a simple page (or you could return JSON)
    return render_template('index.html', passwords=passwords)


if __name__ == '__main__':
    # Run in debug mode for ease of demonstration
    app.run(debug=True)
