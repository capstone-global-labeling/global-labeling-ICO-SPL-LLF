import pandas as pd
from io import BytesIO
import streamlit as st
import re

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

def read_establishments_as_list(excel_file, search_param):
    establishments_to_second_params_map = []

    #to handle streamlit upload (BytesIO)
    if isinstance(excel_file, BytesIO):
        df = pd.read_excel(excel_file)
    else:
        csv_file = convert_excel_to_csv(excel_file)
        df = pd.read_csv(csv_file)
    
    #find row in which establishments are all on
    establishments_label = 'Establishment Name (Source)'
    try:
        establishments_row = df[df.eq(establishments_label).any(axis=1)].index[0]
    except IndexError:
        st.error(f"❌ Could not find the header '{establishments_label}' in the file.")
        return []

    if search_param == "address":
        second_param_label = 'Establishment Address (Source)'
    else:
        second_param_label = 'DUNS (Source)'

    matching_rows = df[df.eq(second_param_label).any(axis=1)].index

    if matching_rows.empty:
        st.error(f"❌ Could not find the expected field '{second_param_label}' in the Excel sheet.\nPlease ensure the sheet contains this exact label, or double-check that the correct 'Search Parameters' option has been selected!")
    else:
        second_param_row = matching_rows[0]
            
        # Iterate over the columns starting from the second column (1:)
        for col in df.columns[1:]:
            establishment = df.at[establishments_row, col]
            second_param = df.at[second_param_row, col]
            print(f"debug: second_param = {second_param_row}")

            # Ensure you only map non-empty values and that datatype is dynamically read from excel sheet for numbers
            if isinstance(establishment,str) and ( isinstance(second_param, str) or isinstance(second_param, int) ):
                establishments_to_second_params_map.append([establishment, str(second_param)])

        print("establishments map:", establishments_to_second_params_map)
        return establishments_to_second_params_map

#takes in dictionary of establishments (mapped to each extrcted second_param) returned from read_in_establishments
def create_search_links(establishments_to_second_params_map):
    links = []
    for establishment in establishments_to_second_params_map: #format: [establishment_name, address/duns]
        link = format_url(establishment[0])
        links.append(link)
    
    return links

def format_url(establishment):
    url_format = "https://dps.fda.gov/decrs/searchresult?type="
    entry = url_format + str(establishment)[:3] #use first 3 letters of establishment
    
    return entry

#Helper function which removes all special characters(including newlines) except spaces and alphanumeric characters
def clean_text(text):
    text = text.replace('\n', ' ')
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    cleaned = cleaned.lower()
    return cleaned