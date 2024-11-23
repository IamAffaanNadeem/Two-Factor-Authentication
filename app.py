from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Use your email
app.config['MAIL_PASSWORD'] = 'your_password'  # Use your email password or app password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Store verification code
verification_code = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_code', methods=['POST'])
def send_code():
    global verification_code
    email = request.form['email']

    # Generate a 6-digit verification code
    verification_code = str(random.randint(100000, 999999))

    # Send verification code via email
    msg = Message('Your Verification Code', sender='your_email@gmail.com', recipients=[email])
    msg.body = f"Your verification code is: {verification_code}"
    try:
        mail.send(msg)
        flash('Verification code sent to your email!', 'success')
        return redirect(url_for('verify_code'))
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('home'))

@app.route('/verify_code')
def verify_code():
    return render_template('verify_code.html')

@app.route('/validate_code', methods=['POST'])
def validate_code():
    global verification_code
    entered_code = request.form['code']

    if entered_code == verification_code:
        flash('Authentication successful!', 'success')
        verification_code = None  # Reset the code
        return redirect(url_for('home'))
    else:
        flash('Invalid code. Please try again.', 'danger')
        return redirect(url_for('verify_code'))

if __name__ == '__main__':
    app.run(debug=True)
