from flask import Flask, render_template, request, jsonify
from scrape import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Return a JSON of listings
@app.route('/get_listings')
def get_listings():
    search_query = request.args.get('search_query')
    if not search_query:
        return "No search query provided", 400
    listings = fetch_listings(search_query)
    return jsonify(listings)

if __name__ == '__main__':
    app.run(debug=True)