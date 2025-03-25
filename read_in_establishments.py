import csv
import pandas as pd

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
    establishments_list = []
    csv_file = convert_excel_to_csv(excel_file)
    df = pd.read_csv(csv_file)
    
    #find row in which establishments are all on
    establishments_label = 'Establishment Name (Source)'
    establishments_row = df[df.eq(establishments_label).any(axis=1)].index[0]
    for source in df.iloc[establishments_row][1:]:
        establishments_list.append(source)

    return establishments_list

#takes in list of establishments returned from read_in_establishments
def create_search_links(establishments_list):
    links = []
    for establishment in establishments_list:
        link = format_url(establishment)
        links.append(link)
    
    return links

def format_url(establishment):
    url_format = "https://dps.fda.gov/decrs/searchresult?type="
    if " " in establishment:
        search_term = establishment.replace(" ", "+")
        entry = url_format + search_term
    else:
        entry = url_format + establishment
    
    return entry