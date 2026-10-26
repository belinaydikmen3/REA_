"""Clinical AI Research Assistant for Power Analysis (K4 chi2-contingency).

Strict Rule: The agent NEVER calculates sample size or statistical power itself.
It parses Turkish clinical research questions, maps them to parameters,
invokes the MCP 'power_analysis' tool, and explains the verified result.
"""

from typing import Dict, Any, List
import re
import time
from src.mcp_server import power_analysis


class ClinicalAgent:
    """Agent that translates Turkish clinical research queries to MCP tool calls."""

    def __init__(self):
        self.call_logs: List[Dict[str, Any]] = []

    def parse_clinical_query(self, query: str) -> Dict[str, Any]:
        """Parses clinical research query to extract statistical parameters."""
        params = {
            "test": "chi2-contingency",
            "mode": "a-priori",
            "w": 0.3,
            "alpha": 0.05,
            "df": 1,
            "power": None,
            "n_total": None
        }

        # 1. Mode determination
        q_lower = query.lower()
        if "gerçekleşen güç" in q_lower or "post hoc" in q_lower or "güç nedir" in q_lower or "gücü ne" in q_lower:
            params["mode"] = "post-hoc"
        else:
            params["mode"] = "a-priori"

        # 2. Extract w (effect size)
        w_match = re.search(r"w\s*=\s*([0-9\.]+)", q_lower)
        if w_match:
            params["w"] = float(w_match.group(1))
        elif "küçük etki" in q_lower:
            params["w"] = 0.1
        elif "orta etki" in q_lower or "orta düzey" in q_lower:
            params["w"] = 0.3
        elif "büyük etki" in q_lower:
            params["w"] = 0.5

        # 3. Extract alpha
        alpha_match = re.search(r"alfa\s*=\s*([0-9\.]+)|alpha\s*=\s*([0-9\.]+)|p\s*<\s*([0-9\.]+)|anlamlılık\s*=\s*([0-9\.]+)", q_lower)
        if alpha_match:
            for g in alpha_match.groups():
                if g:
                    params["alpha"] = float(g)
                    break

        # 4. Extract power
        power_match = re.search(r"güç\s*=\s*([0-9\.]+)|power\s*=\s*([0-9\.]+)|%\s*([0-9]+)\s*güç", q_lower)
        if power_match:
            if power_match.group(1):
                params["power"] = float(power_match.group(1))
            elif power_match.group(2):
                params["power"] = float(power_match.group(2))
            elif power_match.group(3):
                params["power"] = float(power_match.group(3)) / 100.0
        elif params["mode"] == "a-priori":
            params["power"] = 0.80  # Standart klinik varsayılan hedef güç

        # 5. Extract sample size (n_total)
        n_match = re.search(r"n\s*=\s*([0-9]+)|örneklem\s*=\s*([0-9]+)|([0-9]+)\s*hasta|([0-9]+)\s*denek|([0-9]+)\s*vaka|([0-9]+)\s*katılımcı|([0-9]+)\s*çocuk|([0-9]+)\s*birey", q_lower)
        if n_match:
            for g in n_match.groups():
                if g:
                    params["n_total"] = int(g)
                    break

        # 6. Extract df or table dimensions (r x c)
        df_match = re.search(r"df\s*=\s*([0-9]+)|serbestlik\s*=\s*([0-9]+)", q_lower)
        if df_match:
            for g in df_match.groups():
                if g:
                    params["df"] = int(g)
                    break
        else:
            # Check for grid size e.g. "3x2", "2x2", "4x3"
            table_match = re.search(r"([0-9]+)\s*[xX*]\s*([0-9]+)", q_lower)
            if table_match:
                r = int(table_match.group(1))
                c = int(table_match.group(2))
                params["df"] = (r - 1) * (c - 1)
            else:
                # Group comparison e.g. "3 tedavi grubu ve 2 yanıt durumu"
                grp_match = re.search(r"([0-9]+)\s*grup", q_lower)
                resp_match = re.search(r"([0-9]+)\s*yanıt", q_lower)
                if grp_match and resp_match:
                    r = int(grp_match.group(1))
                    c = int(resp_match.group(1))
                    params["df"] = (r - 1) * (c - 1)

        return params

    def consult(self, query: str) -> Dict[str, Any]:
        """Processes clinical query by delegating pure computation to MCP power_analysis tool."""
        start_time = time.perf_counter()
        parsed_params = self.parse_clinical_query(query)

        # DELEGATION: Call MCP tool without doing any math
        tool_args = {
            "test": parsed_params["test"],
            "mode": parsed_params["mode"],
            "w": parsed_params["w"],
            "alpha": parsed_params["alpha"],
            "df": parsed_params["df"]
        }
        if parsed_params["mode"] == "a-priori":
            tool_args["power"] = parsed_params["power"]
        else:
            tool_args["n_total"] = parsed_params["n_total"]

        tool_result = power_analysis(**tool_args)
        elapsed_sec = time.perf_counter() - start_time

        # Formulate clinical response in Turkish
        if "error" in tool_result:
            clinical_answer = f"Hesaplama hatası: {tool_result['error']} (Hata kodu: {tool_result['code']})"
        elif parsed_params["mode"] == "a-priori":
            clinical_answer = (
                f"Klinik araştırmanız için hedeflenen istatistiksel gücü (%{parsed_params['power']*100:.1f}) "
                f"ve anlamlılık düzeyini (alfa={parsed_params['alpha']}) sağlamak amacıyla "
                f"toplam en az {tool_result['n_total']} hasta/denek dahil edilmelidir. "
                f"Bu örneklemle gerçekleşecek kesin güç %{tool_result['actual_power']*100:.2f} "
                f"(kritik ki-kare = {tool_result['critical_chi2']:.4f}, NCP = {tool_result['ncp']:.2f}) olarak hesaplanmıştır."
            )
        else:
            clinical_answer = (
                f"Mevcut {parsed_params['n_total']} hasta/vaka ile yapılan ki-kare kontenjans testinin "
                f"istatistiksel gücü %{tool_result['power']*100:.2f} olarak gerçekleşmiştir "
                f"(kritik ki-kare = {tool_result['critical_chi2']:.4f}, NCP = {tool_result['ncp']:.2f})."
            )

        log_entry = {
            "query": query,
            "parsed_params": tool_args,
            "tool_called": "power_analysis",
            "tool_result": tool_result,
            "clinical_answer": clinical_answer,
            "latency_ms": round(elapsed_sec * 1000, 2)
        }
        self.call_logs.append(log_entry)

        return log_entry
