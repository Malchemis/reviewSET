""" 
Define the arguments for the script.
"""

import argparse
import os

### ARGUMENTS ###

# Create an argument parser
def create_arg_parser():
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
    return args   