import pandas as pd


def load_csvs(path: str) -> dict:
    """Load CSV files into a dictionary of DataFrames."""
    dfs = {
        "legislators": pd.read_csv(f"{path}/legislators.csv"),
        "bills": pd.read_csv(f"{path}/bills.csv"),
        "votes": pd.read_csv(f"{path}/votes.csv"),
        "vote_results": pd.read_csv(f"{path}/vote_results.csv"),
    }
    return dfs


def process_legislators(
    df_legislators: pd.DataFrame, df_vote_results: pd.DataFrame
) -> pd.DataFrame:
    """Process legislators DataFrame to count supported and opposed bills."""
    df = df_legislators.rename(columns={"id": "legislator_id"}).set_index(
        "legislator_id"
    )

    df["num_supported_bills"] = (
        df_vote_results[df_vote_results["vote_type"] == 1]
        .groupby("legislator_id")
        .size()
    )
    df["num_opposed_bills"] = (
        df_vote_results[df_vote_results["vote_type"] == 2]
        .groupby("legislator_id")
        .size()
    )

    df = df.fillna(0)
    df["num_supported_bills"] = df["num_supported_bills"].astype(int)
    df["num_opposed_bills"] = df["num_opposed_bills"].astype(int)
    df.index.name = "id"

    return df


def process_bills(
    df_bills: pd.DataFrame,
    df_votes: pd.DataFrame,
    df_vote_results: pd.DataFrame,
    df_legislators: pd.DataFrame,
) -> pd.DataFrame:
    """Process bills DataFrame to count supporters and opposers."""
    df_bills = df_bills.rename(
        columns={"id": "bill_id", "title": "bill_title"}
    ).set_index("bill_id")

    df = df_bills.merge(df_votes[["id", "bill_id"]], on="bill_id", how="inner").rename(
        columns={"id": "vote_id"}
    )

    df = df.merge(df_vote_results[["vote_id", "vote_type"]], on="vote_id", how="inner")
    df = df.merge(
        df_legislators[["name"]], left_on="sponsor_id", right_index=True, how="left"
    )
    df = df.rename(columns={"name": "primary_sponsor"}).fillna("Unknown")

    supported = df[df["vote_type"] == 1].groupby("bill_id").size()
    opposed = df[df["vote_type"] == 2].groupby("bill_id").size()

    df_final = (
        df[["bill_id", "bill_title", "primary_sponsor"]]
        .drop_duplicates()
        .set_index("bill_id")
    )
    df_final["supporter_count"] = supported
    df_final["opposer_count"] = opposed
    df_final = df_final.fillna(0)
    df_final = df_final.rename(columns={"bill_title": "title"})
    df_final.index.name = "id"

    return df_final


def main():
    """Main function to load data, process it, and save CSV files."""
    dfs = load_csvs("data")

    df_legislators = process_legislators(dfs["legislators"], dfs["vote_results"])
    df_legislators.to_csv("output/legislators-support-oppose-count.csv")

    df_bills = process_bills(
        dfs["bills"], dfs["votes"], dfs["vote_results"], df_legislators
    )
    df_bills.to_csv("output/bills.csv")


if __name__ == "__main__":
    main()
