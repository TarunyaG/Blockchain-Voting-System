# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from blockchain import Blockchain
import json
from flask import flash
import smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


app = Flask(__name__)
app.secret_key = 'DS_project'

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['e_voting']
collection = db['votes']

# Blockchain setup
blockchain = Blockchain()

# @app.route('/')
# def index():
#     return render_template('index1.html')

# @app.route('/')
# def index():
#     return render_template('index.html')  # Load index.html

@app.route('/')
def index():
    if 'user' not in session:
        flash("Please log in to access the homepage.", "warning")
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/index1')
def index1():  # Create a route for index1.html
    if 'user' not in session:
        flash("Please log in to vote.", "warning")
        return redirect(url_for('login'))
    return render_template('index1.html')  # Load index1.html when the "Vote Now" button is clicked

@app.route('/vote1', methods=['GET', 'POST'])
def vote():
    if 'user' not in session:
        flash("Please log in to vote.", "warning")
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = request.form
        print(data)  # Debugging to check received data

        vote_data = {
            'election': data.get('election', 'Unknown Election'),
            'party': data.get('candidate', 'Unknown Party'),  # Now getting the party name correctly
        }

        # Check if a valid party was selected
        if vote_data['party'] == 'Unknown Party':
            return "Error: No candidate selected!", 400

        # Add vote to blockchain and MongoDB
        blockchain.add_block(vote_data)
        collection.insert_one(vote_data)
        return redirect(url_for('results', election=vote_data['election']))

    election = request.args.get('election', 'General Election 2025')
    return render_template('vote1.html', election=election)

@app.route('/results1/<election>')

def results(election):
    if 'user' not in session:
        flash("Please log in to vote.", "warning")
        return redirect(url_for('login'))
    votes = list(collection.find({'election': election}))
    party_votes = {}
    for vote in votes:
        party = vote['party']
        if party in party_votes:
            party_votes[party] += 1
        else:
            party_votes[party] = 1

    sorted_votes = sorted(party_votes.items(), key=lambda x: x[1], reverse=True)
    total_votes = len(votes)

    return render_template('results1.html', 
                           election=election,
                           total_votes=total_votes, 
                           sorted_votes=sorted_votes, 
                           blockchain=blockchain.chain)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/client')
def client():  # Renamed to 'client'
    return render_template('client.html')

@app.route('/contact')
def contact():  # Renamed to 'contact'
    return render_template('contact.html')

@app.route('/services')
def services():  # Renamed to 'services'
    return render_template('services.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if 'user' not in session:
        flash("Please log in to vote.", "warning")
        return redirect(url_for('login'))
    name = request.form['Name']
    phone = request.form['Phone Number']
    email = request.form['Email']
    message = request.form['Message']

    email_message = EmailMessage()
    email_message['Subject'] = 'New TrustElect Contact'
    email_message['From'] = 'pcos.sjst@gmail.com'  # your sender email
    email_message['To'] = 'pcos.sjst@gmail.com'
    email_message.set_content(f"""
    New message from your website:

    Name: {name}
    Phone: {phone}
    Email: {email}

    Message:
    {message}
    """)

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('pcos.sjst@gmail.com', 'ajya bilw zeys uefw')
            smtp.send_message(email_message)
        flash("Message sent successfully!", "success")
    except Exception as e:
        print("Error:", e)
        flash("Something went wrong. Please try again.", "danger")

    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print("🔥 Inside /signup route")  # Add this!

    if request.method == 'POST':
        print("🚀 Received POST request!")

        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        print(f"📩 Data: {name}, {username}, {email}")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('signup'))

        if db.users.find_one({'email': email}):
            flash("Email already registered.", "danger")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)

        db.users.insert_one({
            'name': name,
            'username': username,
            'email': email,
            'password': hashed_password
        })

        print("✅ User inserted!")

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("Login attempt:", email)

        user = db.users.find_one({'email': email})
        if user:
            print("User found in DB:", user['email'])
        else:
            print("User not found.")

        if user and check_password_hash(user['password'], password):
            session['user'] = email  # Store the email in the session
            flash("Login successful!", "success")
            print("Session set for:", session['user'])
            return redirect(url_for('index'))  # Redirect to index page after successful login
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('login'))  # Redirect back to login page on error

    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)


