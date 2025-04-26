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

def read_establishments_as_list(excel_file, search_param):
    establishments_to_second_params_map = {}

    #to handle streamlit upload (BytesIO)
    if isinstance(excel_file, BytesIO):
        df = pd.read_excel(excel_file)
    else:
        csv_file = convert_excel_to_csv(excel_file)
        df = pd.read_csv(csv_file)
    
    #find row in which establishments are all on
    establishments_label = 'Establishment Name (Source)'
    establishments_row = df[df.eq(establishments_label).any(axis=1)].index[0]

    if search_param=="address":
        second_param_label = 'Establishment Address (Source)'
        second_param_row = df[df.eq(second_param_label).any(axis=1)].index[0]
    else: 
        second_param_label = 'DUNS (Source)'
        second_param_row = df[df.eq(second_param_label).any(axis=1)].index[0]
        
    # Iterate over the columns starting from the second column (1:)
    for col in df.columns[1:]:
        establishment = df.at[establishments_row, col]
        second_param = df.at[second_param_row, col]
        print(f"debug: second_param = {second_param_row}")

        # Ensure you only map non-empty values
        if establishment and second_param:
            establishments_to_second_params_map[establishment] = second_param

    return establishments_to_second_params_map

#takes in dictionary of establishments (mapped to each extrcted second_param) returned from read_in_establishments
def create_search_links(establishments_to_second_parames_map):
    links = []
    for establishment in establishments_to_second_parames_map.keys():
        link = format_url(establishment)
        links.append(link)
    
    return links

def format_url(establishment):
    url_format = "https://dps.fda.gov/decrs/searchresult?type="
    if " " in establishment:
        search_term = establishment.replace(" ", "+") # only uses substring from 5 to 3rd from last digits of name
        entry = url_format + str(search_term)[5:-3]
    else:
        entry = url_format + str(search_term)[5:-3]
    
    return entry

def get_second_param(establishment, establishment_to_second_parames_map):
    if establishment in establishment_to_second_parames_map:
        return establishment_to_second_parames_map[establishment]
