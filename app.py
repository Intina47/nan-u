from flask import Flask, jsonify
import requests
import pandas as pd 
from jobspy import scrape_jobs
import subprocess
import csv
import yaml
import json

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

    # jobs = pd.read_json("jobs.json")
    with open('jobs.json', 'r') as f:
        jobs_json = json.load(f)
    
    message = f"Found {len(jobs_json)} new jobs:\n\n"
    for job in jobs_json:
        message += f"{job['title']} at {job['company']} in {job['location']}\n\n"
    
    webhook_url = config['webhook_url']
    requests.post(webhook_url, json={"text": message})
    print(f"webhook url:", webhook_url)

    return jsonify({'message': f'Scraped {len(jobs)} jobs and updated jobs.json'})

if __name__ == '__main__':
    app.run(debug=True)