# HALLUCINATIONS.md: Doğrulama Sürecinde Yaşanan Yanılgılar ve Düzeltmeler

Bu belge, YZM301 Teardown Sprint K4 `chi2-contingency` projesinde yapay zeka ajanı tarafından başlangıçta doğru kabul edilen, ancak yapılan deneysel ve sistemsel testlerle çürütülerek düzeltilen **gerçek teknik yanılgıları** kayıt altına alır.

---

## Yanılgı Kaydı 1: Ghidra/REA Decompile Motorunun Ortamda Hazır Olduğu Varsayımı

- **İlk İddia:**  
  Ajan, sistemde aktif REA MCP sunucusu ve Masaüstünde `gPower` adında bir klasör gördüğü için, yerel ortamda Ghidra decompile motorunun ve G*Power ikili dosyasının hazır olduğunu ve binary analizi yapılabileceğini varsaydı.
- **Neden Doğru Görünüyordu?**  
  Antigravity IDE yapılandırmasında `rea` lazy MCP araçları (200+ adet) eksiksiz kayıtlıydı. Masaüstünde daha önceki t-testi ödevine ait `gPower` dizini mevcuttu. Bu durum ortamın tam kurulu olduğunu düşündürdü.
- **Nasıl Doğrulandı?**  
  Ortam envanteri çıkarılırken PowerShell üzerinden Java (`where.exe java`), Ghidra dizini (`$env:GHIDRA_INSTALL_DIR`) ve `GPower.exe` arandı.
- **Hangi Kanıtla Çelişti / Neden Kanıtlanamadı?**  
  `where.exe java` boş döndü, `GHIDRA_INSTALL_DIR` ortam değişkeni tanımsızdı ve diskte `GPower.exe` bulunamadı. REA sunucusu Ghidra olmadan yerel C/C++ ikililerini decompile edememekteydi.
- **Hangi Test / İnceleme Yakaladı?**  
  `PROJECT_STATUS.md` aşamasındaki ortam envanteri doğrulaması ve `LEDGER.md` EVD-07 / EVD-14 incelemesi.
- **Nasıl Düzeltildi?**  
  Yapay zeka ajanı hiçbir sahte decompilation çıktısı, sanal PE dizesi veya sahte bellek adresi uydurmadı (`[REA]` etiketi uydurma veriler için kullanılmadı). Decompile motorunun eksikliği dürüstçe raporlandı. Temiz oda metodolojisi gereğince hesaplama mantığı resmi hakemli akademik yayınlar (Faul et al., 2007; Cohen, 1988) ve `CONTRACT.md` açık referans vektörleri temel alınarak yapılandırıldı.

---

## Yanılgı Kaydı 2: Windows Subprocess CLI Çıktısının Varsayılan UTF-8 ile Çakışmayacağı Varsayımı

- **İlk İddia:**  
  CLI katmanında hata mesajlarının Türkçe metinle ve `json.dumps(..., ensure_ascii=False)` ile stdout'a yazılmasının, `subprocess.run(..., text=True, encoding="utf-8")` kullanan test koşucularında sorunsuz çalışacağı varsayıldı.
- **Neden Doğru Görünüyordu?**  
  Python 3 varsayılan olarak Unicode destekler. Linux ve macOS ortamlarında UTF-8 standart terminal çıktısıdır.
- **Nasıl Doğrulandı?**  
  Tüm CLI testlerini içeren `pytest tests/ -v` ilk kez çalıştırıldığında testler yürütüldü.
- **Hangi Kanıtla Çelişti / Hangi Test Yakaladı?**  
  `tests/test_cli.py` içerisindeki 5 test (`test_cli_unsupported_test`, `test_cli_unsupported_mode`, `test_cli_invalid_value_fractional_df`, `test_cli_out_of_range_n_total`, `test_cli_inconsistent_power`) şu hata ile çöktü:
  ```
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfd in position 55: invalid start byte
  AttributeError: 'NoneType' object has no attribute 'strip'
  ```
  Windows konsolunun varsayılan OEM kod sayfasının (cp1254/cp857) Türkçe `ı, ğ, ü, ş` karakterlerini tek baytlık ANSI olarak bastığı ve `utf-8` okuyucusunun kilitlendiği görüldü.
- **Nasıl Düzeltildi?**  
  1. `src/cli.py` içerisinde JSON serileştirme standardı `json.dumps(..., ensure_ascii=True)` olarak güncellendi. Bu sayede tüm Unicode karakterler RFC 8259 standartlarına uygun olarak `\uXXXX` formatında güvenli ASCII haline getirildi.
  2. `sys.stdout.reconfigure(encoding="utf-8")` çağrısı eklendi.
  3. `tests/test_cli.py` içinde subprocess çağrısına `PYTHONIOENCODING=utf-8` ve `errors="replace"` eklendi.
  Rapor: Düzeltme sonrası testler yeniden koşturulduğunda 57/57 testin tamamı (%100) başarıyla geçti.
