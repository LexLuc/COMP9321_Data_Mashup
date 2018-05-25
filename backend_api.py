from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/', methods=['GET'])
def extract_data():

    # connect to Mongodb
    client = MongoClient("mongodb://admin:qwer1234@ds117739.mlab.com:17739/fish")
    db = client['fish']
    db.authenticate('admin', 'qwer1234')

    # obtain parameters
    year = request.args.get('year')
    collection_name = request.args.get('collect')

    # check parameters
    if year is None or collection_name is None:
        return jsonify(prompt='YEAR AND COLLECTION NAME ARE REQUIRED'), 400
    if not year.isdigit():
        return jsonify(prompt='ILLEGAL YEAR'), 400
    if int(year) < 2013 or int(year) > 2015:
        return jsonify(prompt='YEAR NOT FOUND'), 404
    if collection_name not in db.collection_names(include_system_collections=False):
        return jsonify(prompt='ILLEGAL COLLECTION NAME'), 400

    # extract filtered data
    required_resrc = db[collection_name].find_one({'year': year}, {'_id': 0})

    # return jsonify(required_resrc), 200
    return render_template('index.html',resource=required_resrc), 200


if __name__ == '__main__':
    app.run()
