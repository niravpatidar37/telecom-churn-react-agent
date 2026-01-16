# tests/test_tools.py

from src.tools import overall_churn_rate, churn_rate_by_column


def test_overall_churn_rate_basic():
    """overall_churn_rate should return a dict with sensible keys and values."""
    result = overall_churn_rate()

    # Basic structure
    assert isinstance(result, dict)
    assert "total_customers" in result
    assert "churned_customers" in result
    assert "churn_rate_pct" in result

    # Basic sanity checks
    assert result["total_customers"] > 0
    assert result["churned_customers"] >= 0
    assert 0.0 <= result["churn_rate_pct"] <= 100.0


def test_churn_rate_by_column_contract():
    """churn_rate_by_column('contract') should return a non-empty list of group stats."""
    rows = churn_rate_by_column("contract")

    assert isinstance(rows, list)
    assert len(rows) > 0

    for row in rows:
        assert "group_value" in row
        assert "total_customers" in row
        assert "churned_customers" in row
        assert "churn_rate_pct" in row

        assert row["total_customers"] > 0
        assert row["churned_customers"] >= 0
        assert 0.0 <= row["churn_rate_pct"] <= 100.0


def test_churn_rate_by_column_invalid_column():
    """Asking for a non-existent column should raise ValueError."""
    import pytest

    with pytest.raises(ValueError):
        churn_rate_by_column("this_column_does_not_exist")
