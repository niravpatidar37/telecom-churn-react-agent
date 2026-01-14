# src/telecom_data.py
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "telecom_users.csv"

_df_cache = None


def load_telecom_data() -> pd.DataFrame:
    """
    Load the telecom dataset from CSV and perform basic cleaning.
    Uses a simple in-memory cache so we don't reload on every call.
    """
    global _df_cache
    if _df_cache is not None:
        return _df_cache

    df = pd.read_csv(DATA_PATH)

    # Normalize column names: lowercase, underscores
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Try to normalize churn column to boolean if present
    if "churn" in df.columns:
        df["churn"] = (
            df["churn"]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["yes", "1", "true"])
        )

    _df_cache = df
    return df


if __name__ == "__main__":
    df = load_telecom_data()
    print(df.head())
    print("\nColumns:", df.columns.tolist())
