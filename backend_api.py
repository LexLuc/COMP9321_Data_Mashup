from flask import Flask, request, jsonify, render_template
from collections import defaultdict, OrderedDict
from pymongo import MongoClient

app = Flask(__name__)


SPECIES = {'Scallop', 'Squid', 'Salmonids', 'Other_fish', 'Rock lobster', 'Oyster',
           'Tuna', 'Crab', 'Abalone', 'Prawns', 'Other_Molluscs', 'Other_Curstaceans'}

def extract_fishdb():
    # connect to Mongodb
    client = MongoClient("mongodb://admin:qwer1234@ds117739.mlab.com:17739/fish")
    db = client['fish']
    db.authenticate('admin', 'qwer1234')

    return db


@app.route('/by_fish', methods=['GET'])
def data_by_fish():
    """
    Query the unit price, value and volume for each species
    E.g. /by_fish?year=2010&collect=NSW_export
    :return: Json
    """

    # connect to Mongodb
    db = extract_fishdb()

    # obtain parameters
    year = request.args.get('year')
    collection_name = request.args.get('collect')

    # check parameters
    if year is None or collection_name is None:
        return jsonify(prompt='YEAR AND COLLECTION NAME ARE REQUIRED',
                       status_code=4001,
                       data=None), 400
    if not year.isdigit():
        return jsonify(prompt='ILLEGAL YEAR',
                       status_code=4002,
                       data=None), 400
    if int(year) < 2010 or int(year) > 2015:
        return jsonify(prompt='YEAR NOT FOUND',
                       status_code=4041,
                       data=None), 404
    if collection_name not in db.collection_names(include_system_collections=False):
        return jsonify(prompt='ILLEGAL COLLECTION NAME',
                       status_code=4042,
                       data=None), 400

    # extract filtered data
    required_resrc = db[collection_name].find_one({'year': year}, {'_id': 0})

    return jsonify(prompt='OK',
                   status_code=200,
                   data=required_resrc), 200


@app.route('/line_chart_support', methods=['GET'])
def data_by_year():
    """
    Query the volume and price of certain species in a certain state by each year
    E.g. /line_chart_support?states=NSW&species=Tuna
    :return: Json
    """

    # connect to Mongodb
    db = extract_fishdb()

    # obtain parameters
    state = request.args.get('states')
    species = request.args.get('species')

    # check parameters
    if state is None or species is None:
        return jsonify(prompt='STATE AND SPECIES ARE REQUIRED',
                       status_code=4001,
                       data=None), 400

    states = set()
    items = set()
    for collection_name in db.collection_names(include_system_collections=False):
        if '_' not in collection_name:
            continue
        st, it = collection_name.split('_')
        states.add(st)
        items.add(it)

    if state not in states:
        return jsonify(prompt='STATE NOT FOUND',
                       status_code=4043,
                       data=None), 404

    price_chart = defaultdict(dict) # export unit price VS production price
    volume_chart = defaultdict(dict) # export volume VS production volume
    assert len(items) == 2 # either export or production
    for year in range(2010, 2016):
        for it in items:
            collection_name = state + '_' + it
            collection = db[collection_name].find_one({'year': str(year)}, {'_id': 0})
            if species not in collection:
                return jsonify(prompt='SPECIES NOT FOUND',
                               status_code=4044,
                               data=None), 404
            if it == 'export':
                price_chart['sale_price'][year] = collection[species]['unit_price']
                volume_chart['sale_volume'][year] = collection[species]['volume']
            else:
                price_chart['product_price'][year] = collection[species]['unit_price']
                volume_chart['product_volume'][year] = collection[species]['volume']

    price_chart_data = [list(price_chart['product_price'].values()),
                        list(price_chart['sale_price'].values())]
    volume_chart_data = [list(volume_chart['product_volume'].values()),
                         list(volume_chart['sale_volume'].values())]
    # return jsonify(prompt='OK',
    #                status_code=200,
    #                data={'sales': price_chart,
    #                      'volume': volume_chart}), 200
    return render_template("linechart.html", price=price_chart_data, volume=volume_chart_data,state=state,species=species)

@app.route('/bar_chart_support', methods=['GET'])
def data_by_state():
    """
    Query the unit price and total volume for certain species in a certain year by states
    (For ranking of unit price and total production volume data support)
    E.g. /bar_chart_support?year=2012&species=Tuna
    :return: Json
    """
    # connect to Mongodb
    db = extract_fishdb()

    # obtain parameters
    year = request.args.get('year')
    species = request.args.get('species')

    # check parameters
    if year is None or species is None:
        return jsonify(prompt='YEAR AND SPECIES ARE REQUIRED',
                       status_code=4001,
                       data=None), 400
    if not year.isdigit():
        return jsonify(prompt='ILLEGAL YEAR',
                       status_code=4002,
                       data=None), 400
    if int(year) < 2010 or int(year) > 2015:
        return jsonify(prompt='YEAR NOT FOUND',
                       status_code=4041,
                       data=None), 404

    required_resrc = defaultdict(dict)
    for collection_name in db.collection_names(include_system_collections=False):
        if '_' in collection_name:

            st = collection_name.split('_')[0]
            print(collection_name)
            year_species_entry = db[collection_name].find_one({'year': year}, {'_id': 0})[species]
            if collection_name.endswith('_production') and year_species_entry['volume']!=0:
                required_resrc['volume'][st] = year_species_entry['volume']
            elif  collection_name.endswith('_export') and year_species_entry['unit_price']!=0:
                required_resrc['unit_price'][st] = year_species_entry['unit_price']
    p_label = []
    s_label = []
    p_value = []
    s_value = []
    product_volume_ranking = list(sorted(required_resrc['volume'].items(), key=lambda x: x[1],reverse=True))
    sale_price_ranking = list(sorted(required_resrc['unit_price'].items(), key=lambda x: x[1], reverse=True))

    for item in sale_price_ranking:
        s_label.append(item[0])
        s_value.append(item[1])
    for item in product_volume_ranking:
        p_label.append(item[0])
        p_value.append(item[1])
    # return jsonify(prompt='OK',
    #                status_code=200,
    #                data=required_resrc), 200
    return render_template("barchart.html",
                           v_rank_lable=p_label,
                           v_rank_value=p_value,
                           p_rank_lable=s_label,
                           p_rank_value=s_value,
                           species=species,
                           year=year)


@app.route('/pie_chart_support', methods=['GET'])
def pie_chart_support():
    """
    Query the production volume and sales data of each species by states in a certain year
    E.g. /pie_chart_support?year=2015
    :return: Json
    """
    # connect to Mongodb
    db = extract_fishdb()

    # obtain parameters
    year = request.args.get('year')

    # check parameters
    if year is None :
        return jsonify(prompt='YEAR IS REQUIRED',
                       status_code=4001,
                       data=None), 400
    if not year.isdigit():
        return jsonify(prompt='ILLEGAL YEAR',
                       status_code=4002,
                       data=None), 400
    if int(year) < 2010 or int(year) > 2015:
        return jsonify(prompt='YEAR NOT FOUND',
                       status_code=4041,
                       data=None), 404

    sale_resrc = defaultdict(dict)
    product_resrc = defaultdict(dict)
    for collection_name in db.collection_names(include_system_collections=False):
        if '_' in collection_name:
            st, it = collection_name.split('_')
            year_species_entry = db[collection_name].find_one({'year': year}, {'_id': 0})
            for species in year_species_entry:
                if species in SPECIES:
                    if it == 'export':
                        sale_resrc[st][species] = year_species_entry[species]['volume']
                    else:
                        product_resrc[st][species] = year_species_entry[species]['volume']

    sale_list_label = [[(sp) for sp in sale_resrc[st].keys()] for st in sorted(sale_resrc.keys())]
    sale_list_value = [[(data) for data in sale_resrc[st].values()] for st in sorted(sale_resrc.keys())]
    product_list_label = [[(sp) for sp in product_resrc[st].keys()] for st in sorted(product_resrc.keys())]
    product_list_value = [[(data) for data in product_resrc[st].values()] for st in sorted(product_resrc.keys())]
    # print(sale_list_label)
    # print(sale_list_value)
    # return jsonify(prompt='OK',
    #                status_code=200,
    #                data={'sale': sale_resrc, 'production': product_resrc}), 200

    return render_template("piechart.html",
                           sale_label=sale_list_label,
                           sale_value=sale_list_value,
                           product_label=product_list_label,
                           product_value=product_list_value,
                           year=year)

@app.route('/recommendation', methods=['GET'])
def recommend():
    """
    Recommend customers which state to purchase from
    by given wanted species, volume and budget.
    E.g. /recommendation?species=Salmonids&volume=10&budget=2000
    :return: Json
    """
    # connect to Mongodb
    db = extract_fishdb()

    # obtain parameters
    species = request.args.get('species')
    volume = request.args.get('volume')
    budget = request.args.get('budget')

    # check parameters
    if species is None or volume is None or budget is None:
        return jsonify(prompt='SPECIES AND VOLUME AND BUDGET ARE REQUIRED',
                       status_code=4008,
                       data=None), 400
    if species not in SPECIES:
        return jsonify(prompt='SPECIES NOT FOUND',
                       status_code=4044,
                       data=None), 404

    required_resrc = defaultdict(dict)
    for collection_name in db.collection_names(include_system_collections=False):
        if '_' in collection_name:
            st, it = collection_name.split('_')
            species_entry = db[collection_name].find_one({'year': '2014'}, {'_id': 0})[species]
            if it == 'production' and species_entry['volume'] != 0:
                required_resrc['volume'][st] = species_entry['volume']
            elif it == 'export' and species_entry['unit_price'] != 0:
                required_resrc['unit_price'][st] = species_entry['unit_price']

    sale_price_ranking = OrderedDict(sorted(required_resrc['unit_price'].items(), key=lambda x: x[1]))
    product_volume_ranking = OrderedDict(sorted(required_resrc['volume'].items(), key=lambda x: x[1],reverse=True))

    recommend_state = []
    for st in sale_price_ranking:
        if st in product_volume_ranking:
            if product_volume_ranking[st] >= float(budget):
                return jsonify(prompt='OK',
                               status_code=200,
                               data=[st])
            recommend_state.append(st)
    return render_template('xxx.html', recommend_state=recommend_state)
    #
    # return jsonify(prompt='OK',
    #                status_code=200,
    #                data=recommend_state), 200


# for testing ---- by Yanjie
@app.route("/" , methods=['GET'])
def init():
  return render_template('index.html')

@app.route("/trend" , methods=['GET'])
def init_tr():
  return render_template('ProductionAndExport.html')

@app.route("/species" , methods=['GET'])
def init_sp():
  return render_template('species.html')

@app.route("/pies" , methods=['GET'])
def init_pi():
  return render_template('persentage.html')

if __name__ == '__main__':
    app.run(port=5050,debug=True)
