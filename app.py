from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import re
import random
import smtplib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@gmail.com$'
    return re.match(email_regex, email)

def is_valid_password(password):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$'
    return re.match(password_regex, password)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        session['email'] = email  # Store email in session
        return jsonify({"message": "Login successful!", "redirect": url_for('after_login')})
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    password = data['password']

    global otp
    otp = ''.join(random.choices('0123456789', k=6))
    
    if not is_valid_email(email):
        return jsonify({"message": "Invalid email format. It should be in format 'xxx@gmail.com'"}), 400
    
    if not is_valid_password(password):
        return jsonify({"message": "Invalid password format. It should contain at least one uppercase, one lowercase, one number, and one special character"}), 400

    new_user = User(firstname=firstname, lastname=lastname, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    send_otp_email(email,otp)
    session['email'] = email
                  
    return jsonify({"message": "Registration successful!", "redirect": url_for('otp')})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    otp_entered = request.form['otp']  # Retrieve OTP from form data
    
    if otp_entered == otp: 
        return jsonify({"message": "OTP verified successfully!", "redirect": url_for('after_login')})
    else:
        return jsonify({"message": "Invalid OTP"}), 401
        
def send_otp_email(email, otp):
    sender_email = "" # Your email ID
    sender_password = "" # Your Password

    message = f"""\
    Subject: OTP Verification

    Your OTP for account verification is: {otp}
    """
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=sender_email, password=sender_password)
    return connection.sendmail(from_addr=sender_email, to_addrs=email, msg = message)


@app.route('/routes', methods=['GET'])
def get_routes():
    routes = [
        {"from": "Hyderabad", "to": "Chennai", "timings": "9:00 PM - 6:00 AM", "distance": "627 km"},
        {"from": "Chennai", "to": "Hyderabad", "timings": "9:00 PM - 6:00 AM", "distance": "627 km"},
        {"from": "Hyderabad", "to": "Bangalore", "timings": "9:00 PM - 6:00 AM", "distance": "569 km"},
        {"from": "Bangalore", "to": "Hyderabad", "timings": "9:00 PM - 6:00 AM", "distance": "569 km"},
        {"from": "Hyderabad", "to": "Pune", "timings": "9:00 PM - 6:00 AM", "distance": "560 km"},
        {"from": "Pune", "to": "Hyderabad", "timings": "9:00 PM - 6:00 AM", "distance": "560 km"},
        {"from": "Hyderabad", "to": "Coimbatore", "timings": "9:00 PM - 6:00 AM", "distance": "764 km"},
        {"from": "Coimbatore", "to": "Hyderabad", "timings": "9:00 PM - 6:00 AM", "distance": "764 km"},
        {"from": "Hyderabad", "to": "Kochi", "timings": "9:00 PM - 6:00 AM", "distance": "855 km"},
        {"from": "Kochi", "to": "Hyderabad", "timings": "9:00 PM - 6:00 AM", "distance": "855 km"},
        {"from": "Hyderabad", "to": "Kannur", "timings": "9:00 PM - 9:00 AM", "distance": "882 km"},
        {"from": "Kannur", "to": "Hyderabad", "timings": "9:00 PM - 6:00 AM", "distance": "882 km"}
    ]
    return jsonify(routes)

@app.route('/book_tickets', methods=['POST'])
def book_tickets():
    from_location = request.form['from']
    to_location = request.form['to']
    date = request.form['date']
    
    # Check if the user is logged in
    user_email = session.get('email')
    if not user_email:
        return jsonify({"message": "User not logged in"}), 401

    # Get the logged-in user's email from the session
    user_email = session.get('email')  # Safely get email from session
    if user_email:
        send_ticket_email(user_email, from_location, to_location, date)
        return jsonify({"message": "Tickets booked successfully!", "from": from_location, "to": to_location, "date": date})

    

def send_ticket_email(email, from_location, to_location, date):
    sender_email = "richeprashanth@gmail.com"
    sender_password = "dohg rnkl fxbj dvqm"

    message = f"""\
    Subject: Your Ticket Booking Confirmation

    Thanks for Booking your journey with our travels. This is your ticket from {from_location} to {to_location} on {date}.
    """
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=sender_email, password=sender_password)
            connection.sendmail(from_addr=sender_email, to_addrs=email, msg=message)
            print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/otp')
def otp():
    return render_template('otp.html')

@app.route('/after')
def after_login():
    return render_template('after.html')

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'  # Set a secret key for session management
    with app.app_context():
        db.create_all()
    app.run(debug=True)

