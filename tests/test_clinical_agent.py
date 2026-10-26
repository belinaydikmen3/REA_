"""Evaluation test suite for Clinical AI Agent across 10 synthetic clinical questions.

Rule: Uses 100% synthetic research scenarios. No real patient data.
Verifies that:
- The agent extracts parameters from natural Turkish research queries.
- The agent invokes MCP 'power_analysis' tool without computing math itself.
- All 10 queries achieve 100% execution accuracy.
"""

import pytest
from src.clinical_agent import ClinicalAgent

# 10 Sentetik Klinik Senaryo Değerlendirme Seti
SYNTHETIC_CLINICAL_BENCHMARK = [
    {
        "id": "CLIN-01",
        "question": "3 farklı kemoterapi protokolünün 2 yıllık remisyon durumları (remisyon var/yok, 3x2 tablo) karşılaştırılacaktır. Orta etki büyüklüğü (w=0.3), alfa=0.05 ve %95 güç hedeflendiğinde gerekli toplam hasta sayısı nedir?",
        "expected_mode": "a-priori",
        "expected_df": 2,
        "expected_w": 0.3
    },
    {
        "id": "CLIN-02",
        "question": "Tip 2 diyabetik hastalarda yeni bir ilacın hipoglisemi gelişme sıklığı plasebo ile karşılaştırılacaktır (2x2 tablo, df=1). Küçük etki w=0.1, alfa=0.05, güç=0.80 için kaç denek gereklidir?",
        "expected_mode": "a-priori",
        "expected_df": 1,
        "expected_w": 0.1
    },
    {
        "id": "CLIN-03",
        "question": "Bir kardiyoloji çalışmasında 4 farklı stent tipinin restenoz oranları incelenmektedir (4x2 tablo, df=3). w=0.25, alfa=0.01 ve %90 güç için gerekli örneklem büyüklüğü nedir?",
        "expected_mode": "a-priori",
        "expected_df": 3,
        "expected_w": 0.25
    },
    {
        "id": "CLIN-04",
        "question": "Acil servise başvuran 150 hasta üzerinde triyaj skorlarının (3 kategori) yatış kararına etkisi incelenmiştir (3x2 tablo, df=2). w=0.3, alfa=0.05 ile yapılan bu çalışmanın gerçekleşen gücü nedir?",
        "expected_mode": "post-hoc",
        "expected_df": 2,
        "expected_w": 0.3
    },
    {
        "id": "CLIN-05",
        "question": "Hipertansiyon klinik araştırmasında 200 hasta incelenmiştir. 2x3 kontenjans tablosunda (df=2), w=0.2 ve alfa=0.05 için elde edilen istatistiksel güç nedir?",
        "expected_mode": "post-hoc",
        "expected_df": 2,
        "expected_w": 0.2
    },
    {
        "id": "CLIN-06",
        "question": "Onkoloji faz III çalışmasında büyük etki (w=0.5), alfa=0.001 ve %99 güç ile 5x2 kontenjans tablosu (df=4) için kaç hasta gerekmektedir?",
        "expected_mode": "a-priori",
        "expected_df": 4,
        "expected_w": 0.5
    },
    {
        "id": "CLIN-07",
        "question": "Nörolojik inme rehabilitasyonunda 2 grup hastada taburculuk bağımsızlık durumu (2x2 tablo, df=1) test edilecektir. w=0.4, alfa=0.05 ve %80 güç için örneklem büyüklüğü nedir?",
        "expected_mode": "a-priori",
        "expected_df": 1,
        "expected_w": 0.4
    },
    {
        "id": "CLIN-08",
        "question": "Cerrahi yara enfeksiyonu oranları 3 hastane arasında karşılaştırılmış ve toplam 300 hasta taranmıştır (3x2 tablo, df=2). w=0.15 ve alfa=0.05 için post hoc test gücü nedir?",
        "expected_mode": "post-hoc",
        "expected_df": 2,
        "expected_w": 0.15
    },
    {
        "id": "CLIN-09",
        "question": "Pediatrik aşı yanıtı çalışmasında 4 yaş grubu ve 3 antikor titresi düzeyi (4x3 tablo, df=6) incelenecektir. w=0.3, alfa=0.05 ve %90 güç için gereken toplam çocuk sayısı nedir?",
        "expected_mode": "a-priori",
        "expected_df": 6,
        "expected_w": 0.3
    },
    {
        "id": "CLIN-10",
        "question": "Radyoloji çalışmasında yapay zeka ve uzman hekim uyumu 80 vaka üzerinde test edilmiştir (2x2 tablo, df=1). w=0.35 ve alfa=0.05 için gerçekleşen güç nedir?",
        "expected_mode": "post-hoc",
        "expected_df": 1,
        "expected_w": 0.35
    }
]


def test_clinical_agent_10_queries_benchmark():
    """Evaluates agent across 10 benchmark queries and logs performance."""
    agent = ClinicalAgent()
    results = []

    for item in SYNTHETIC_CLINICAL_BENCHMARK:
        resp = agent.consult(item["question"])
        assert resp["tool_called"] == "power_analysis"
        assert "error" not in resp["tool_result"]

        parsed = resp["parsed_params"]
        assert parsed["mode"] == item["expected_mode"]
        assert parsed["df"] == item["expected_df"]
        assert abs(parsed["w"] - item["expected_w"]) < 1e-6
        assert resp["latency_ms"] >= 0

        # Check response content
        assert "Klinik araştırmanız" in resp["clinical_answer"] or "istatistiksel gücü" in resp["clinical_answer"]
        results.append(resp)

    assert len(agent.call_logs) == 10
    total_time_ms = sum(r["latency_ms"] for r in results)
    avg_latency = total_time_ms / len(results)

    print(f"\n[CLINICAL AGENT BENCHMARK] 10/10 Queries PASSED! Avg Latency: {avg_latency:.2f} ms")
