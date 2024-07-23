# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
base = automap.base()

# Use the Base class to reflect the database tables
base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = base.classes.measurement
Station = base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"/List all available routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"

@app.route("/api/v1.0/precipitation")

    # Calculate the date one year from the last date in data set.
    prior_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prior_year)

    session.close()

    precipitation = {date: prcp for date, prcp in precipitation}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")

def stations():
    
    # Find all stations
    all_stations = session.query(Station.station).all()
    session.close()

    # Convert all_stations to a list and jsonify
    list_stations = list(np.ravel(all_stations))
    return jsonify(stations=list_stations)

@app.route("/api/v1.0/tobs")

def tobs():

    # Calculate the date one year from the last date in data set.
    prior_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= prior_year).\
    filter(Measurement.station=='USC00519281').order_by(Measurement.date).all()

    session.close()

    # Convert temperatures to a list and jsonify
    temperatures = list(np.ravel(results))
    return jsonify(tobs=temperatures)



@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start><end>")
def metrics(start=None, end=None)

    # Return MIN, AVG, and MAX
    metrics = [func.min(Measurenments.tobs), func.avg(Measurenments.tobs),func.max(Measurenments.tobs)]

    if not end:

        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*metrics).filter(Measurement.date >= start).all()

        session.close()

        # Convert temperatures to a list and jsonify
        temperatures = list(np.ravel(results))
        return jsonify(temperatures)

    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*metrics).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Convert temperatures to a list and jsonify
    temperatures = list(np.ravel(results))
    return jsonify(tobs=temperatures)

if __name__ == '__main__':
    app.run()


