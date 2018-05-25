from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/by_fish', methods=['GET'])
def data_by_fish():
    """
    Query the unit price, value and volume for each fish type
    :return: Json
    """

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
    if int(year) < 2010 or int(year) > 2015:
        return jsonify(prompt='YEAR NOT FOUND'), 404
    if collection_name not in db.collection_names(include_system_collections=False):
        return jsonify(prompt='ILLEGAL COLLECTION NAME'), 400

    # extract filtered data
    required_resrc = db[collection_name].find_one({'year': year}, {'_id': 0})

    return jsonify(required_resrc), 200
    # return render_template('index.html', resrc=required_resrc), 200


@app.route('/by_year', methods=['GET'])
def data_by_year():
    """
    Query the volume and price of a certain fish in a certain state by each year
    E.g. /by_year?state=NSW&fish=Tuna
    :return: Json
    """

    # connect to Mongodb
    client = MongoClient("mongodb://admin:qwer1234@ds117739.mlab.com:17739/fish")
    db = client['fish']
    db.authenticate('admin', 'qwer1234')

    # obtain parameters
    state = request.args.get('states')
    species = request.args.get('species')

    # check parameters
    if state is None or species is None:
        return jsonify(prompt='STATE AND SPECIES ARE REQUIRED'), 400

    states = set()
    items = set()
    for collection_name in db.collection_names(include_system_collections=False):
        if '_' not in collection_name:
            continue
        st, it = collection_name.split('_')
        states.add(st)
        items.add(it)

    if state not in states:
        return jsonify(prompt='STATE NOT FOUND'), 404

    required_resrc = {}
    assert len(items) == 2 # either export or production
    for it in items:
        for year in range(2010, 2016):
            collection_name = state + '_' + it
            collection = db[collection_name].find_one({'year': str(year)}, {'_id': 0})
            if species not in collection:
                return jsonify(prompt='SPECIES NOT FOUND'), 404
            required_resrc[year] = collection[species]

    return jsonify(required_resrc), 200
    # return render_template('index.html', resrc=required_resrc), 200


if __name__ == '__main__':
    app.run()
