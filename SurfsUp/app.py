import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
# REMEMBER TO CLOSE SESSIONS AFTER ROUTES
# connecting the data base
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the database
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# 1. adding routes


@app.route("/")
def main():
    return (
        f"Climate changes in Hawaii<br/>"
        f"Available Routes:<br/>"
        f"Rain fall from last year: /api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )

# creating percipitation routes for last 12 months of data


@app.route("/api/v1.0/precipitation")
def raining():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).\
    order_by(Measurement.date).all()

# 2. convert results to a dictionary with date as key and prcp as value

    result_dict = dict(results)
    session.close()

# 2. return the json representation of your dictionary
    return jsonify(result_dict)


# 3. create station route of a list of the stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station, func.count(Measurement.id)).\
        group_by(Measurement.station).order_by(
            func.count(Measurement.id).desc()).all()

# # 2. convert results to a dictionary
    stations_dict = dict(stations)
    session.close()

 #  return the json representation of your dictionary
    return jsonify(stations_dict)


# create temp route for the most active station for the prevoius year of data
@app.route("/api/v1.0/tobs")
def tobs():
    max_temp_obs = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()


# creating dictionary
    tobs_dict = dict(max_temp_obs)
    session.close()


# reeturning JSON representation of the dictionary
    return jsonify(tobs_dict)

# creating route for min max and av temps


@app.route("/api/v1.0/<start>")
def start(start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                           func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

# creating an empty list to feed in the values later.
    temp_stats = []

    for min, avg, max in result:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        temp_stats.append(tobs_dict)

    return jsonify(temp_stats)


# specific start and en date


    @app.route('/api/v1.0/<start>/<end>')
    def start_end(start, end):
        start_ending = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
                                     func.max(Measurement.tobs)).filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    session.close()

    ALL_STATS = []
    for min, avg, max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        ALL_STATS.append(tobs_dict)

    return jsonify(ALL_STATS)

    if __name__ == "__main__":
        app.run(debug=True)
