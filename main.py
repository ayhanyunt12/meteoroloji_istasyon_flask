import uuid

from flask import Flask, jsonify, request
from models.Station import Station, create_data_1h_json, create_data_day_json
from models.Station import Station_data_1h
from models.Station import Station_data_day
from models.Station import db, insertRandomHourlyValues
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:asd123@localhost/station_service'
db.app = app
db.init_app(app)


'''
get all station information without data
'''
@app.route('/stations', methods=['GET'])
def get_all_stations():
    stations = Station.query.all()

    output = []
    for station in stations:
        station_data = {}
        station_data['id'] = station.id
        station_data['public_id'] = station.public_id
        station_data['name'] = station.name
        station_data['lang'] = station.lang
        station_data['latd'] = station.latd
        output.append(station_data)

    return jsonify(output)


'''
get one station information
look example.json
'''
@app.route('/station/<station_id>', methods=['GET'])
def get_station(station_id):
    # get station datas for given station_id
    station_data_1h = Station_data_1h.query.filter_by(station_id=station_id).all()
    station_data_day = Station_data_day.query.filter_by(station_id=station_id).all()

    # if station doesn't exist
    if not station_data_1h:
        return jsonify({'message': 'No station found!'})
    if not station_data_day:
        return jsonify({'message': 'No station found!'})

    # add units to json
    station_data = {'units':
        {
            'time': 'YYYY-MD-DD hh:mm',
            'temperature': 'C',
            'windspeed': 'ms-1',
            'precipitation_probability': 'percent',
            'pressure': 'hPa',
            'relativehumidity': 'percent',
            'precipitation': 'mm',
            'winddirection': 'degree',
            'predictability': 'percent'
        }
    }

    # add 1h values to json
    create_data_1h_json(station_data, station_data_1h)
    # add 1day values to json
    create_data_day_json(station_data, station_data_day)
    return jsonify(station_data)


'''
create one station
example body: {"name":"Sivas2","lang":"37.015021700000034","latd":"39.750545"}
'''
@app.route('/station', methods=['POST'])
def create_station():
    data = request.get_json()
    new_station = Station(public_id=str(uuid.uuid4()), name=data['name'], lang=data['lang'], latd=data['latd'])
    db.session.add(new_station)
    db.session.commit()
    insertRandomHourlyValues(new_station.id)

    output = []
    station_data = {}
    station_data['id'] = new_station.id
    station_data['public_id'] = new_station.public_id
    station_data['name'] = new_station.name
    station_data['lang'] = new_station.lang
    station_data['latd'] = new_station.latd
    output.append(station_data)

    return jsonify(output)


'''
update one station with id
example body: {"name":"Yeni_Sivas", public_id="bc1dbde9-dac2-4f04-9e6f-a19807275dd4"}
'''
@app.route('/station',methods=['PUT'])
def update_station():
    data = request.get_json()
    station = Station.query.filter_by(public_id = data['public_id']).first()
    station.name=data['name']
    station.lang=data['lang']
    station.latd=data['latd']
    db.session.commit()

    return jsonify({'message':'Station has updated!'})


'''
delete one station with public id
example usage: /station/19c6a052-79e8-4c41-89d2-c82bb16441c1
'''
@app.route('/station/<public_id>', methods=['DELETE'])
def delete_station(public_id):
    station = Station.query.filter_by(public_id=public_id).first()

    if not station:
        return jsonify({'message': 'No station found!'})

    db.session.delete(station)
    db.session.commit()

    return jsonify({'message': 'The station has been deleted!'})


if __name__ == '__main__':
    app.run(debug=True)
