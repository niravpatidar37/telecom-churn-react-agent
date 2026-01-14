# src/tools.py
from typing import Dict, Any, List
from .telecom_data import load_telecom_data

_df = load_telecom_data()


def overall_churn_rate() -> Dict[str, float]:
    """
    Compute overall churn rate across all customers.
    Returns dict with total, churned, and rate %
    """
    total = len(_df)
    churned = int(_df["churn"].sum()) if "churn" in _df.columns else 0
    rate = 100.0 * churned / total if total > 0 else 0.0

    return {
        "total_customers": int(total),
        "churned_customers": churned,
        "churn_rate_pct": rate,
    }


def churn_rate_by_column(column: str) -> List[Dict[str, Any]]:
    """
    Compute churn rate grouped by a categorical column, e.g. 'contract', 'payment_method'.

    Returns list of records with:
      - group_value
      - total_customers
      - churned_customers
      - churn_rate_pct
    """
    if column not in _df.columns:
        raise ValueError(f"Unknown column: {column}")

    if "churn" not in _df.columns:
        raise ValueError("Dataset has no 'churn' column.")

    groups = []
    grouped = _df.groupby(column)

    for val, group in grouped:
        total = len(group)
        churned = int(group["churn"].sum())
        rate = 100.0 * churned / total if total > 0 else 0.0
        groups.append(
            {
                "group_value": str(val),
                "total_customers": int(total),
                "churned_customers": churned,
                "churn_rate_pct": rate,
            }
        )
    return groups


if __name__ == "__main__":
    print("Overall churn:", overall_churn_rate())
    print("\nChurn by contract (if column exists):")
    try:
        for row in churn_rate_by_column("contract"):
            print(row)
    except Exception as e:
        print("Error:", e)
