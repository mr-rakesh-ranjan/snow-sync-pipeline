import requests
import csv
import schedule
import time
from datetime import datetime

# ServiceNow instance and credentials
instance = 'dev254362'
user = 'admin'
pwd = 'Rakesh@1227'

# Endpoint for the KB table
url = f'https://{instance}.service-now.com/api/now/table/kb_knowledge'

# Headers for the request
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Authenticate
session = requests.Session()
session.auth = (user, pwd)

# Function to fetch and download new KB articles
def fetch_new_kb_articles():
    # Load the last run timestamp
    try:
        with open('last_run.txt', 'r') as f:
            last_run = f.read()
    except FileNotFoundError:
        last_run = '1970-01-01 00:00:00'

    # Convert last run to datetime object
    last_run_dt = datetime.strptime(last_run, '%Y-%m-%d %H:%M:%S')

    # Update the query parameters to fetch only new articles
    params = {
        'sysparm_query': f'sys_created_on>{last_run}',
        'sysparm_limit': 100  # Adjust as needed
    }

    # Make the API request
    response = session.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        articles = response.json()['result']
        
        # Write new articles to CSV and update last run timestamp if new articles are found
        if articles:
            with open('kb_articles.csv', 'a', newline='') as csvfile:
                fieldnames = ['number', 'short_description', 'sys_created_on','text']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                for article in articles:
                    writer.writerow({
                        'number': article['number'],
                        'short_description': article['short_description'],
                        'sys_created_on': article['sys_created_on'],
                        'text': article['text']
                    })

            # Update last run timestamp
            with open('last_run.txt', 'w') as f:
                f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Schedule the job every 5 minutes
schedule.every(1).minutes.do(fetch_new_kb_articles)

# Run the scheduler
while True:
    schedule.run_pending()
    # print("job done...")
    time.sleep(1)
