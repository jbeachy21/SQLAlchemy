import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt 


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Stations = Base.classes.station


app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'start'<br/>"
        f"/api/v1.0/'start'/'end'/<br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precipitation_dict = {}
    for date, prcp in results:
        
        precipitation_dict[date] = prcp
        
    return jsonify(precipitation_dict)




@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Stations.station).all()
    session.close()
    stations = list(results)
    return jsonify(results)



@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    start = dt.datetime(2017,8,23)
    end = dt.datetime(2016,8,23)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date <= start).\
    filter(Measurement.date >= end).all()
    session.close()


    tobs_list = []
    for tobs in results:
        tobs_list.append(tobs)

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start)
    session.close()
    tobs_list = []
    for tobs in results:
        tobs_list.append(tobs)
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start, end):
    session = Session(engine)
    # start = dt.datetime(start)
    # end = dt.datetime(end)

    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date >= end)

    session.close()
    tobs_list = []
    for tobs in results:
        tobs_list.append(tobs)
    return jsonify(tobs_list)




if __name__ == '__main__':
    app.run(debug=True)
