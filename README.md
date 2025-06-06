# WeatherLook ⛅
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green)](https://flask.palletsprojects.com/en/latest/)
[![pip](https://img.shields.io/badge/pip-latest-orange)](https://pip.pypa.io/en/stable/)


**WeatherLook** is a web application that provides users with a more in-depth view of the weather anywhere in the world. With its interactive and dynamic front-end design using CSS, Bootstrap, Jinja, and JavaScript, and a secure and efficient Flask-powered back-end, users can input the location of any place and receive weather forecasts/data for the current time, today (the entire day), a 7-day forecast, and a 16-day forecast! **WeatherLook** also includes a forecast history page, which allows users to access past weather forecasts/data from 2020 to current in 2 month intervals (~62 days).


## 🌐 Website use

The website is **not hosted online yet**, but I plan to in the future.  
For now, it is only available for **local use**. Please follow the instructions below to run it on your own machine.


## Prerequisites

- **Python** 3.9+  
- **pip** (Python package installer)


## ⚙️ Setup and Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/Hudson111-s/WeatherLook.git
    cd WeatherLook
    ```


2. **Create a virtual environment (optional but recommended)**
    
    ```bash
    python -m venv .venv     # python3 -m venv .venv
    .venv\Scripts\activate   # source .venv/bin/activate
    ```


3. **Install dependencies**
    
    ```bash
    pip install -r requirements.txt
    ```


4. **Set environment variables**

    This application uses Flask sessions, which require a secret key.
    Create a `.env` file in the root directory and add the following:
    
    ```bash
    FLASK_KEY=<your_secret_key>
    ```

    Replace <your_secret_key> with a strong, randomly generated key.



5. **Run the app**

    Run the application using Flask:
    ```bash
    flask run
    ```


6. **Open your browser** 

    Visit `http://127.0.0.1:5000` to access the app.



## Weather and Geolocation Data Attribution

The weather data displayed and in the `.csv` files were sourced from the [Open-Meteo API](https://open-meteo.com/).

The geolocation data (latitude and longitude) used to obtain location was sourced from [OpenStreetMap](https://www.openstreetmap.org/) via the [Nominatim API](https://nominatim.org/).

Data © OpenStreetMap contributors, [OpenStreetMap](https://www.openstreetmap.org/copyright).


## Contribution

Contributions are welcome! Feel free to open issues or pull requests.


## Author

Created with ❤️ by [Hudson111-s](https://github.com/Hudson111-s)