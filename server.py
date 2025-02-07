from flask import Flask, render_template, request, jsonify
from scrape import *
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Return a JSON of listings
@app.route('/get_listings')
def get_listings():
    query = request.args.get('query')
    if not query:
        return "Missing query", 400
    listings = fetch_listings(query)
    return jsonify(listings)

@app.route('/render_listing')
def render_listing():
    item_data = json.loads(request.args.get('item'))
    return render_template('listing.html', item=item_data)

if __name__ == '__main__':
    app.run(debug=True)