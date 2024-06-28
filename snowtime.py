import requests
import csv
import schedule
import time
from datetime import datetime, timezone

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
    print("function called")
    # Load the last run timestamp
    try:
        with open('last_run.txt', 'r') as f:
            print("last_run.txt found and opened")
            last_run = f.read()
    except FileNotFoundError:
        last_run = '1970-01-01 00:00:00'

    # Convert last run to datetime object
    last_run_dt = datetime.strptime(last_run, '%Y-%m-%d %H:%M:%S')
    print(f"last run : {last_run_dt}")
    print(f'current time: {datetime.now(timezone.utc)}')


    # Update the query parameters to fetch only new articles
    params = {
        'sysparm_query': f'sys_created_on>{last_run}',
        'sysparm_limit': 100  # Adjust as needed
    }

    # Make the API request
    response = session.get(url, headers=headers, params=params)
    # response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        print("response: 200")
        articles = response.json()['result']
        # print(articles)
        
        # Write new articles to CSV and update last run timestamp if new articles are found
        if articles:
            print("articles found")
            with open('kb_articles.csv', 'a', newline='') as csvfile:
                print("csv file opened")
                fieldnames = ['number', 'short_description', 'sys_created_on','text']
                writer = csv.DictWriter(csvfile,  fieldnames=fieldnames)
                
                # Check if the file is empty, if so, write the header
                if csvfile.tell() == 0:
                    writer.writeheader()
                    print("header added..!")

                for article in articles:
                    print("article: ")
                    writer.writerow({
                        'number': article['number'],
                        'short_description': article['short_description'],
                        'sys_created_on': article['sys_created_on'],
                        'text': article['text']
                    })
                    print(f"article {article['number']} added..!")

            # Update last run timestamp
            with open('last_run.txt', 'w') as f:
                print("upadting current date")
                f.write(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
                print("current time updated")

# Schedule the job every 5 minutes
schedule.every(1).minutes.do(fetch_new_kb_articles)

from fabricate_csv import fabricate_csv
import pandas as pd

def fetch_febricate_data(interval : int):
    schedule.every(interval).minutes.do(fetch_new_kb_articles)
    df = pd.read_csv('./kb_articles.csv')
    schedule.every(interval).minutes.do(fabricate_csv(df=df))

# Run the scheduler
while True:
    schedule.run_pending()
    # print("job done...")
    time.sleep(1)

