"""MCP (Model Context Protocol) Server implementation for power analysis (YZM301 K4).

Tool Name: power_analysis
Single Source of Truth: Uses src.engine calculation engine directly.
"""

from typing import Dict, Any, Optional
import json
from src.engine import calculate_a_priori, calculate_post_hoc, EngineError


def power_analysis(
    test: str,
    mode: str,
    w: float,
    alpha: float,
    df: int,
    power: Optional[float] = None,
    n_total: Optional[int] = None
) -> Dict[str, Any]:
    """MCP tool for statistical power analysis of contingency tables (K4 chi2-contingency).
    
    Args:
        test: Statistical test family (must be 'chi2-contingency').
        mode: Calculation mode ('a-priori' or 'post-hoc').
        w: Cohen's effect size w (> 0).
        alpha: Type I error probability (0 < alpha < 1).
        df: Degrees of freedom (integer >= 1).
        power: Desired statistical power (required for a-priori).
        n_total: Total sample size (required for post-hoc).
        
    Returns:
        Exact JSON-compatible dictionary identical to CLI output.
    """
    if test != "chi2-contingency":
        return {
            "error": f"Desteklenmeyen test ailesi: '{test}'. Yalnızca 'chi2-contingency' desteklenir.",
            "code": "UNSUPPORTED",
            "field": "test"
        }

    if mode not in ("a-priori", "post-hoc"):
        return {
            "error": f"Desteklenmeyen mod: '{mode}'. Yalnızca 'a-priori' ve 'post-hoc' desteklenir.",
            "code": "UNSUPPORTED",
            "field": "mode"
        }

    try:
        if mode == "a-priori":
            if power is None:
                return {
                    "error": "Parametre 'power' a-priori modunda zorunludur.",
                    "code": "MISSING_PARAM",
                    "field": "power"
                }
            if n_total is not None:
                return {
                    "error": "'a-priori' modunda beklenmeyen parametre: 'n_total'",
                    "code": "UNKNOWN_PARAM",
                    "field": "n_total"
                }
            return calculate_a_priori(w=w, alpha=alpha, power=power, df=df)
        else:  # post-hoc
            if n_total is None:
                return {
                    "error": "Parametre 'n_total' post-hoc modunda zorunludur.",
                    "code": "MISSING_PARAM",
                    "field": "n_total"
                }
            if power is not None:
                return {
                    "error": "'post-hoc' modunda beklenmeyen parametre: 'power'",
                    "code": "UNKNOWN_PARAM",
                    "field": "power"
                }
            return calculate_post_hoc(w=w, alpha=alpha, n_total=n_total, df=df)

    except EngineError as ee:
        return ee.to_dict()
    except Exception as ex:
        return {
            "error": f"İç hesaplama hatası: {str(ex)}",
            "code": "INTERNAL_ERROR",
            "field": "system"
        }
