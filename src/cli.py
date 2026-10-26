"""CLI wrapper for gpower-clone (K4 chi2-contingency).

Strict adherence to CONTRACT.md:
- Single-line pure JSON output on stdout
- Exit code 0 for success
- Exit code 2 for input errors / contract violations with JSON: {"error": "...", "code": "...", "field": "..."}
- Exit code 1 for internal errors
- Version support: --version
"""

import sys
import json
import os
from typing import Dict, List, Tuple
from src.engine import calculate_a_priori, calculate_post_hoc, EngineError

# Ensure UTF-8 output encoding across Windows/Linux
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SUPPORTED_TEST = "chi2-contingency"
SUPPORTED_MODES = ["a-priori", "post-hoc"]
VERSION_INFO = {
    "name": "gpower-clone",
    "test_family": "chi2-contingency",
    "version": "1.0.0",
    "team": "K4"
}


def print_error_and_exit(message: str, code: str, field: str, exit_code: int = 2) -> None:
    """Outputs single-line JSON error to stdout and terminates with given exit code."""
    payload = {
        "error": message,
        "code": code,
        "field": field
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=True) + "\n")
    sys.stdout.flush()
    sys.exit(exit_code)


def parse_raw_args(args: List[str]) -> Tuple[Dict[str, str], List[str]]:
    """Strict argument parser for CLI flags."""
    parsed: Dict[str, str] = {}
    unknown: List[str] = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("--version", "-v"):
            parsed["version"] = "true"
            i += 1
        elif arg.startswith("--"):
            key = arg[2:]
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                val = args[i + 1]
                i += 2
            else:
                val = ""
                i += 1
            parsed[key] = val
        else:
            unknown.append(arg)
            i += 1
    return parsed, unknown


def main(cli_args: List[str] = None) -> None:
    if cli_args is None:
        cli_args = sys.argv[1:]

    # 1. Version check
    if "--version" in cli_args or "-v" in cli_args:
        sys.stdout.write(json.dumps(VERSION_INFO, ensure_ascii=True) + "\n")
        sys.stdout.flush()
        sys.exit(0)

    try:
        parsed_args, unknown_positionals = parse_raw_args(cli_args)

        if unknown_positionals:
            print_error_and_exit(
                f"Beklenmeyen argüman(lar): {', '.join(unknown_positionals)}",
                "UNKNOWN_PARAM",
                unknown_positionals[0]
            )

        # 2. Check test family
        test_family = parsed_args.get("test")
        if not test_family:
            print_error_and_exit("Parametre 'test' zorunludur.", "MISSING_PARAM", "test")
        if test_family != SUPPORTED_TEST:
            print_error_and_exit(
                f"Desteklenmeyen test ailesi: '{test_family}'. Yalnızca '{SUPPORTED_TEST}' desteklenir.",
                "UNSUPPORTED",
                "test"
            )

        # 3. Check mode
        mode = parsed_args.get("mode")
        if not mode:
            print_error_and_exit("Parametre 'mode' zorunludur.", "MISSING_PARAM", "mode")
        if mode not in SUPPORTED_MODES:
            print_error_and_exit(
                f"Desteklenmeyen hesaplama modu: '{mode}'. Yalnızca {SUPPORTED_MODES} desteklenir.",
                "UNSUPPORTED",
                "mode"
            )

        # Check for unknown parameters
        known_ap_keys = {"test", "mode", "w", "alpha", "power", "df"}
        known_ph_keys = {"test", "mode", "w", "alpha", "n_total", "df"}

        allowed_keys = known_ap_keys if mode == "a-priori" else known_ph_keys
        for key in parsed_args:
            if key not in allowed_keys and key != "version":
                print_error_and_exit(
                    f"'{mode}' modunda beklenmeyen veya ilgisiz parametre: '--{key}'",
                    "UNKNOWN_PARAM",
                    key
                )

        # 4. Mode-specific execution
        w = parsed_args.get("w")
        alpha = parsed_args.get("alpha")
        df = parsed_args.get("df")

        if mode == "a-priori":
            power = parsed_args.get("power")
            result = calculate_a_priori(w=w, alpha=alpha, power=power, df=df)
        else:  # post-hoc
            n_total = parsed_args.get("n_total")
            result = calculate_post_hoc(w=w, alpha=alpha, n_total=n_total, df=df)

        # Successful output
        sys.stdout.write(json.dumps(result, ensure_ascii=True) + "\n")
        sys.stdout.flush()
        sys.exit(0)

    except EngineError as ee:
        print_error_and_exit(ee.message, ee.code, ee.field, exit_code=2)
    except Exception as ex:
        # Internal unexpected system error
        print_error_and_exit(f"İç hesaplama hatası: {str(ex)}", "INTERNAL_ERROR", "system", exit_code=1)


if __name__ == "__main__":
    main()
