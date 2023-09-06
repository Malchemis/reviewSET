import pandas as pd
import requests
import json
import time
import sys
import os

# Import the local functions
from local.utils import obtain_string_from_list, obtain_keywords, combine_keywords
from local.arg import create_arg_parser

# Retrieve the arguments
offset, data_folder, json_folder, query, fields, limit, cap = create_arg_parser()

### FUNCTIONS ###
def send_request_and_process_response():
    """Send a request to the Semantic Scholar API and process the response."""
    # Semantic Scholar API endpoint
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&fields={fields}&offset={offset}&limit={limit}"

    # Send a GET request
    response = requests.get(url)

    # the filename
    name = query.replace('+', '_')
    
    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response to JSON
        data = response.json()['data']
        print("Retrieved", len(data), "records")
        # Save the response to a JSON file
        with open(f'{json_folder}/{name}_{offset}.json', 'w') as f:
            json.dump(data, f)
        print(f"Data saved to '{json_folder}/sound_event_detection_reviews_{offset}.json'")
        
        df = pd.DataFrame(columns=['id', 'title', 'abstract', 'keywords', 'authors', 'doi', 'url'])
        records = []
        for record in data:
            id = record['paperId']
            title = record['title']
            abstract = record['abstract']
            fieldsOfStudy = ''
            s2fieldofstudy = ''
            # switch case scenario
            if record['fieldsOfStudy'] is not None:
                fieldsOfStudy = record['fieldsOfStudy']
            if record['s2FieldsOfStudy'] is not None:
                s2fieldofstudy = obtain_keywords(record['s2FieldsOfStudy'], 'category')
            
            keywords = obtain_string_from_list(combine_keywords(fieldsOfStudy, s2fieldofstudy))
            
            authors = obtain_string_from_list(obtain_keywords(record['authors'], 'name'))
            
            url = None
            doi = None
            if record['openAccessPdf'] is not None:
                url = record['openAccessPdf']['url']
            if 'DOI' in record['externalIds']:
                doi = record['externalIds']['DOI']
        
            records.append([id, title, abstract, keywords, authors, doi, url])
            df = pd.DataFrame(records, columns=['id','title', 'abstract', 'keywords', 'authors', 'doi', 'url'])

        # Write the DataFrame to a CSV file
        df.to_csv(f'{data_folder}/{name}_{offset}.csv', index=False)

        print(f"Data saved to '{data_folder}/sound_event_detection_reviews_{offset}.csv'")
        
        return 0 if len(data) > 0 else 1
    else:
        print("Failed to retrieve data")
        for key, value in response.json().items():
            print(f"{key}: {value}")
        return -1
        
    return -2 # it should never reach this point

### MAIN ###
if __name__ == "__main__":
    while offset < cap:
        print(f"Retrieving data from offset {offset}")        
        
        res = send_request_and_process_response()
        
        # Check if the request was successful
        if res == -2:
            print("Something went wrong")
        if res == -1:
            print("Error: For more information, check the response from the API")
        if res == 0:
            offset += limit
            print("Data retrieved successfully, moving to the next offset")
        if res == 1:
            print("No more data to retrieve")
            break
            
        print("Waiting for 10 minutes due to API restrictions...")
        # Countdown timer
        for remaining in range(600, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
            sys.stdout.flush()
            time.sleep(1)
        print() # new line
    os.system("python stats.py")