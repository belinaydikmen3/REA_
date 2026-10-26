# gpower-clone: K4 Chi-Square Contingency Tables

**YZM301 Teardown Sprint — Bağımsız İstatistiksel Güç Analizi Hesaplama Motoru**

[![Tests](https://img.shields.io/badge/tests-83%2F83%20passed-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)]()
[![SciPy](https://img.shields.io/badge/scipy-1.18.1-orange.svg)]()
[![License](https://img.shields.io/badge/license-Educational-lightgrey.svg)]()

> ⚠️ **Yasal ve Etik Bildirim:** Bu proje bir eğitim çalışmasıdır. Orijinal yazılımın (G*Power) telifli kaynak kodunu veya ikili dosyalarını içermez. Proje, hakemli akademik yayınlarda (Faul et al., 2007, 2009; Cohen, 1988) açıklanan matematiksel modelleri temel alarak temiz oda (clean room) ilkelerine tam uyumlu biçimde bağımsız olarak geliştirilmiştir. Uygulama ticari olarak G*Power olarak adlandırılamaz.

---

## 1. Proje Amacı ve K4 Test Ailesi

Bu projenin amacı, G*Power 3.1.9.7 yazılımının **K4** ailesi davranışını tersine mühendislik ve istatistiksel analiz yöntemleriyle inceleyerek bağımsız, deterministik ve yüksek hassasiyetli bir hesaplama motoru, CLI arayüzü, MCP aracı ve klinik yapay zeka danışmanı geliştirmektir.

- **Atanan Test Ailesi:** `K4 — chi2-contingency`
- **G*Power Karşılığı:** `χ² tests – Goodness-of-fit tests: Contingency tables`
- **Klinik Kullanım Senaryosu:** Çoklu tedavi gruplarının klinik yanıt/iyileşme oranları arasındaki farkların incelenmesi, tedavi etkinliğinin ki-kare testiyle analizi ve klinik deneyler öncesinde/sonrasında örneklem büyüklüğü ve test gücünün belirlenmesi.

---

## 2. Gerçekleştirilen Özellikler

1. **A Priori Modu (`--mode a-priori`):**
   - Hedeflenen test gücünü ($1-\beta$) karşılamak için gereken minimal tamsayı toplam örneklem büyüklüğünü ($N \ge 2$) monotonik tamsayı arama algoritmasıyla bulur.
   - Noncentrality parameter (`ncp`), kritik ki-kare (`critical_chi2`), örneklem büyüklüğü (`n_total`) ve gerçekleşen güç (`actual_power`) üretir.
2. **Post Hoc Modu (`--mode post-hoc`):**
   - Verilen toplam örneklem büyüklüğü ($N$), etki büyüklüğü ($w$), anlamlılık düzeyi ($\alpha$) ve serbestlik derecesi ($df$) ile testin gücünü (`power`) hesaplar.
3. **Kapsamlı CLI Arayüzü (`gpower-clone`):**
   - Tek satır saf JSON çıktısı (stdout).
   - Başarıda çıkış kodu `0`, sözleşme ihlali ve hatalı girdilerde çıkış kodu `2`, iç hatalarda `1`.
   - Standart hata kodları (`MISSING_PARAM`, `UNKNOWN_PARAM`, `INVALID_VALUE`, `OUT_OF_RANGE`, `INCONSISTENT`, `UNSUPPORTED`).
   - Sürüm çıktısı (`gpower-clone --version`).
4. **Sayısal Doğruluk ve Hassasiyet:**
   - Double (float64) hassasiyetinde tam analitik hesaplama. Keyfî erken yuvarlama yapılmaz.
   - Örneklem büyüklüğü $N$ için %100 tam eşleşme, sürekli değişkenler için $\le 10^{-6}$ mutlak/bağıl tolerans.
5. **Bonus 1 — MCP Sunucusu (`src/mcp_server.py`):**
   - Tek hesaplama motorunu kullanan `power_analysis` MCP aracı.
   - 25 farklı test vektöründe CLI çıktısıyla %100 tam eşdeğerlik doğrulanmıştır.
6. **Bonus 2 — Klinik AI Araştırma Danışmanı (`src/clinical_agent.py`):**
   - Türkçe klinik soruları anlar, parametreleri ayıklar ve HESABI KENDİSİ YAPMADAN doğrudan `power_analysis` aracına devreder.
   - 10 sentetik klinik senaryoda %100 doğrulukla test edilmiştir.

---

## 3. Matematiksel Temeller

1. **Cohen'in $w$ Etki Büyüklüğü:**
   $$w = \sqrt{\sum_{i=1}^{m} \frac{(p_{1i} - p_{0i})^2}{p_{0i}}} = \sqrt{\frac{\chi^2}{N}}$$
2. **Noncentrality Parameter (NCP / $\lambda$):**
   $$\lambda = w^2 \cdot N$$
3. **Kritik Ki-Kare Değeri ($\chi^2_{crit}$):**
   $$\chi^2_{crit} = F_{\chi^2(df)}^{-1}(1 - \alpha)$$
4. **İstatistiksel Güç ($1 - \beta$):**
   $$\text{Power} = P(X \ge \chi^2_{crit} \mid df, \lambda) = 1 - F_{\chi^2(df, \lambda)}(\chi^2_{crit})$$
5. **Örneklem Arama (A Priori):**
   $$\min \{ N \in \mathbb{Z}^+ \mid N \ge 2 \text{ ve } \text{Power}(N) \ge \text{target\_power} \}$$

---

## 4. Kurulum ve Çalıştırma

### 4.1 Gereksinimler
- Python 3.10+ (Test edilen: Python 3.13.14)
- SciPy $\ge$ 1.10.0 (Test edilen: SciPy 1.18.1)
- pytest $\ge$ 7.0.0 (Test edilen: pytest 9.1.1)

### 4.2 Kurulum Adımları
```bash
# 1. Sanal ortamı oluşturun ve aktifleştirin
python -m venv .venv

# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

# 2. Bağımlılıkları ve paketi geliştirici modunda kurun
pip install scipy pytest -e .
```

---

## 5. CLI Kullanım Örnekleri

### 5.1 A Priori Modu (Örneklem Büyüklüğü Hesaplama)
```bash
gpower-clone --test chi2-contingency --mode a-priori --w 0.3 --alpha 0.05 --power 0.95 --df 5
```
**Çıktı (tek satır saf JSON):**
```json
{"ncp": 19.8, "critical_chi2": 11.070497693516351, "n_total": 220, "actual_power": 0.9502155018970163}
```

### 5.2 Post Hoc Modu (Gerçekleşen Güç Analizi)
```bash
gpower-clone --test chi2-contingency --mode post-hoc --w 0.3 --alpha 0.05 --n_total 100 --df 5
```
**Çıktı:**
```json
{"ncp": 9.0, "critical_chi2": 11.070497693516351, "power": 0.6235846116825704}
```

### 5.3 Sürüm Bilgisi
```bash
gpower-clone --version
```
**Çıktı:**
```json
{"name": "gpower-clone", "test_family": "chi2-contingency", "version": "1.0.0", "team": "K4"}
```

### 5.4 Hatalı Çağrı Örneği (Exit Code 2)
```bash
gpower-clone --test chi2-contingency --mode a-priori --w 0.3 --alpha 0.05 --df 5
```
**Hata Çıktısı:**
```json
{"error": "Parametre 'power' a-priori modunda zorunludur.", "code": "MISSING_PARAM", "field": "power"}
```

---

## 6. Test Komutları ve Diferansiyel Uyumluluk

Tüm test paketini çalıştırmak için:
```bash
pytest tests/ -v
```

### Diferansiyel Test Raporu Özeti
- **Toplam Test:** 83 / 83 PASSED (%100 Başarı)
- **Oracle Vektör Sayısı:** 39 adet (17 A priori, 16 Post hoc, 6 Hata/Sınır)
- **A Priori $N$ Tam Eşleşme Oranı:** %100 (17/17 tam eşleşme, sıfır hata)
- **Sayısal Tolerans Uyumu ($\le 10^{-6}$):** %100 (Tüm çıktılar $10^{-8}$ hassasiyetinde)
- **MCP Eşdeğerlik Testi:** %100 (25/25 vektörde CLI ile tam özdeş)
- **Klinik Ajan Doğruluğu:** %100 (10/10 sentetik soruda hatasız araç çağrısı)

Detaylı raporlar:
- Diferansiyel Test Raporu: [tests/compliance_report.md](tests/compliance_report.md)
- Klinik AI Ajanı Değerlendirmesi: [eval/clinical_agent_report.md](eval/clinical_agent_report.md)

---

## 7. Temiz Oda Süreci ve İzlenebilirlik

Proje iki ayrı aşamada gerçekleştirilmiştir:
1. **Oturum 1 (İnceleme & Şartname):** G*Power 3.1.9.7 matematiksel ve mimari davranışları incelenmiş, kanıtlar [LEDGER.md](LEDGER.md) dosyasına kaydedilmiş, kabul kriterleri [SPEC.md](SPEC.md) olarak yazılmış ve 39 referans vektörü [oracle/gpower_vectors.csv](oracle/gpower_vectors.csv) içerisine kaydedilmiştir.
2. **Oturum 2 (Bağımsız Uygulama):** Yalnızca `SPEC.md` ve `CONTRACT.md` girdi alınarak [src/engine.py](src/engine.py), [src/cli.py](src/cli.py), [src/mcp_server.py](src/mcp_server.py) ve [src/clinical_agent.py](src/clinical_agent.py) sıfırdan bağımsız olarak geliştirilmiş ve test edilmiştir.

Süreçte yaşanan doğrulanmış yanılgılar ve teknik çözümler [HALLUCINATIONS.md](HALLUCINATIONS.md) dosyasında şeffafça belgelenmiştir. Ajan maliyet ve iterasyon dökümü [AGENT_COST.md](AGENT_COST.md) dosyasında yer almaktadır.

---

## 8. Referans Yazılım ve Hash Bilgisi

- **Referans Yazılım:** G*Power 3.1.9.7 (Resmi dağıtım: Heinrich Heine Universität Düsseldorf)
- **Resmi Web:** https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower
- **Arşiv Adı:** `GPowerWin_3.1.9.7.zip`
- **Dosya Boyutu:** 2,287,616 bytes
- **SHA-256 Hash:** `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`

---

## 9. Bilinen Sınırlamalar ve Demo

- **Kapsam:** Yalnızca K4 `chi2-contingency` ailesini ve `a-priori` ile `post-hoc` modlarını destekler (`compromise`, `criterion`, `sensitivity` modları sonraki sürümlere bırakılmıştır).
- **Hücre Frekansları:** Doğrudan hücre bazlı $r \times c$ frekans matrisleri yerine G*Power standardı olan özet $w$ ve $df$ parametreleriyle çalışır.
- **Demo Video:** [60 Saniyelik CLI Tanıtım ve Doğrulama Videosu (YouTube / Drive Linki)](https://youtu.be/placeholder-k4-demo)

---

## 10. Akademik Atıf

Bu projede kullanılan istatistiksel algoritmalar ve matematiksel formüller şu yayınlara dayanmaktadır:

1. **Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A.** (2007). *G\*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences.* Behavior Research Methods, 39(2), 175–191.
2. **Faul, F., Erdfelder, E., Buchner, A., & Lang, A.-G.** (2009). *Statistical power analyses using G\*Power 3.1: Tests for correlation and regression analyses.* Behavior Research Methods, 41(4), 1149–1160.
3. **Cohen, J.** (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
