"""Unit and integration tests for CLI interface (src/cli.py)."""

import subprocess
import sys
import os
import json
import pytest

PYTHON_EXE = sys.executable


def run_cli(*args):
    """Helper function to run CLI command via subprocess."""
    cmd = [PYTHON_EXE, "-m", "src.cli"] + list(args)
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env
    )
    stdout_str = proc.stdout.strip() if proc.stdout else ""
    stderr_str = proc.stderr.strip() if proc.stderr else ""
    return proc.returncode, stdout_str, stderr_str


def test_cli_version():
    """--version must output JSON and exit 0."""
    code, out, err = run_cli("--version")
    assert code == 0
    data = json.loads(out)
    assert data["name"] == "gpower-clone"
    assert data["test_family"] == "chi2-contingency"
    assert data["team"] == "K4"


def test_cli_a_priori_success():
    """Successful a priori call must exit 0 and output valid single-line JSON."""
    code, out, err = run_cli(
        "--test", "chi2-contingency",
        "--mode", "a-priori",
        "--w", "0.3",
        "--alpha", "0.05",
        "--power", "0.95",
        "--df", "5"
    )
    assert code == 0
    assert "\n" not in out  # Single-line JSON
    data = json.loads(out)
    assert data["n_total"] == 220
    assert abs(data["ncp"] - 19.8) < 1e-6
    assert abs(data["critical_chi2"] - 11.0704977) < 1e-6
    assert abs(data["actual_power"] - 0.9502155) < 1e-6


def test_cli_post_hoc_success():
    """Successful post hoc call must exit 0 and output valid single-line JSON."""
    code, out, err = run_cli(
        "--test", "chi2-contingency",
        "--mode", "post-hoc",
        "--w", "0.3",
        "--alpha", "0.05",
        "--n_total", "100",
        "--df", "5"
    )
    assert code == 0
    assert "\n" not in out
    data = json.loads(out)
    assert abs(data["ncp"] - 9.0) < 1e-6
    assert abs(data["critical_chi2"] - 11.0704977) < 1e-6
    assert abs(data["power"] - 0.6235846) < 1e-6


def test_cli_missing_param():
    """Missing required parameter must exit 2 with MISSING_PARAM."""
    code, out, err = run_cli(
        "--test", "chi2-contingency",
        "--mode", "a-priori",
        "--w", "0.3",
        "--alpha", "0.05",
        "--df", "5"
    )
    assert code == 2
    data = json.loads(out)
    assert data["code"] == "MISSING_PARAM"
    assert data["field"] == "power"


def test_cli_unknown_param():
    """Irrelevant or unknown parameter must exit 2 with UNKNOWN_PARAM."""
    code, out, err = run_cli(
        "--test", "chi2-contingency",
        "--mode", "post-hoc",
        "--w", "0.3",
        "--alpha", "0.05",
        "--n_total", "100",
        "--df", "5",
        "--tails", "2"
    )
    assert code == 2
    data = json.loads(out)
    assert data["code"] == "UNKNOWN_PARAM"


def test_cli_unsupported_test():
    """Unsupported test family must exit 2 with UNSUPPORTED."""
    code, out, err = run_cli(
        "--test", "t2-indep",
        "--mode", "a-priori",
        "--w", "0.3",
        "--alpha", "0.05",
        "--power", "0.95",
        "--df", "5"
    )
    assert code == 2
    data = json.loads(out)
    assert data["code"] == "UNSUPPORTED"
    assert data["field"] == "test"


def test_cli_unsupported_mode():
    """Unsupported mode must exit 2 with UNSUPPORTED."""
    code, out, err = run_cli(
        "--test", "chi2-contingency",
        "--mode", "compromise",
        "--w", "0.3",
        "--alpha", "0.05",
        "--df", "5"
    )
    assert code == 2
    data = json.loads(out)
    assert data["code"] == "UNSUPPORTED"
    assert data["field"] == "mode"


def test_cli_invalid_value_fractional_df():
    """Fractional df must exit 2 with INVALID_VALUE."""
    code, out, err = run_cli(
        "--test", "chi2-contingency",
        "--mode", "a-priori",
        "--w", "0.3",
        "--alpha", "0.05",
        "--power", "0.95",
        "--df", "1.5"
    )
    assert code == 2
    data = json.loads(out)
    assert data["code"] == "INVALID_VALUE"
    assert data["field"] == "df"


def test_cli_out_of_range_n_total():
    """Sample size < 2 must exit 2 with OUT_OF_RANGE."""
    code, out, err = run_cli(
        "--test", "chi2-contingency",
        "--mode", "post-hoc",
        "--w", "0.3",
        "--alpha", "0.05",
        "--n_total", "1",
        "--df", "5"
    )
    assert code == 2
    data = json.loads(out)
    assert data["code"] == "OUT_OF_RANGE"
    assert data["field"] == "n_total"


def test_cli_inconsistent_power():
    """Power <= alpha must exit 2 with INCONSISTENT."""
    code, out, err = run_cli(
        "--test", "chi2-contingency",
        "--mode", "a-priori",
        "--w", "0.3",
        "--alpha", "0.05",
        "--power", "0.04",
        "--df", "5"
    )
    assert code == 2
    data = json.loads(out)
    assert data["code"] == "INCONSISTENT"
    assert data["field"] == "power"
