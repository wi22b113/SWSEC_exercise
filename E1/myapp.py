

from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

SPECIAL_CHARS = "!@#$%^&*"
ALPHABET = string.ascii_letters + string.digits + SPECIAL_CHARS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_passwords():
    try:
        num_passwords = int(request.form['passwordCount'])
        password_length = int(request.form['passwordLength'])

        # Generate random passwords ensuring at least one special character is included
        passwords = []
        for _ in range(num_passwords):
            base_password = ''.join(random.choices(ALPHABET, k=password_length - 1))
            special_char = random.choice(SPECIAL_CHARS)
            password = list(base_password + special_char)
            random.shuffle(password)
            passwords.append(''.join(password))

        return jsonify(passwords)

    except ValueError:
        return jsonify({"error": "Invalid input."}), 400

if __name__ == '__main__':
    app.run(debug=True)
    
    #Backend Check for password length and number of passwords
        #if num_passwords > 10:
        #    return jsonify({"error": "Maximum limit of 10 passwords exceeded."}), 400
        #if password_length < 4 or password_length > 32:
        #    return jsonify({"error": "Password length must be between 4 and 32 characters."}), 400