import csv
import json
from jobspy import scrape_jobs
import subprocess

jobs = scrape_jobs(
    # site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
    site_name=["linkedin"],
    search_term="software engineer",
    location="Dallas, TX",
    results_wanted= 10,
    hours_old=72, # (only Linkedin/Indeed is hour specific, others round up to days old)
    country_indeed='USA'  # only needed for indeed / glassdoor
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())

jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
# run our jsonnify.py to convert our csv to json
subprocess.run(["python", "jsonify.py"])