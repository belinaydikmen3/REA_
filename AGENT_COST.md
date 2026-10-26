# AGENT_COST.md: Yapay Zeka Ajanı Efor, Araç ve Maliyet Analizi

Bu belge, YZM301 Teardown Sprint K4 `chi2-contingency` projesinde kullanılan yapay zeka modelleri, harcanan iterasyon sayısı, kullanılan araçlar ve kaynak kullanımının şeffaf dökümüdür.

---

## 1. Model ve Oturum Bilgileri

| Parametre | Değer / Açıklama |
|---|---|
| **Ajan / Ortam** | Antigravity AI Coding Assistant (Google DeepMind Advanced Agentic Coding) |
| **Kullanılan Model** | Gemini 3.8 Flash (Medium) / Gemini 2.5 Flash |
| **Oturum Sayısı** | 2 Oturum (Temiz Oda: 1. İnceleme & Şartname, 2. Bağımsız Uygulama) |
| **Toplam Görev İterasyonu** | ~28 Araç Çağrısı (Tool Calls) |
| **Ölçülen Token Kullanımı** | Antigravity IDE API doğrudan harici token faturasını yansıtmadığından token sayısı **ölçülmemiş** olarak kaydedilmiştir. Tahmini toplam bağlam işleme: ~120.000 - 160.000 token. |
| **Finansal Maliyet** | Öğrenci/Geliştirici hesabı kapsamında doğrudan maliyet 0$ (Ölçülmemiş harici API maliyeti uydurulmamıştır). |

---

## 2. Kullanılan Araçlar (Tooling)

1. **`run_command` (PowerShell / Windows CMD):**
   - Disk ve ortam taraması (GPower, Java, Ghidra, Python, SciPy, pytest denetimi).
   - `.venv` sanal ortamı oluşturma ve bağımlılık kurulumu (`pip install scipy pytest -e .`).
   - CLI komut satırı testleri ve çıkış kodu (`$LASTEXITCODE` / `%ERRORLEVEL%`) denetimi.
   - pytest test koşuları.
2. **`write_to_file`:**
   - Şartname, sözleşme, motor, CLI ve test dosyalarının oluşturulması ve güncellenmesi.
3. **`list_dir` / `view_file`:**
   - Dizin yapısı, dosya boyutu ve şema incelemeleri.
4. **`manage_task`:**
   - Arka planda çalışan uzun süreli komutların (paket yükleme, tam test koşuları) asenkron yönetimi.

---

## 3. Başarısız Denemeler ve Giderilen Sorunlar

1. **PowerShell İçi Tırnak ve Dize Ayrıştırma Hataları:**
   - PowerShell `run_command` üzerinden `python -c "import scipy; ..."` çağrılırken iç içe çift tırnakların PowerShell tarafından yutulması nedeniyle SyntaxError alındı.
   - *Çözüm:* Kodlar geçici `scratch/` scriptlerine yazılarak doğrudan çalıştırıldı.
2. **Subprocess UnicodeDecodeError (Windows Türkçe Karakterler):**
   - Windows konsolunda `ı, ğ, ü` gibi karakterler içeren hata çıktılarının `subprocess.run(..., encoding='utf-8')` ile okunmasında çökme yaşandı.
   - *Çözüm:* `src/cli.py` içerisinde `json.dumps(..., ensure_ascii=True)` standardına geçildi ve stdout akışı yeniden yapılandırıldı.
3. **Pytest PYTHONPATH Eksikliği:**
   - `pytest tests/ -v` ilk çağrıda `src` paketini root olarak göremedi.
   - *Çözüm:* `pyproject.toml` içerisine `[tool.pytest.ini_options] pythonpath = ["."]` tanımı eklendi.

---

## 4. Gelecekte İyileştirilecek Adımlar

1. **MCP Bonus Katmanı:**
   - CLI'ya ek olarak tek motoru kullanan bir Model Context Protocol (MCP) `power_analysis` aracı ve klinik AI ajanı eklenmesi.
2. **Web Arayüzü:**
   - Araştırmacılar için hızlı görsel analiz sağlayan yerel bir web arayüzü (HTML/JS/Canvas) prototipi.
3. **Çoklu Platform CI/CD:**
   - Linux, macOS ve Windows üzerinde GitHub Actions ile test matrisinin otomatik koşturulması.
