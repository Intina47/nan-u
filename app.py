from flask import Flask, request, jsonify
import pandas as pd 
from jobspy import scrape_jobs
import subprocess
import csv
import yaml

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    with open('./config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    jobs = scrape_jobs(
        site_name= config['site_name'],
        search_term=config['search_term'],
        location=config['location'],
        results_wanted=config['results_wanted'],
        hours_old=config['hours_old'],
        country_indeed=config['country_indeed'],
    )

    jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
    subprocess.run(["python", "jsonify.py"])

    jobs = pd.read_json("jobs.json")
    return jsonify(jobs.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)