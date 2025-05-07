import pandas as pd
import pytest
from main import process_legislators, process_bills


class TestFunctions:
    @pytest.fixture
    def df_legislators(self):
        df = pd.DataFrame(
            {
                "id": [1, 2],
                "name": ["Alice", "Bob"],
            }
        )
        df.index = pd.Index([1, 2], name="id")
        return df

    def test_process_legislators(self, df_legislators):
        df_vote_results = pd.DataFrame(
            {
                "vote_id": [101, 102, 103, 104],
                "legislator_id": [1, 1, 2, 2],
                "vote_type": [1, 2, 1, 1],
            }
        )

        result = process_legislators(df_legislators, df_vote_results)

        assert result.loc[1, "num_supported_bills"] == 1
        assert result.loc[1, "num_opposed_bills"] == 1
        assert result.loc[2, "num_supported_bills"] == 2
        assert result.loc[2, "num_opposed_bills"] == 0

    def test_process_bills(self, df_legislators):
        df_bills = pd.DataFrame(
            {
                "id": [10, 20],
                "title": ["Education Bill", "Health Bill"],
                "sponsor_id": [1, 5],
            }
        )
        df_votes = pd.DataFrame(
            {"id": [201, 202], "bill_id": [10, 20], "vote_type": [1, 2]}
        )
        df_vote_results = pd.DataFrame(
            {"vote_id": [201, 202], "legislator_id": [1, 2], "vote_type": [1, 2]}
        )

        result = process_bills(df_bills, df_votes, df_vote_results, df_legislators)

        assert result.loc[10, "title"] == "Education Bill"
        assert result.loc[10, "primary_sponsor"] == "Alice"
        assert result.loc[10, "supporter_count"] == 1
        assert result.loc[10, "opposer_count"] == 0
        assert result.loc[20, "title"] == "Health Bill"
        assert result.loc[20, "primary_sponsor"] == "Unknown"
        assert result.loc[20, "supporter_count"] == 0
        assert result.loc[20, "opposer_count"] == 1
