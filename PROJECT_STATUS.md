# PROJECT STATUS: YZM301 TEARDOWN SPRINT — K4 CHI-SQUARE CONTINGENCY TABLES

**Tarih:** 26 Ekim 2026  
**Atanan Test Ailesi:** K4 — `chi2-contingency`  
**G*Power Karşılığı:** `χ² tests – Goodness-of-fit tests: Contingency tables`  
**Sorumlu Rol:** Kıdemli Yazılım Mühendisi, İstatistiksel Hesaplama Uzmanı, Tersine Mühendislik Araştırmacısı, Test Mühendisi  
**Çalışma Alanı:** `c:\Users\admin\OneDrive - samsun.edu.tr\Masaüstü\REA`

---

## 1. Ortam ve Araç Envanteri Kontrolü

| Bileşen / Araç | Beklenen | Mevcut Durum | Notlar |
|---|---|---|---|
| **CONTRACT.md** | Bağlayıcı sözleşme | **MEVCUT** (`REA/CONTRACT.md`) | CLI bayrakları, çıktı alanları, toleranslar ve referans vektörleriyle eksiksiz oluşturuldu. |
| **Excel Takım Dağılımı** | Takım ve aile tablosu | **BULUNAMADI** | Yerel disk ve OneDrive üzerinde `.xlsx` tespit edilemedi. Kullanıcı tarafından atanan `K4 chi2-contingency` sabittir. |
| **Mevcut Kaynak Kodlar** | K4 motor ve CLI kodları | **TEMİZ (YOK)** | Temiz oda kuralı gereğince `REA` dizini boştur; bağımsız kod Oturum 2'de yazılacaktır. |
| **Test Dosyaları** | Birim, CLI ve diferansiyel testler | **HENÜZ YOK** | Oturum 1'de spesifikasyon ve test vektörleri hazırlanacak, Oturum 2'de uygulanacaktır. |
| **G*Power 3.1.9.7** | Orijinal ikili dosya ve arayüz | **KURULU DEĞİL** | Sistemde `GPowerNT.exe` bulunamadı. Referanslar akademik kılavuz (Faul et al., 2007) ve açık vektörlerle doğrulanmaktadır. |
| **Python Ortamı** | Python 3.x | **HAZIR** | Python 3.13.14 (`gPower/.venv/Scripts/python.exe`) |
| **SciPy Kütüphanesi** | scipy.stats | **HAZIR** | SciPy 1.18.1 doğrulandı. |
| **pytest Çatısı** | Test koşucu | **HAZIR** | pytest 9.1.1 doğrulandı. |
| **REA MCP Sunucusu** | Tersine mühendislik araçları | **AKTİF (Lazy MCP)** | REA araç seti yüklü ve çağrılabilir durumda. |
| **Ghidra / Java Ortamı** | Decompile motoru | **EKSİK / TANIMSIZ** | `GHIDRA_INSTALL_DIR` ve Java JDK tanımlı değil; decompile uydurulmayacak, gerçek sistem kısıtı olarak belgelendi. |

---

## 2. Sözleşmenin Temel Gereksinimleri (K4 Özeti)

1. **Desteklenecek İki Temel Mod:**
   - **A priori:** `w`, `alpha`, `power`, `df` -> `ncp`, `critical_chi2`, `n_total`, `actual_power`
   - **Post hoc:** `w`, `alpha`, `n_total`, `df` -> `ncp`, `critical_chi2`, `power`
2. **Sayısal Toleranslar:**
   - `n_total` için tam eşleşme (hata = 0).
   - `critical_chi2`, `ncp`, `power` / `actual_power` için mutlak veya bağıl hata $\le 10^{-6}$.
3. **CLI Davranışı:**
   - Çıkış kodu `0`, `stdout` tek satır saf JSON.
   - Hatalı parametrelerde çıkış kodu `2`, standart hata kodları (`MISSING_PARAM`, `UNKNOWN_PARAM`, `INVALID_VALUE`, `OUT_OF_RANGE`, `INCONSISTENT`, `UNSUPPORTED`, `NO_SOLUTION`).
   - İç hatalarda çıkış kodu `1`.
   - `gpower-clone --version` JSON çıktısı.

---

## 3. Uygulama ve İş Planı (Temiz Oda Aşamaları)

### Aşama 1: İnceleme ve Şartname (Oturum 1 — Mevcut Oturum)
- [x] Ortam ve dosya envanterinin çıkarılması (`PROJECT_STATUS.md`).
- [x] Bağlayıcı sözleşmenin teyidi (`CONTRACT.md`).
- [ ] G*Power 3.1.9.7 matematiksel ve mimari davranışının incelenmesi (Ki-kare kontenjans analizi: Faul et al. 2007/2009, Cohen 1988).
- [ ] Kanıt defterinin hazırlanması (`LEDGER.md` — `[DOK]`, `[REA]`, `[AJAN]` etiketleriyle).
- [ ] Gherkin kabul kriterleriyle şartnamenin yazılması (`SPEC.md`).
- [ ] Referans test vektörlerinin ve oracle veritabanının oluşturulması (`oracle/gpower_vectors.csv`).
- [ ] İki oturumun başlangıç prompt'larının hazırlanması (`prompts/session1_first_prompt.md`, `prompts/session2_first_prompt.md`).
- [ ] **Kural:** Oturum 1'de bağımsız motor kodu ve CLI kodları YAZILMAYACAKTIR.

### Aşama 2: Bağımsız Uygulama (Oturum 2)
- [ ] `SPEC.md` ve `CONTRACT.md` girdi alınarak temiz oda motorunun (`src/engine.py`) geliştirilmesi.
- [ ] CLI sarmalayıcısının (`src/cli.py`) ve giriş noktasının (`gpower-clone`) geliştirilmesi.
- [ ] Birim testler (`tests/test_engine.py`, `tests/test_cli.py`) ve diferansiyel testlerin (`tests/differential_test.py`) koşulması.
- [ ] %90+ N eşleşmesinin doğrulanması ve uyumsuzlukların çözülmesi.
- [ ] `compliance_report.md` oluşturulması.

### Aşama 3: Dokümantasyon, Halüsinasyon Takibi ve Bonuslar
- [ ] Yaşanan gerçek halüsinasyonların ve yanılgıların belgelenmesi (`HALLUCINATIONS.md`).
- [ ] Harcanan efor ve model metriklerinin kaydı (`AGENT_COST.md`).
- [ ] `README.md` hazırlanması.
- [ ] MCP ve Klinik Ajan bonus katmanlarının geliştirilmesi.
