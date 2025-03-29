import streamlit as st
import pandas as pd
from read_in_establishments import read_establishments_as_list, create_search_links
from io import BytesIO

st.title("🎈 Global Labeling ICO SPL LLF Project")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
uploaded_excel_file = st.file_uploader("Upload excel file here: ", type=["xlsx"])

if uploaded_excel_file is not None:
    excel_file = BytesIO(uploaded_excel_file.getvalue())

    establishments_list = read_establishments_as_list(excel_file)
    links = create_search_links(establishments_list[1])

    st.write("Generated Links:")
    for link in links:
        st.write(link)