import streamlit as st
import pandas as pd
from read_in_establishments import read_establishments_as_list, create_search_links
from io import BytesIO
import os
from datetime import datetime
from scrape_data import scrape_website

# Set the directory where the file will be saved
save_directory = "scraped_links"  # Change this to the desired folder name
os.makedirs(save_directory, exist_ok=True)  # Create folder if it does not exist

# Define the file path
file_path = os.path.join(save_directory, "generated_links.txt")

st.title("🎈 Global Labeling ICO SPL LLF Project")

search_choice = st.radio(
        "Select Search Parameters:",
        ("Establishment Name and Address", "Establishment Name and DUNS")
    )
search_param = "address" if search_choice == "Establishment Name and Address" else "duns"

uploaded_excel_file = st.file_uploader("Upload an Excel file:", type=["xlsx"])

if uploaded_excel_file is not None:
    excel_file = BytesIO(uploaded_excel_file.getvalue())

    establishments_list = read_establishments_as_list(excel_file, search_param)
    links = create_search_links(establishments_list)

    # Display generated links
    st.write("Generated Links:")
    for link in links:
        st.write(link)

    # Save links to the file automatically
    with open(file_path, "w") as f:
        for link in links:
            f.write(link + "\n")

    st.success(f"Links saved successfully in `{file_path}`")

    output_file = scrape_website(excel_file, links, establishments_list, search_param)
    st.success(f"Scraped succesfully. Download result file below.")
    output_file_name = f"{datetime.now().date()}_result_{uploaded_excel_file.name}"
        
    st.download_button(
    label="Download Result",
    data = output_file,
    file_name= output_file_name,
    icon=":material/download:"
    )