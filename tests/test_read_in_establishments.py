import pandas as pd
import pytest
from io import BytesIO
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from read_in_establishments import (
    convert_excel_to_csv,
    read_establishments_as_list,
    create_search_links,
    format_url,
    clean_text
)

# ---------- TEST: convert_excel_to_csv ----------

def test_convert_excel_to_csv(tmp_path):
    temp_excel = tmp_path / "test_file.xlsx"
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df.to_excel(temp_excel, index=False)

    csv_path = convert_excel_to_csv(str(temp_excel))
    assert os.path.exists(csv_path)

    df_csv = pd.read_csv(csv_path)
    pd.testing.assert_frame_equal(df, df_csv)

# ---------- TEST: read_establishments_as_list ----------

def test_read_establishments_as_list_bytesio_for_duns(mocker):
    data = {
        "A": ["", "Establishment Name (Source)", "DUNS (Source)"],
        "B": ["", "Test Company", 123456789],
        "C": ["", "Another Co", 987654321]
    }
    df = pd.DataFrame(data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)

    mocker.patch("streamlit.error")  # mock st.error

    result = read_establishments_as_list(excel_file, search_param="duns")
    assert result == [["Test Company", "123456789"], ["Another Co", "987654321"]]

def test_read_establishments_as_list_bytesio_for_address(mocker):
    data = {
        "A": ["", "Establishment Name (Source)", "Establishment Address (Source)"],
        "B": ["", "Test Company", "123 Test Ave"],
        "C": ["", "Another Co", "456 Pass St"]
    }
    df = pd.DataFrame(data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)

    mocker.patch("streamlit.error")  # mock st.error

    result = read_establishments_as_list(excel_file, search_param="address")
    assert result == [["Test Company", "123 Test Ave"], ["Another Co", "456 Pass St"]]

# ---------- TEST: create_search_links ----------

def test_create_search_links():
    data = [["Company A", "123"], ["Biz B", "456"]]
    links = create_search_links(data)
    assert links == [
        "https://dps.fda.gov/decrs/searchresult?type=Com",
        "https://dps.fda.gov/decrs/searchresult?type=Biz"
    ]

# ---------- TEST: format_url ----------

def test_format_url():
    assert format_url("ExampleCorp") == "https://dps.fda.gov/decrs/searchresult?type=Exa"

# ---------- TEST: clean_text ----------

def test_clean_text():
    raw = "Hello! This is an\nexample -- text, with $$symbols##."
    cleaned = clean_text(raw)
    assert cleaned == "hello this is an example  text with symbols"

