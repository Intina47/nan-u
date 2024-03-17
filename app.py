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
    
    embeds = []
    for job in jobs_json:
        embed = {
            "title": job['title'],
            "url": job['job_url'],
            "location": job['location'],
            "footer": {
                "text": job['company']
            }
        }
        embeds.append(embed)
    
    webhook_url = config['webhook_url']
    response = requests.post(webhook_url, json={"embeds": embeds})
    
    if response.status_code != 204:
        print(f"Failed to send message to Discord: {response.status_code}, {response.text}")

    return jsonify({'message': f'Scraped {len(jobs)} jobs and updated jobs.json'})

if __name__ == '__main__':
    app.run(debug=True)