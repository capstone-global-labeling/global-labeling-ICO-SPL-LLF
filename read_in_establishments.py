import csv
import pandas as pd
from io import BytesIO

def convert_excel_to_csv(excel_file):
    user_file = str(excel_file)
    user_file_no_extension = user_file.replace(".xlsx", "")
    user_file_csv = user_file_no_extension + ".csv"

    read_file = pd.read_excel(user_file)
    read_file.to_csv(user_file_csv,
                     index=None,
                     header=True
                     )
    
    return user_file_csv
    '''
    TO DO: Consider how these intermediary files will be stored.
    
    Can set method to discard with each new query request to avoid excess overhead
    '''

def read_establishments_as_list(excel_file):
    establishments_to_addresses_map = {}

    #to handle streamlit upload (BytesIO)
    if isinstance(excel_file, BytesIO):
        df = pd.read_excel(excel_file)
    else:
        csv_file = convert_excel_to_csv(excel_file)
        df = pd.read_csv(csv_file)
    
    #find row in which establishments are all on
    establishments_label = 'Establishment Name (Source)'
    establishments_row = df[df.eq(establishments_label).any(axis=1)].index[0]

    address_label = 'Establishment Address (Source)'
    address_row = df[df.eq(address_label).any(axis=1)].index[0]

    # Iterate over the columns starting from the second column (1:)
    for col in df.columns[1:]:
        establishment = df.at[establishments_row, col]
        address = df.at[address_row, col]

        # Ensure you only map non-empty values
        if establishment and address:
            establishments_to_addresses_map[establishment] = address

    return establishments_to_addresses_map

#takes in dictionary of establishments (mapped to each extrcted address) returned from read_in_establishments
def create_search_links(establishments_to_addresses_map):
    links = []
    for establishment in establishments_to_addresses_map.keys():
        link = format_url(establishment)
        links.append(link)
    
    return links

def format_url(establishment):
    url_format = "https://dps.fda.gov/decrs/searchresult?type="
    if " " in establishment:
        search_term = establishment.replace(" ", "+") # only uses substring from 5 to 3rd from last digits of name
        entry = url_format + search_term[5:-3]
    else:
        entry = url_format + establishment
    
    return entry

def get_address(establishment, establishment_to_addresses_map):
    if establishment in establishment_to_addresses_map:
        return establishment_to_addresses_map[establishment]
