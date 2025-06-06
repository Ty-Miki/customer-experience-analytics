import pandas as pd
from unittest.mock import patch
from scripts.load_csv import load_reviews

@patch("scripts.load_csv.os.path.exists")
def test_load_reviews_file_not_exist(mock_exists):
    mock_exists.return_value = False
    result = load_reviews("fake.csv")
    assert result is None

@patch("scripts.load_csv.os.path.exists")
@patch("scripts.load_csv.pd.read_csv")
def test_load_reviews_success(mock_read_csv, mock_exists):
    mock_exists.return_value = True
    mock_df = pd.DataFrame({"a": [1, 2]})
    mock_read_csv.return_value = mock_df
    result = load_reviews("test.csv")
    assert result.equals(mock_df)
    mock_read_csv.assert_called_once_with("test.csv", parse_dates=True)

@patch("scripts.load_csv.os.path.exists")
@patch("scripts.load_csv.pd.read_csv")
def test_load_reviews_exception(mock_read_csv, mock_exists):
    mock_exists.return_value = True
    mock_read_csv.side_effect = Exception("Read error")
    result = load_reviews("test.csv")
    assert result is None