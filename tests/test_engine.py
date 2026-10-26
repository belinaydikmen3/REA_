"""Unit tests for calculation engine (src/engine.py)."""

import pytest
import math
from src.engine import (
    calculate_a_priori,
    calculate_post_hoc,
    compute_critical_chi2,
    compute_ncp,
    compute_power,
    EngineError
)


def test_contract_reference_a_priori():
    """K4-REF-01: A priori reference vector from CONTRACT.md."""
    res = calculate_a_priori(w=0.3, alpha=0.05, power=0.95, df=5)
    assert res["n_total"] == 220
    assert math.isclose(res["ncp"], 19.8, rel_tol=1e-6, abs_tol=1e-6)
    assert math.isclose(res["critical_chi2"], 11.0704977, rel_tol=1e-6, abs_tol=1e-6)
    assert math.isclose(res["actual_power"], 0.9502155, rel_tol=1e-6, abs_tol=1e-6)


def test_contract_reference_post_hoc():
    """K4-REF-02: Post hoc reference vector from CONTRACT.md."""
    res = calculate_post_hoc(w=0.3, alpha=0.05, n_total=100, df=5)
    assert math.isclose(res["ncp"], 9.0, rel_tol=1e-6, abs_tol=1e-6)
    assert math.isclose(res["critical_chi2"], 11.0704977, rel_tol=1e-6, abs_tol=1e-6)
    assert math.isclose(res["power"], 0.6235846, rel_tol=1e-6, abs_tol=1e-6)


def test_deterministic_behavior():
    """Ensures deterministic, idempotent execution across multiple calls."""
    res1 = calculate_a_priori(w=0.25, alpha=0.01, power=0.85, df=4)
    res2 = calculate_a_priori(w=0.25, alpha=0.01, power=0.85, df=4)
    assert res1 == res2


def test_invalid_and_out_of_range_w():
    """Negative, zero or non-numeric w must raise OUT_OF_RANGE or INVALID_VALUE."""
    with pytest.raises(EngineError) as exc_info:
        calculate_a_priori(w=-0.2, alpha=0.05, power=0.80, df=3)
    assert exc_info.value.code == "OUT_OF_RANGE"
    assert exc_info.value.field == "w"

    with pytest.raises(EngineError) as exc_info:
        calculate_a_priori(w="abc", alpha=0.05, power=0.80, df=3)
    assert exc_info.value.code == "INVALID_VALUE"


def test_invalid_and_out_of_range_alpha():
    """Alpha <= 0 or Alpha >= 1 must raise OUT_OF_RANGE."""
    with pytest.raises(EngineError) as exc_info:
        calculate_a_priori(w=0.3, alpha=1.2, power=0.80, df=3)
    assert exc_info.value.code == "OUT_OF_RANGE"
    assert exc_info.value.field == "alpha"


def test_power_lte_alpha_inconsistent():
    """Target power <= alpha is mathematically inconsistent."""
    with pytest.raises(EngineError) as exc_info:
        calculate_a_priori(w=0.3, alpha=0.05, power=0.04, df=3)
    assert exc_info.value.code == "INCONSISTENT"
    assert exc_info.value.field == "power"

    with pytest.raises(EngineError) as exc_info:
        calculate_a_priori(w=0.3, alpha=0.05, power=0.05, df=3)
    assert exc_info.value.code == "INCONSISTENT"


def test_fractional_df():
    """Fractional degrees of freedom (e.g. df=1.5) must raise INVALID_VALUE."""
    with pytest.raises(EngineError) as exc_info:
        calculate_a_priori(w=0.3, alpha=0.05, power=0.80, df=1.5)
    assert exc_info.value.code == "INVALID_VALUE"
    assert exc_info.value.field == "df"

    with pytest.raises(EngineError) as exc_info:
        calculate_a_priori(w=0.3, alpha=0.05, power=0.80, df="2.5")
    assert exc_info.value.code == "INVALID_VALUE"


def test_n_total_less_than_two():
    """Sample size < 2 in post hoc must raise OUT_OF_RANGE."""
    with pytest.raises(EngineError) as exc_info:
        calculate_post_hoc(w=0.3, alpha=0.05, n_total=1, df=2)
    assert exc_info.value.code == "OUT_OF_RANGE"
    assert exc_info.value.field == "n_total"
