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

# --- Unit tests ---
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

# --- Integration tests ---
def test_read_establishments_and_create_links(tmp_path):
    data = {
        "A": ["", "Establishment Name (Source)", "Establishment Address (Source)"],
        "B": ["", "Test Establishment", "123 Main St"],
    }
    df = pd.DataFrame(data)
    excel_file = tmp_path / "test_file.xlsx"
    df.to_excel(excel_file, index=False)

    establishment_map = read_establishments_as_list(excel_file)
    links = create_search_links(establishment_map)

    assert establishment_map == {"Test Establishment": "123 Main St"}
    assert len(links) == 1
    assert links[0].startswith("https://dps.fda.gov/decrs/searchresult?type=")

def test_read_establishments_bytesio():
    data = {
        "A": ["", "Establishment Name (Source)", "Establishment Address (Source)"],
        "B": ["", "Another Test", "456 Other St"],
    }
    df = pd.DataFrame(data)
    excel_bytes = BytesIO()
    df.to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)

    establishment_map = read_establishments_as_list(excel_bytes)

    assert establishment_map == {"Another Test": "456 Other St"}

def test_read_establishments_missing_label(tmp_path):
    data = {
        "A": ["", "Wrong Header", "Establishment Address (Source)"],
        "B": ["", "Missing Name", "789 Street"],
    }
    df = pd.DataFrame(data)
    excel_file = tmp_path / "bad_file.xlsx"
    df.to_excel(excel_file, index=False)

    with pytest.raises(IndexError):
        read_establishments_as_list(excel_file)
    
def test_convert_excel_to_csv_creates_csv(tmp_path):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    excel_file = tmp_path / "dummy.xlsx"
    df.to_excel(excel_file, index=False)

    csv_file_path = convert_excel_to_csv(excel_file)

    assert tmp_path.joinpath(csv_file_path).exists()

    csv_df = pd.read_csv(tmp_path / csv_file_path)
    assert csv_df.equals(df)