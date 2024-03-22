# path: bot_components/jsonify.py
import csv
import json

csvfile = open('jobs.csv', 'r')
jsonfile = open('jobs.json', 'w')

fieldnames = ("site","job_url","job_url_direct","title","company","location","job_type","date_posted","interval","min_amount","max_amount","currency","is_remote","emails","description","company_url","company_url_direct","company_addresses","company_industry","company_num_employees","company_revenue","company_description","logo_photo_url","banner_photo_url","ceo_name","ceo_photo_url")
reader = csv.DictReader(csvfile, fieldnames)

next(reader, None)  # skip the headers

out = json.dumps([row for row in reader])  # create a JSON array of jobs
jsonfile.write(out)