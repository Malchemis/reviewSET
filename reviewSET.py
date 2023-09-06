import pandas as pd
import requests
import json
import time
import sys
import argparse
import os

### ARGUMENTS ###

# Create an argument parser
parser = argparse.ArgumentParser(description='Retrieve reviews from the Semantic Scholar API')
parser.add_argument('--offset', type=int, default=100, help='Initial offset')
parser.add_argument('--data_folder', type=str, default='data', help='Data folder')
parser.add_argument('--json_folder', type=str, default='jsons', help='JSON folder')
parser.add_argument('--query', type=str, default='sound+event+detection', help='Query for the Semantic Scholar API')
parser.add_argument('--fields', type=str, default='paperId,title,abstract,authors,openAccessPdf,fieldsOfStudy,s2FieldsOfStudy,externalIds', 
                    help='Fields to retrieve from the Semantic Scholar API. Format: field1,field2,field3,...')
parser.add_argument('--limit', type=int, default=100, help='Number of records to retrieve per request')
parser.add_argument('--cap', type=int, default=1000, help='Maximum number of records to retrieve')
# Parse the arguments
args = parser.parse_args()

# Check if the data folder exists, if not, create it
if not os.path.exists(args.data_folder):
    os.makedirs(args.data_folder)

# Check if the json folder exists, if not, create it
if not os.path.exists(args.json_folder):
    os.makedirs(args.json_folder)

# Use the arguments in the code
offset = args.offset
data_folder = args.data_folder
json_folder = args.json_folder
query = args.query
fields = args.fields
limit = args.limit
cap = args.cap

### FUNCTIONS ###

def obtain_string_from_list(list):
    """Obtain a string from a list of strings."""
    string = ''
    for item in list:
        string += item + ', '
    return string[:-2]    

def combine_keywords(keywords1, keywords2):
    """Combine two lists of keywords into a single list."""
    keywords = []
    for keyword in keywords1:
        if keyword not in keywords:
            keywords.append(keyword)
    for keyword in keywords2:
        if keyword not in keywords:
            keywords.append(keyword)
    return keywords

def obtain_keywords(dict_field, keyword):
    """Obtain the desired keywords (for example category) from the specified dictionary field."""
    keywords = []
    for field in dict_field:
        keywords.append(field[keyword])
    return keywords

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
        
        return 0
    else:
        print("Failed to retrieve data")
        for key, value in response.json().items():
            print(f"{key}: {value}")
        return -1
    
    if len(data) < limit:
        return 1
    
    return -2 # it should never reach this point

### MAIN ###
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