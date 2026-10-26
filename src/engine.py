"""Chi-Square Contingency Tables Calculation Engine (K4).

G*Power Equivalent:
    χ² tests – Goodness-of-fit tests: Contingency tables

Mathematical Model:
    - Noncentrality parameter: lambda = w^2 * N
    - Critical chi-square: crit = chi2.ppf(1 - alpha, df)
    - Statistical power: power = 1 - ncx2.cdf(crit, df, lambda) = ncx2.sf(crit, df, lambda)
    - A priori sample size search: Minimal integer N >= 2 such that actual_power >= target_power.
"""

from typing import Dict, Any, Union
import math
import scipy.stats as stats


class EngineError(Exception):
    """Custom exception class for statistical engine validation and calculation errors."""
    def __init__(self, message: str, code: str, field: str):
        super().__init__(message)
        self.message = message
        self.code = code
        self.field = field

    def to_dict(self) -> Dict[str, str]:
        return {
            "error": self.message,
            "code": self.code,
            "field": self.field
        }


def validate_common_params(w: Any, alpha: Any, df: Any) -> tuple[float, float, int]:
    """Validates common parameters (w, alpha, df) for chi2 contingency tests."""
    # 1. w validation
    if w is None:
        raise EngineError("Parametre 'w' zorunludur.", "MISSING_PARAM", "w")
    try:
        w_float = float(w)
    except (ValueError, TypeError):
        raise EngineError("Parametre 'w' sayısal bir değer olmalıdır.", "INVALID_VALUE", "w")
    if math.isnan(w_float) or math.isinf(w_float):
        raise EngineError("Parametre 'w' geçerli bir reel sayı olmalıdır.", "INVALID_VALUE", "w")
    if w_float <= 0.0:
        raise EngineError("Cohen'in etki büyüklüğü w sıfırdan büyük olmalıdır (w > 0).", "OUT_OF_RANGE", "w")

    # 2. alpha validation
    if alpha is None:
        raise EngineError("Parametre 'alpha' zorunludur.", "MISSING_PARAM", "alpha")
    try:
        alpha_float = float(alpha)
    except (ValueError, TypeError):
        raise EngineError("Parametre 'alpha' sayısal bir değer olmalıdır.", "INVALID_VALUE", "alpha")
    if math.isnan(alpha_float) or math.isinf(alpha_float):
        raise EngineError("Parametre 'alpha' geçerli bir reel sayı olmalıdır.", "INVALID_VALUE", "alpha")
    if not (0.0 < alpha_float < 1.0):
        raise EngineError("Anlamlılık düzeyi alpha (0, 1) aralığında olmalıdır.", "OUT_OF_RANGE", "alpha")

    # 3. df validation
    if df is None:
        raise EngineError("Parametre 'df' zorunludur.", "MISSING_PARAM", "df")
    try:
        if isinstance(df, str):
            if "." in df:
                # Kesirli string örn. "1.5"
                float_val = float(df)
                if not float_val.is_integer():
                    raise EngineError("Serbestlik derecesi df pozitif bir tamsayı olmalıdır.", "INVALID_VALUE", "df")
                df_int = int(float_val)
            else:
                df_int = int(df)
        elif isinstance(df, float):
            if not df.is_integer():
                raise EngineError("Serbestlik derecesi df pozitif bir tamsayı olmalıdır.", "INVALID_VALUE", "df")
            df_int = int(df)
        elif isinstance(df, int):
            df_int = df
        else:
            raise EngineError("Serbestlik derecesi df bir tamsayı olmalıdır.", "INVALID_VALUE", "df")
    except ValueError:
        raise EngineError("Parametre 'df' sayısal bir tamsayı olmalıdır.", "INVALID_VALUE", "df")

    if df_int < 1:
        raise EngineError("Serbestlik derecesi df en az 1 olmalıdır (df >= 1).", "OUT_OF_RANGE", "df")

    return w_float, alpha_float, df_int


def compute_critical_chi2(alpha: float, df: int) -> float:
    """Computes critical chi-square value for significance level alpha and degrees of freedom df."""
    return float(stats.chi2.ppf(1.0 - alpha, df))


def compute_ncp(w: float, n_total: Union[int, float]) -> float:
    """Computes noncentrality parameter lambda = w^2 * N."""
    return float((w ** 2) * n_total)


def compute_power(critical_chi2: float, df: int, ncp: float) -> float:
    """Computes statistical power = P(chi2(df, ncp) >= critical_chi2)."""
    if ncp < 0:
        return 0.0
    power = float(stats.ncx2.sf(critical_chi2, df, ncp))
    # Güç olasılık olduğundan [0, 1] aralığında kalmalıdır
    if power < 0.0:
        return 0.0
    if power > 1.0:
        return 1.0
    return power


def calculate_post_hoc(w: Any, alpha: Any, n_total: Any, df: Any) -> Dict[str, Union[float, int]]:
    """Executes post hoc power analysis.
    
    Given w, alpha, n_total, and df, computes:
        - ncp
        - critical_chi2
        - power
    """
    w_val, alpha_val, df_val = validate_common_params(w, alpha, df)

    if n_total is None:
        raise EngineError("Parametre 'n_total' post-hoc modunda zorunludur.", "MISSING_PARAM", "n_total")

    try:
        if isinstance(n_total, str):
            if "." in n_total:
                float_val = float(n_total)
                if not float_val.is_integer():
                    raise EngineError("Toplam örneklem büyüklüğü n_total bir tamsayı olmalıdır.", "INVALID_VALUE", "n_total")
                n_int = int(float_val)
            else:
                n_int = int(n_total)
        elif isinstance(n_total, float):
            if not n_total.is_integer():
                raise EngineError("Toplam örneklem büyüklüğü n_total bir tamsayı olmalıdır.", "INVALID_VALUE", "n_total")
            n_int = int(n_total)
        elif isinstance(n_total, int):
            n_int = n_total
        else:
            raise EngineError("Parametre 'n_total' geçerli bir tamsayı olmalıdır.", "INVALID_VALUE", "n_total")
    except ValueError:
        raise EngineError("Parametre 'n_total' sayısal bir tamsayı olmalıdır.", "INVALID_VALUE", "n_total")

    if n_int < 2:
        raise EngineError("Toplam örneklem büyüklüğü n_total en az 2 olmalıdır (n_total >= 2).", "OUT_OF_RANGE", "n_total")

    crit = compute_critical_chi2(alpha_val, df_val)
    ncp_val = compute_ncp(w_val, n_int)
    p_val = compute_power(crit, df_val, ncp_val)

    return {
        "ncp": ncp_val,
        "critical_chi2": crit,
        "power": p_val
    }


def calculate_a_priori(w: Any, alpha: Any, power: Any, df: Any) -> Dict[str, Union[float, int]]:
    """Executes a priori sample size calculation.
    
    Given w, alpha, target power, and df, searches for minimal integer N >= 2 such that:
        actual_power >= target_power
    Returns:
        - ncp
        - critical_chi2
        - n_total
        - actual_power
    """
    w_val, alpha_val, df_val = validate_common_params(w, alpha, df)

    if power is None:
        raise EngineError("Parametre 'power' a-priori modunda zorunludur.", "MISSING_PARAM", "power")

    try:
        power_float = float(power)
    except (ValueError, TypeError):
        raise EngineError("Parametre 'power' sayısal bir değer olmalıdır.", "INVALID_VALUE", "power")

    if math.isnan(power_float) or math.isinf(power_float):
        raise EngineError("Parametre 'power' geçerli bir reel sayı olmalıdır.", "INVALID_VALUE", "power")

    if not (0.0 < power_float < 1.0):
        raise EngineError("Hedef güç (power) (0, 1) aralığında olmalıdır.", "OUT_OF_RANGE", "power")

    if power_float <= alpha_val:
        raise EngineError(
            f"Hedef güç ({power_float}), anlamlılık düzeyi alfa ({alpha_val}) değerinden büyük olmalıdır.",
            "INCONSISTENT",
            "power"
        )

    crit = compute_critical_chi2(alpha_val, df_val)

    # Monotonik tamsayı arama (Minimal integer N >= 2 such that power(N) >= target_power)
    # Kontrol 1: N = 2 zaten gücü karşılıyor mu?
    ncp_2 = compute_ncp(w_val, 2)
    p_2 = compute_power(crit, df_val, ncp_2)
    if p_2 >= power_float:
        return {
            "ncp": ncp_2,
            "critical_chi2": crit,
            "n_total": 2,
            "actual_power": p_2
        }

    # Üstel adımlarla üst sınırı (high) bul
    low = 2
    high = 4
    max_limit = 100_000_000  # Pratik üst sınır
    while high <= max_limit:
        ncp_h = compute_ncp(w_val, high)
        p_h = compute_power(crit, df_val, ncp_h)
        if p_h >= power_float:
            break
        low = high
        high *= 2

    if high > max_limit:
        raise EngineError("A priori örneklem büyüklüğü aramasında çözüm yakınsamadı.", "NO_SOLUTION", "power")

    # İkiye bölme (Binary Search) ile en küçük tamsayıyı bul
    best_n = high
    while low <= high:
        mid = (low + high) // 2
        mid_ncp = compute_ncp(w_val, mid)
        mid_p = compute_power(crit, df_val, mid_ncp)
        if mid_p >= power_float:
            best_n = mid
            high = mid - 1
        else:
            low = mid + 1

    final_ncp = compute_ncp(w_val, best_n)
    final_power = compute_power(crit, df_val, final_ncp)

    return {
        "ncp": final_ncp,
        "critical_chi2": crit,
        "n_total": int(best_n),
        "actual_power": final_power
    }
