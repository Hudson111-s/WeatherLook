from website.utils import stream_csv_from_json, validate_input, validate_date_range, get_location_coordinates, validate_url_params
from website.api import call_api, build_api_url, build_history_api_url
from website.params import *
from flask import current_app,  Blueprint, redirect, render_template, request, flash, url_for, session, make_response, stream_with_context
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def Index():
    return render_template("index.html", description="Input a location and get historical or current weather data including: Surface Pressure, Relative Humidity, and Temperature.")

@main.route("/search", methods=["GET", "POST"])
def Search():
    if request.method == "POST":
        # Gets location and validates it.
        location = request.form.get("Location")
        err = validate_input(location, current_app.pattern, current_app.logger)
        if err:
            flash(err)
            return redirect(url_for("main.Search"))
        
        # Gets forecast and validates it, along with checkbox selections and units.
        output = validate_url_params(request.form.get("Forecast"), request.form.getlist("Checkbox[]"), request.form.getlist("Units[]"))
        forecast_is_current, url_forecast, url_forecast_length, url_weather_params, url_units, err = output
        if err:
            flash(err)
            return redirect(url_for("main.Search"))
        
        try:
            # Try to get location's latitude and longitude.
            location_coordinates, err = get_location_coordinates(location, current_app.geolocator, current_app.logger)
            if err:
                flash(err)
                return redirect(url_for("main.Search"))
            
            
            # Build API URL.
            api_url = build_api_url(location_coordinates, url_weather_params, url_units, url_forecast, url_forecast_length)

            # Make call to API.
            weather_json, err = call_api(api_url, 5, current_app.logger)
            if err:
                flash(err)
                return redirect(url_for("main.Search"))

            # This cant hold large amount of data (~4096 bytes) so I will add server-side db later.
            session["search_results"] = {
                "location": location,
                "weather_json": weather_json,
                "weather_params": url_weather_params,
                "forecast_is_current": forecast_is_current,
            }

            return redirect(url_for("main.Results"))

        except Exception as e:
            current_app.logger.exception(f"An error occurred while processing location/api: {e}")
            flash("Something went wrong, try again later!")
            return redirect(url_for("main.Search")) 
        
    return render_template("search.html", daily_params=DAILY_PARAMS, daily_readable_names=DAILY_PARAMS_READABLE, current_params=CURRENT_PARAMS, current_readable_names=CURRENT_PARAMS_READABLE)

@main.route("/download", methods=["GET"])
def Download():
    try:
        data = session.get("search_results")
        if not data:
            flash("No data available to download. Try running a search first.")
            return redirect(url_for("main.Search"))
        
        location = data.get("location")
        weather_json = data.get("weather_json")
        weather_params = data.get("weather_params")
        forecast_is_current = data.get("forecast_is_current")
        
        timestamp = datetime.today().strftime("%Y%m%d_%H%M%S")
        filename = f"WeatherLook_{location}_{timestamp}.csv"

        response = make_response(stream_with_context(stream_csv_from_json(forecast_is_current, weather_params, weather_json)))
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["Content-Type"] = "text/csv; charset=utf-8"
        return response

    except Exception as e:
        current_app.logger.exception(f"An error occurred while streaming CSV: {e}")
        flash("Something went wrong while trying to download.")
        return redirect(url_for("main.Search"))    
    
@main.route("/history", methods=["GET", "POST"])
def History():
    if request.method == "POST":
        # Gets location and validates it.
        location = request.form.get("Location")
        err = validate_input(location, current_app.pattern, current_app.logger)
        if err:
            flash(err)
            return redirect(url_for("main.History"))

        # Gets valid params.
        url_weather_params = [param for param in request.form.getlist("Checkbox[]") if param in DAILY_PARAMS] # Add other params not in current.
        if not url_weather_params:
            flash("Please select one or more checkboxes")
            return redirect(url_for("main.History"))
        
        # Get and validate dates.
        dates = (request.form.get("StartDate"), request.form.get("EndDate"))
        err = validate_date_range(dates)
        if err:
            flash(err)
            return redirect(url_for("main.History"))
        
        # Gets valid units.
        url_units = [param for param in request.form.getlist("Units[]") if param in UNITS_PARAMS]

        try:
            # Try to get location's latitude and longitude.
            location_coordinates, err = get_location_coordinates(location, current_app.geolocator, current_app.logger)
            if err:
                flash(err)
                return redirect(url_for("main.History"))
            
            # Build API URL.
            api_url = build_history_api_url(location_coordinates, url_weather_params, url_units, dates)

            # Make call to API.
            weather_json, err = call_api(api_url, 10, current_app.logger)
            if err:
                flash(err)
                return redirect(url_for("main.History"))

            session["search_results"] = {
                "location": location,
                "weather_json": weather_json,
                "weather_params": url_weather_params,
                "forecast_is_current": False,
            }

            return redirect(url_for("main.Results"))

        except Exception as e:
            current_app.logger.exception(f"An error occurred while processing location/api: {e}")
            flash("Something went wrong, try again later!")
            return redirect(url_for("main.History"))

    current_date = datetime.today().strftime("%Y-%m-%d")
    return render_template("history.html", daily_params=DAILY_PARAMS, daily_readable_names=DAILY_PARAMS_READABLE, current_date=current_date)


@main.route("/results", methods=["GET"])
def Results():
    data = session.get("search_results")
    if not data:
        flash("No results to display. Please perform a search or history query.")
        return redirect(url_for("main.Search"))

    location = data.get("location")
    weather_json = data.get("weather_json")
    weather_params = data.get("weather_params")
    forecast_is_current = data.get("forecast_is_current")

    if forecast_is_current:
        return render_template("search_results_current.html", weather_json=weather_json, weather_params=weather_params, readable_names=CURRENT_PARAMS_READABLE, location=location)
    else:
        return render_template("search_results_forecast.html", weather_json=weather_json, weather_params=weather_params, readable_names=DAILY_PARAMS_READABLE, location=location)