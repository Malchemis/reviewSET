## Project Overview

This repository is designed to facilitate the tracking and classification of reviews for meta-analysis. The primary focus (see defaults parameter) is on sound event detection reviews.

## reviewSET.py

The `reviewSET.py` script is a Python script that interacts with the Semantic Scholar API to retrieve review data.

### Dependencies

The script requires several Python libraries, including:

- pandas
- requests
- json
- argparse

(you can run the requirements.sh script to install these libraries)

Ensure these libraries are installed before running the script.

### Functions

The script includes several functions:

- `obtain_string_from_list`: Transforms a list of strings into a single string.
- `combine_keywords`: Combines multiple keyword arguments into a single string.
- `obtain_keywords`: Retrieves the keywords for the API request.
- `send_request_and_process_response`: Sends a request to the Semantic Scholar API, processes the response, and saves the data.

### Execution

The script runs a loop that sends a request to the Semantic Scholar API every 10 minutes. The response is processed and the data is saved. To run the script, use the command `python reviewSET.py`.

### Arguments

The script accepts several command line arguments:

- `offset`: The offset for the API request.
- `data_folder`: The folder where the data will be saved.
- `json_folder`: The folder where the JSON files will be saved.
- `query`: The query for the API request.
- `fields`: The fields to be included in the API request.
- `limit`: The limit for the API request.

Defaults are considered if no arguments are provided. Be careful when changing the offset, as the script will not check for duplicates, and the API will not return any data if the offset is too high.
Also, changing the fields may cause the script to fail, as the script is designed to work with the default fields for now.
