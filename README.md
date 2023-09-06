# Sound Event Detection Reviews

This repository is dedicated to tracking and classifying reviews for meta-analysis, with a primary focus on sound event detection reviews. The main script interacts with the Semantic Scholar API to retrieve review data.

## Project Structure

The project is organized as follows:

- `reviewSET.py`: The main script that interacts with the Semantic Scholar API to retrieve review data.
- `local/` directory: This directory contains utility scripts:
  - `arg.py`: This script is used to parse command-line arguments which include `offset`, `data_folder`, `json_folder`, `query`, `fields`, `limit`, and `cap`.
  - `requirements.sh`: This script installs pandas, request, argparse, os, json, time, and sys libraries using pip.
  - `utils.py`: This file contains utility functions used by `reviewSET.py`.

The python executable will create a `data/` directory and a `json/` directory if they do not already exist. The `data/` directory will contain the CSV files, and the `json/` directory will contain the JSON files. If `stats.py` is run, it will create a `save/` directory that contains the combined CSV files and a stat profile.

## Utility Functions

The `utils.py` file contains the following functions:

- `obtain_string_from_list`: This function takes a list of strings and joins them all into one single string.
- `combine_keywords`: This function takes two lists of keywords, combines them into a single list, and removes any duplicates.
- `obtain_keywords`: This function takes a dictionary field and a keyword and returns a list of the desired keywords from the specified field.

## reviewSET.py

The `reviewSET.py` script is a Python script that interacts with the Semantic Scholar API to retrieve review data. It starts with the defined parameters and sends remote requests to Semantic Scholar API to fetch academic paper data. The received data is processed and saved into both JSON and CSV in corresponding directories under specified filenames.

### Running the Script

The `reviewSET.py` script is run using the following command line arguments:

```bash
python reviewSET.py --offset <Starting index of API fetching> --data_folder <directory containing csv files> --json_folder <directory containing json files> --query <search keyword> --fields <fields to retrieve> --limit <maximum number of records> --cap <ending index of API fetching>
```

#### Arguments
Due to API restrictions, there is a 10-minute wait between each API request. This delay is automatically handled by the script.

The script accepts several command line arguments:

- `offset`: The offset for the API request.
- `data_folder`: The folder where the data will be saved.
- `json_folder`: The folder where the JSON files will be saved.
- `query`: The query for the API request.
- `fields`: The fields to be included in the API request.
- `limit`: The limit for the API request.

Defaults are considered if no arguments are provided. Be careful when changing the offset, as the script will not check for duplicates, and the API will not return any data if the offset is too high.
Also, changing the fields may cause the script to fail, as the script is designed to work with the default fields for now.