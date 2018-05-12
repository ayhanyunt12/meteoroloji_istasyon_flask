import datetime
import uuid
from random import randrange
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from pygeocoder import Geocoder
import pandas as pd

db = SQLAlchemy()
timeFormat = "%Y-%m-%d %H:%M"
timeFormatDay="%Y-%m-%d"

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    lang = db.Column(db.Float, nullable=False)
    latd = db.Column(db.Float, nullable=False)
    pass


class Station_data_1h(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    felt_temperature = db.Column(db.Float, nullable=False)
    windspeed = db.Column(db.Float, nullable=False)
    precipitation_probability = db.Column(db.Integer, nullable=False)
    pass


class Station_data_day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    temperature_min = db.Column(db.Float, nullable=False)
    temperature_max = db.Column(db.Float, nullable=False)
    precipitation_probability = db.Column(db.Integer, nullable=False)
    precipitation = db.Column(db.Float, nullable=False)
    windspeed_max = db.Column(db.Float, nullable=False)
    windspeed_min = db.Column(db.Float, nullable=False)
    windspeed_mean = db.Column(db.Float, nullable=False)
    relative_humidity_max = db.Column(db.Integer, nullable=False)
    relative_humidity_min = db.Column(db.Integer, nullable=False)
    relative_humidity_mean = db.Column(db.Integer, nullable=False)
    pass


def insertRandomHourlyValues(station_id):
    '''
    :param station_id: given station_id we will insert to database

    first we create a random start data
    then we iterate 168 times and create random values
    for temperature, felt_temperature etc.
    then we create a Station_data_1h object with generated values
    then we insert this object to database
    then add 1hour to startDate
    '''
    randomStartDay = randrange(1,30)
    randomStartMonth = randrange(1,13)
    randomStartHour = randrange(23)
    startDate = datetime.datetime(2018, randomStartMonth, randomStartDay, randomStartHour, 00)
    tempDate = datetime.datetime(2018, randomStartMonth, randomStartDay)
    for i in range(168):
        temperature = round(np.random.uniform(-46.4, 48.8), 2)
        felt_temperature = round(np.random.uniform(-46.4, 48.8), 2)
        wind_speed = round(np.random.uniform(0, 11), 2)
        precipitation_probability = randrange(100)
        new_station_data = Station_data_1h(
            station_id=station_id,
            time=tempDate.strftime(timeFormat),
            temperature=temperature,
            felt_temperature=felt_temperature,
            windspeed=wind_speed,
            precipitation_probability=precipitation_probability
        )
        db.session.add(new_station_data)
        db.session.commit()
        tempDate = tempDate + datetime.timedelta(minutes=60)
    insertRandomDayValues(station_id, startDate)


def insertRandomDayValues(station_id, startDate):
    '''
    :param station_id: given station_id we will insert to database
    :param startDate: given startDate from above function for using same startDate

    first we iterate 7 times and create random values
    for temperature_max, temperature_min etc.
    then we create a Station_data_day object with generated values
    then we insert this object to database
    then add 1day to startDate
    '''
    tempDate = startDate
    for i in range(7):
        temperature_max = round(np.random.uniform(-46.4, 48.8), 2)
        temperature_min = round(np.random.uniform(-46.4, 48.8), 2)
        precipitation_probability = randrange(100)
        precipitation = round(np.random.uniform(0, 10), 2)
        windspeed_max = round(np.random.uniform(0, 11), 2)
        windspeed_min = round(np.random.uniform(0, 11), 2)
        windspeed_mean = (windspeed_max + windspeed_min) / 2
        relative_humidity_max = randrange(20, 100)
        relative_humidity_min = randrange(20, 100)
        relative_humidity_mean = (relative_humidity_max + relative_humidity_min) / 2
        new_station_data = Station_data_day(
            station_id=station_id,
            time=tempDate.strftime(timeFormatDay),
            temperature_min=temperature_min,
            temperature_max=temperature_max,
            precipitation_probability=precipitation_probability,
            precipitation=precipitation,
            windspeed_max=windspeed_max,
            windspeed_min=windspeed_min,
            windspeed_mean=windspeed_mean,
            relative_humidity_max=relative_humidity_max,
            relative_humidity_min=relative_humidity_min,
            relative_humidity_mean=relative_humidity_mean
        )
        db.session.add(new_station_data)
        db.session.commit()
        tempDate = tempDate + datetime.timedelta(days=1)

def create_data_1h_json(station_data, station_data_1h):
    '''
    :param station_data: json output we will append new values to this output
    :param station_data_1h: station data hourly from database
    first we initialize the empty arrays
    after we iterate through all data that comes from database
    we append related values to related arrays
    we append related data to temp_data JSON
    we append temp_data to station_data[data_1h]
    '''
    temp_data = {}
    timeData = []
    temperatureData = []
    feltTemperatureData = []
    windSpeedData = []
    precipitationProbabilityData = []
    for one_station_data in station_data_1h:
        timeData.append(one_station_data.time)
        temperatureData.append(one_station_data.temperature)
        feltTemperatureData.append(one_station_data.felt_temperature)
        windSpeedData.append(one_station_data.windspeed)
        precipitationProbabilityData.append(one_station_data.precipitation_probability)
    temp_data['time'] = timeData
    temp_data['temperature'] = temperatureData
    temp_data['felttemperature'] = feltTemperatureData
    temp_data['windspeed'] = windSpeedData
    temp_data['precipitation_probability'] = precipitationProbabilityData
    station_data['data_1h'] = temp_data
    pass


def create_data_day_json(station_data, station_data_day):
    '''
    :param station_data: json output we will append new values to this output
    :param station_data_day: station data day from database

    first we initialize the empty arrays
    after we iterate through all data that comes from database
    we append related values to related arrays
    we append related data to temp_data JSON
    we append temp_data to station_data[data_day]
    '''
    temp_data = {}
    timeData = []
    temperatureMaxData = []
    temperatureMinData = []
    precipitationProbabilityData = []
    precipitationData = []
    windspeedMaxData = []
    windpseedMinData = []
    windspeedMeanData = []
    relativeHumidityMaxData = []
    relativeHumidityMinData = []
    relativeHumidityMeanData = []

    for one_station_data in station_data_day:
        timeData.append(one_station_data.time)
        temperatureMaxData.append(one_station_data.temperature_max)
        temperatureMinData.append(one_station_data.temperature_min)
        precipitationProbabilityData.append(one_station_data.precipitation_probability)
        precipitationData.append(one_station_data.precipitation)
        windspeedMaxData.append(one_station_data.windspeed_max)
        windpseedMinData.append(one_station_data.windspeed_min)
        windspeedMeanData.append(one_station_data.windspeed_mean)
        relativeHumidityMaxData.append(one_station_data.relative_humidity_max)
        relativeHumidityMinData.append(one_station_data.relative_humidity_min)
        relativeHumidityMeanData.append(one_station_data.relative_humidity_mean)
    temp_data['time'] = timeData
    temp_data['temperature_max'] = temperatureMaxData
    temp_data['temperature_min'] = temperatureMinData
    temp_data['precipitation_probability'] = precipitationProbabilityData
    temp_data['precipitation'] = precipitationData
    temp_data['windspeed_max'] = windspeedMaxData
    temp_data['windspeed_min'] = windpseedMinData
    temp_data['windspeed_mean'] = windspeedMeanData
    temp_data['relativehumidity_max'] = relativeHumidityMaxData
    temp_data['relativehumidity_min'] = relativeHumidityMinData
    temp_data['relativehumidity_mean'] = relativeHumidityMeanData
    station_data['data_day'] = temp_data
    pass
