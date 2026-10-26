"""Equivalence tests between CLI and MCP tool (power_analysis) across 25 vectors."""

import csv
import os
import sys
import subprocess
import json
import pytest
from src.mcp_server import power_analysis

ORACLE_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "oracle", "gpower_vectors.csv")
PYTHON_EXE = sys.executable


def load_valid_vectors(limit=25):
    """Loads first N valid vectors from oracle CSV."""
    vectors = []
    with open(ORACLE_CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"] == "VALID":
                vectors.append(row)
                if len(vectors) >= limit:
                    break
    return vectors


@pytest.mark.parametrize("vector", load_valid_vectors(25))
def test_cli_mcp_equivalence(vector):
    """Verifies that MCP output is 100% equivalent to CLI output for 25 different vectors."""
    mode = vector["mode"]
    w = float(vector["w"])
    alpha = float(vector["alpha"])
    df = int(vector["df"])

    # 1. Run via CLI
    cli_args = [
        PYTHON_EXE, "-m", "src.cli",
        "--test", "chi2-contingency",
        "--mode", mode,
        "--w", str(w),
        "--alpha", str(alpha),
        "--df", str(df)
    ]

    if mode == "a-priori":
        power = float(vector["power"])
        cli_args.extend(["--power", str(power)])
        mcp_res = power_analysis(
            test="chi2-contingency",
            mode="a-priori",
            w=w,
            alpha=alpha,
            df=df,
            power=power
        )
    else:
        n_total = int(vector["n_total"])
        cli_args.extend(["--n_total", str(n_total)])
        mcp_res = power_analysis(
            test="chi2-contingency",
            mode="post-hoc",
            w=w,
            alpha=alpha,
            df=df,
            n_total=n_total
        )

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(cli_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    assert proc.returncode == 0
    cli_res = json.loads(proc.stdout.strip())

    # 2. Assert exact key and value equivalence
    assert set(cli_res.keys()) == set(mcp_res.keys())
    for k in cli_res:
        if isinstance(cli_res[k], float):
            assert abs(cli_res[k] - mcp_res[k]) < 1e-12
        else:
            assert cli_res[k] == mcp_res[k]
