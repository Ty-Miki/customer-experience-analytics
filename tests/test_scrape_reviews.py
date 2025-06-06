import pytest
from unittest.mock import patch, MagicMock
from scripts.scrape_reviews import GooglePlayReviewScraper

@pytest.fixture
def scraper():
    return GooglePlayReviewScraper(
        app_id="com.example.app",
        bank_name="TestBank",
        total_reviews=5,
        lang="en",
        file_name="test_reviews.csv"
    )

@patch("scripts.scrape_reviews.reviews")
def test_fetch_reviews_returns_expected_count(mock_reviews, scraper):
    # Mock the reviews function to return 2 reviews per call
    mock_reviews.side_effect = [
        ([{"reviewId": 1}, {"reviewId": 2}], "token1"),
        ([{"reviewId": 3}, {"reviewId": 4}], "token2"),
        ([{"reviewId": 5}], None)
    ]
    reviews_list = scraper.fetch_reviews()
    assert len(reviews_list) == 5
    assert all("reviewId" in r for r in reviews_list)

@patch("scripts.scrape_reviews.pd.DataFrame")
def test_save_reviews_to_csv_calls_dataframe_and_to_csv(mock_df, scraper):
    mock_instance = MagicMock()
    mock_df.return_value = mock_instance
    reviews_list = [{"reviewId": 1, "content": "Great!"}]
    scraper.save_reviews_to_csv(reviews_list)
    mock_df.assert_called_once_with(reviews_list)
    mock_instance.to_csv.assert_called_once_with("test_reviews.csv", index=False)

@patch.object(GooglePlayReviewScraper, "fetch_reviews")
@patch.object(GooglePlayReviewScraper, "save_reviews_to_csv")
def test_scrape_and_save_calls_methods(mock_save, mock_fetch, scraper):
    mock_fetch.return_value = [{"reviewId": 1}]
    scraper.scrape_and_save()
    mock_fetch.assert_called_once()
    mock_save.assert_called_once_with([{"reviewId": 1}])