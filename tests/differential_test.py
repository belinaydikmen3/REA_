"""Differential testing harness against oracle reference vectors (oracle/gpower_vectors.csv)."""

import csv
import os
import math
import subprocess
import sys
import json
import pytest
from src.engine import calculate_a_priori, calculate_post_hoc, EngineError

ORACLE_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "oracle", "gpower_vectors.csv")
PYTHON_EXE = sys.executable


def load_oracle_vectors():
    """Loads all test vectors from oracle CSV."""
    vectors = []
    with open(ORACLE_CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vectors.append(row)
    return vectors


@pytest.mark.parametrize("vector", [v for v in load_oracle_vectors() if v["status"] == "VALID"])
def test_differential_valid_vector(vector):
    """Verifies that engine output matches oracle vector within strict numerical tolerance (1e-6) and exact N."""
    mode = vector["mode"]
    w = float(vector["w"])
    alpha = float(vector["alpha"])
    df = int(vector["df"])
    expected_crit = float(vector["critical_chi2"])
    expected_ncp = float(vector["ncp"])

    if mode == "a-priori":
        power = float(vector["power"])
        expected_n = int(vector["n_total"])
        expected_act_p = float(vector["actual_power"])

        res = calculate_a_priori(w=w, alpha=alpha, power=power, df=df)

        # 1. Exact sample size match (zero error)
        assert res["n_total"] == expected_n, f"Vector {vector['vector_id']}: n_total mismatch! got {res['n_total']}, expected {expected_n}"

        # 2. Strict tolerance <= 1e-6 for float fields
        assert math.isclose(res["critical_chi2"], expected_crit, rel_tol=1e-6, abs_tol=1e-6)
        assert math.isclose(res["ncp"], expected_ncp, rel_tol=1e-6, abs_tol=1e-6)
        assert math.isclose(res["actual_power"], expected_act_p, rel_tol=1e-6, abs_tol=1e-6)

    elif mode == "post-hoc":
        n_total = int(vector["n_total"])
        expected_p = float(vector["power"])

        res = calculate_post_hoc(w=w, alpha=alpha, n_total=n_total, df=df)

        assert math.isclose(res["critical_chi2"], expected_crit, rel_tol=1e-6, abs_tol=1e-6)
        assert math.isclose(res["ncp"], expected_ncp, rel_tol=1e-6, abs_tol=1e-6)
        assert math.isclose(res["power"], expected_p, rel_tol=1e-6, abs_tol=1e-6)


@pytest.mark.parametrize("vector", [v for v in load_oracle_vectors() if v["status"] != "VALID"])
def test_differential_error_vector(vector):
    """Verifies that invalid or boundary vectors correctly produce expected error codes."""
    mode = vector["mode"]
    expected_code = vector["status"]

    w = float(vector["w"]) if vector["w"] else None
    alpha = float(vector["alpha"]) if vector["alpha"] else None
    df = float(vector["df"]) if vector["df"] else None
    power = float(vector["power"]) if vector["power"] else None
    n_total = float(vector["n_total"]) if vector["n_total"] else None

    with pytest.raises(EngineError) as exc_info:
        if mode == "a-priori":
            calculate_a_priori(w=w, alpha=alpha, power=power, df=df)
        else:
            calculate_post_hoc(w=w, alpha=alpha, n_total=n_total, df=df)

    assert exc_info.value.code == expected_code, f"Vector {vector['vector_id']}: expected {expected_code}, got {exc_info.value.code}"
