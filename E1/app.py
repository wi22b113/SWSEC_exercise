from flask import Flask, request, render_template_string
import random
import string

app = Flask(__name__)

ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*"


def generate_password(length=8):
    return ''.join(random.choice(ALPHABET) for _ in range(length))


@app.route('/', methods=['GET'])
def index():
    # We will embed our HTML (with client-side checks) right here
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Client-Side Limit Demo</title>
        <script>
            function validateForm() {
                const numberOfPasswords = document.getElementById('number_of_passwords').value;
                // Client-side check only:
                if (parseInt(numberOfPasswords, 10) > 10) {
                  alert("Max limit is 10 passwords!");
                  return false; // block form submission
                }
                return true;
            }
        </script>
    </head>
    <body>
        <h1>Generate Passwords (Client-Side Limit Only)</h1>
        <form action="/generate" method="POST" onsubmit="return validateForm();">
            <label for="number_of_passwords">Number of Passwords (max 10):</label>
            <input type="number" id="number_of_passwords" name="number_of_passwords" value="1" min="1" max="10">
            <br><br>
            <label for="password_length">Length of Each Password:</label>
            <input type="number" id="password_length" name="password_length" value="8" min="1" max="50">
            <br><br>
            <button type="submit">Generate</button>
        </form>
        <hr>
        {% if passwords %}
            <h2>Generated Passwords:</h2>
            <ul>
            {% for p in passwords %}
                <li>{{ p }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html_code)


@app.route('/generate', methods=['POST'])
def generate():
    # Intentionally no server-side limit or validation here
    number_of_passwords = int(request.form.get('number_of_passwords', 1))
    password_length = int(request.form.get('password_length', 8))

    passwords = [
        generate_password(password_length)
        for _ in range(number_of_passwords)
    ]

    return render_template_string(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Passwords</title>
        </head>
        <body>
            <h1>Generate Passwords (Client-Side Limit Only)</h1>
            <form action="/generate" method="POST" onsubmit="return validateForm();">
                <label for="number_of_passwords">Number of Passwords (max 10):</label>
                <input type="number" id="number_of_passwords" name="number_of_passwords" value="1" min="1" max="10">
                <br><br>
                <label for="password_length">Length of Each Password:</label>
                <input type="number" id="password_length" name="password_length" value="8" min="1" max="50">
                <br><br>
                <button type="submit">Generate</button>
            </form>
            <hr>
            <h2>Generated Passwords:</h2>
            <ul>
            {% for p in passwords %}
                <li>{{ p }}</li>
            {% endfor %}
            </ul>
        </body>
        </html>
        """,
        passwords=passwords
    )


if __name__ == '__main__':
    app.run(debug=True)
