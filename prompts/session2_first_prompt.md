# Oturum 2: Temiz Oda Bağımsız Uygulama (Clean Room Implementation) Başlangıç Promptu

**Proje:** YZM301 Teardown Sprint  
**Test Ailesi:** K4 — `chi2-contingency` (G*Power: `χ² tests – Goodness-of-fit tests: Contingency tables`)  
**Giriş Koşulu:** YALNIZCA onaylanmış `SPEC.md`, `CONTRACT.md` ve genel Python/SciPy ortamı.  
**Temiz Oda İlkesi:** Tersine mühendislik iç notları, ikili decompile çıktıları veya REA oturum verileri bu oturuma AKTARILMAZ. Geliştirme tamamen davranışsal spesifikasyona ve sözleşmeye dayalı olarak sıfırdan yürütülür.

---

## Talimatlar

Sen bir kıdemli Python yazılım mühendisi, istatistiksel hesaplama uzmanı ve test mühendisisin. Temiz oda kuralına tam sadık kalarak bağımsız `gpower-clone` uygulamasını geliştir:

1. **Giriş Belgelerini İncele:**
   - `SPEC.md` dosyasındaki Gherkin kabul kriterlerini oku.
   - `CONTRACT.md` dosyasındaki CLI bayraklarını, hata kodlarını, sayısal toleransları ($10^{-6}$, N tam eşleşme) ve tek satır JSON gereksinimini doğrula.

2. **Hesaplama Motoru (`src/engine.py`):**
   - CLI'dan tamamen bağımsız bir modül olarak yaz.
   - Fonksiyonlar:
     - Girdi doğrulama ($w > 0$, $0 < \alpha < 1$, $0 < \text{power} < 1$, $df \ge 1$, $n\_total \ge 2$, `power > alpha`).
     - Kritik ki-kare hesabı: $\chi^2_{crit} = \text{chi2.ppf}(1 - \alpha, df)$.
     - Noncentrality parameter hesabı: $\lambda = w^2 \cdot N$.
     - Post hoc güç hesabı: $\text{Power} = \text{ncx2.sf}(\chi^2_{crit}, df, \lambda)$.
     - A priori tamsayı örneklem arama: Hedef gücü ($\ge \text{power}$) sağlayan minimal $N \ge 2$ tamsayısının monotonik aramayla bulunması.
     - Çıktı sözleşmesi: float değerlerde tam double hassasiyeti, N için tamsayı.

3. **CLI Arayüzü (`src/cli.py` ve `gpower-clone`):**
   - Komut adı: `gpower-clone`.
   - Parametreleri ayrıştır; eksik, hatalı veya modla ilgisiz parametrelerde sözleşmeye uygun JSON basarak çıkış kodu `2` ile sonlan (`MISSING_PARAM`, `UNKNOWN_PARAM`, `INVALID_VALUE`, `OUT_OF_RANGE`, `INCONSISTENT`, `UNSUPPORTED`).
   - Başarılı çağrılarda yalnızca tek satır JSON bas ve çıkış kodu `0` döndür.
   - `gpower-clone --version` desteğini ekle.

4. **Kapsamlı Test ve Doğrulama (`tests/`):**
   - `tests/test_engine.py`: Motor birim testleri, formül ve arama doğrulamaları.
   - `tests/test_cli.py`: CLI çıkış kodları, parametre validasyonları, hata formatı ve stdout temizliği.
   - `tests/differential_test.py`: `oracle/gpower_vectors.csv` içindeki 39 vektörle diferansiyel testler; %100 N eşleşmesi ve $10^{-6}$ sayısal tolerans denetimi.
   - `tests/compliance_report.md`: Diferansiyel test sonuç raporu.

5. **Dokümantasyon:**
   - Yaşanan gerçek yanılgıları `HALLUCINATIONS.md` dosyasına kaydet.
   - Token ve iterasyon maliyetlerini `AGENT_COST.md` dosyasına kaydet.
   - Projenin `README.md` dosyasını oluştur.
