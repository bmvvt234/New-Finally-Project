from flask import Flask, render_template, jsonify
import pycountry_convert as pc
import pandas as pd

app = Flask(__name__)

# Load the data
file = pd.read_csv('gapminder_internet.csv')
countries = file['country']
internet_usage = file['internetuserate']  # Replace with actual column name if different

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route('/gapminder')
def internet_by_continent():
    grouped = {}

    for index, country in enumerate(countries):
        try:
            usage = internet_usage[index]

            # Convert country to continent
            country_code = pc.country_name_to_country_alpha2(country)
            continent_code = pc.country_alpha2_to_continent_code(country_code)
            continent_name = pc.convert_continent_code_to_continent_name(continent_code)

            # Organize into grouped[continent][country] = usage
            if continent_name not in grouped:
                grouped[continent_name] = {}
            grouped[continent_name][country] = usage

        except Exception as e:
            print(f"Error processing {country}: {e}")

    return jsonify(grouped)

if __name__ == '__main__':
    app.run(debug=True)
