from flask import Flask, render_template, jsonify
import pymongo
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trends']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script')
def run_script():
    data = collection.find().sort('_id', -1).limit(1)[0]
    data['_id'] = str(data['_id'])  # Convert ObjectId to string
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
