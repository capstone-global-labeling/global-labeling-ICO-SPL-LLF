import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from io import BytesIO
from read_in_establishments import (
    convert_excel_to_csv,
    read_establishments_as_list,
    create_search_links,
    format_url
)

@pytest.fixture
def sample_excel_file(tmp_path):
    file_path = tmp_path / "sample.xlsx"
    df = pd.DataFrame({
        'Col1': ["Header1", "Header2"],
        'Col2': ["Establishment Name (Source)", "Establishment Address (Source)"],
        'Col3': ["Test Establishment", "123 Test St"]
    })
    df.to_excel(file_path, index=False)
    return file_path

@pytest.fixture
def sample_bytesio_excel():
    df = pd.DataFrame({
        'Col1': ["Header1", "Header2"],
        'Col2': ["Establishment Name (Source)", "Establishment Address (Source)"],
        'Col3': ["Test Establishment", "123 Test St"]
    })

    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    return excel_buffer

def test_convert_excel_to_csv(sample_excel_file):
    csv_path = convert_excel_to_csv(sample_excel_file)
    assert csv_path.endswith(".csv")
    assert os.path.exists(csv_path)

    df = pd.read_csv(csv_path)
    assert 'Col1' in df.columns
    assert 'Col2' in df.columns
    assert 'Col3' in df.columns

def test_read_establishments_as_list_file(sample_excel_file):
    result = read_establishments_as_list(sample_excel_file)
    assert isinstance(result, dict)
    assert "Test Establishment" in result
    assert result["Test Establishment"] == "123 Test St"

def test_read_establishments_as_list_bytesio(sample_bytesio_excel):
    result = read_establishments_as_list(sample_bytesio_excel)
    assert isinstance(result, dict)
    assert "Test Establishment" in result
    assert result["Test Establishment"] == "123 Test St"

def test_create_search_links():
    establishments = {"Test Establishment1": "123 Test St", "Test Establishment2": "345 Test St"}
    links = create_search_links(establishments)
    assert isinstance(links, list)
    assert all(link.startswith("https://dps.fda.gov/decrs/searchresult?type=") for link in links)

def test_format_url_with_spaces():
    url = format_url("Test Establishment Multiple Spaces")
    assert url.startswith("https://dps.fda.gov/decrs/searchresult?type=")
    assert "+" in url

def test_format_url_without_spaces():
    url = format_url("TestEstablishment")
    assert url.startswith("https://dps.fda.gov/decrs/searchresult?type=")
    assert "+" not in url