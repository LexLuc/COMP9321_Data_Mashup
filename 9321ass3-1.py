from flask import Flask
from flask import render_template
from flask_restful import reqparse
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import operator

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')




@app.route('/data', methods=['POST'])
def extract_data():

    # connect to Mongodb
    client = MongoClient("mongodb://admin:qwer1234@ds117739.mlab.com:17739/fish")
    db = client['fish']
    db.authenticate('admin', 'qwer1234')

    # obtain parameters
    parser = reqparse.RequestParser()
    parser.add_argument('year', type=str)
    parser.add_argument('region', type=str)
    args = parser.parse_args()
    year = str(args.get("year"))
    region = str(args.get("region"))

    #year = request.args.get('year')
    #collection_name = request.args.get('collect')
    export = region + '_export'
    product = region + '_production'
    collection_name = export
    print(year,export,'???')

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
    print(required_resrc.keys())
    vol_d = dict()
    vol_l = []
    for k in required_resrc:
        if k != 'year':
            vol_d[k]= required_resrc[k]['volume']
            vol_l.append(required_resrc[k]['volume'])

    vol_l.sort(reverse=True)

    rank_l = dict()
    rank_v = dict()

    for i in range(6):
        cur_v = vol_l[i]
        for k in vol_d:
            if vol_d[k] == cur_v:
                rank_l[i] = k
                rank_v[i] = cur_v

    return render_template('species.html', rank_l = rank_l, rank_v= rank_v, vol_d = vol_d)
    # return render_template('index.html'), 200

if __name__ == '__main__':
    app.run(port=22423,debug=True)
