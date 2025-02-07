from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from scrape import *
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "defaultsecretkey") 

PASSWORD = os.getenv("PASSWORD")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_password = request.form['password']
        print(f"Entered password: {entered_password}")
        
        if entered_password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash("Incorrect password, please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/get_listings')
def get_listings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    query = request.args.get('query')
    if not query:
        return "Missing query", 400
    listings = fetch_listings(query)
    return jsonify(listings)

@app.route('/render_listing')
def render_listing():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    item_data = json.loads(request.args.get('item'))
    return render_template('listing.html', item=item_data)

if __name__ == '__main__':
    app.run(debug=True)
