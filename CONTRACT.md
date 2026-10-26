# CONTRACT: YZM301 Teardown Sprint — Test Ailesi K4 (`chi2-contingency`)

Bu belge, YZM301 Teardown Sprint kapsamında `gpower-clone` bağımsız hesaplama motoru ve CLI arayüzünün bağlayıcı teknik sözleşmesidir.

---

## 1. Test Ailesi Tanımı

- **Aile Kodu:** `K4`
- **CLI Test Parametresi:** `--test chi2-contingency`
- **G*Power Karşılığı:** `χ² tests` -> `Goodness-of-fit tests: Contingency tables`
- **İstatistiksel Kapsam:** Kontenjans tablolarında uyum iyiliği / bağımsızlık testi (Chi-Square Goodness-of-fit / Contingency Tables).
- **Klinik Kullanım Senaryosu:** Çoklu tedavi gruplarının klinik yanıt/iyileşme oranları arasındaki farkların incelenmesi ve çalışma öncesi/sonrası örneklem analizi.

---

## 2. CLI Arayüzü ve Çağrı Sözleşmesi

Komut adı: `gpower-clone`

### 2.1 Desteklenen Modlar

#### Mod 1: A Priori (`--mode a-priori`)
Hedeflenen istatistiksel güç (`power`) için gereken toplam örneklem büyüklüğünü (`n_total`) hesaplar.

- **Zorunlu Parametreler:**
  - `--test chi2-contingency`
  - `--mode a-priori`
  - `--w <float>`: Cohen'in etki büyüklüğü ($w > 0$)
  - `--alpha <float>`: Tip I hata olasılığı ($0 < \alpha < 1$)
  - `--power <float>`: Hedef güç ($0 < 1-\beta < 1$)
  - `--df <int>`: Serbestlik derecesi ($df \ge 1$, tam sayı)

- **Başarılı Çıktı Formatı (stdout, tek satır JSON):**
  ```json
  {"ncp":19.8,"critical_chi2":11.0704977,"n_total":220,"actual_power":0.9502155}
  ```

- **Açık Referans Test Vektörü (K4-REF-01):**
  - Girdi: `gpower-clone --test chi2-contingency --mode a-priori --w 0.3 --alpha 0.05 --power 0.95 --df 5`
  - Beklenen Çıktı: `{"ncp":19.8,"critical_chi2":11.0704977,"n_total":220,"actual_power":0.9502155}`

#### Mod 2: Post Hoc (`--mode post-hoc`)
Verilen toplam örneklem büyüklüğü (`n_total`) ile ulaşılan test gücünü (`power`) hesaplar.

- **Zorunlu Parametreler:**
  - `--test chi2-contingency`
  - `--mode post-hoc`
  - `--w <float>`: Cohen'in etki büyüklüğü ($w > 0$)
  - `--alpha <float>`: Tip I hata olasılığı ($0 < \alpha < 1$)
  - `--n_total <int>`: Toplam örneklem büyüklüğü ($N \ge 2$, tam sayı)
  - `--df <int>`: Serbestlik derecesi ($df \ge 1$, tam sayı)

- **Başarılı Çıktı Formatı (stdout, tek satır JSON):**
  ```json
  {"ncp":9.0,"critical_chi2":11.0704977,"power":0.6235846}
  ```

- **Açık Referans Test Vektörü (K4-REF-02):**
  - Girdi: `gpower-clone --test chi2-contingency --mode post-hoc --w 0.3 --alpha 0.05 --n_total 100 --df 5`
  - Beklenen Çıktı: `{"ncp":9.0,"critical_chi2":11.0704977,"power":0.6235846}`

---

## 3. Sayısal Toleranslar ve Doğrulama Kuralları

1. **Örneklem Büyüklüğü (`n_total`):**
   - Tam eşleşme zorunludur. Kesirli örneklem kabul edilmez; tamsayı olmalıdır.
   - Fark = $0$.

2. **Kritik Değer (`critical_chi2`), NCP (`ncp`), Güç (`power` / `actual_power`):**
   - Mutlak hata: $|x_{hesap} - x_{ref}| \le 10^{-6}$ VEYA
   - Bağıl hata: $\frac{|x_{hesap} - x_{ref}|}{|x_{ref}|} \le 10^{-6}$

3. **Çıktı Biçimi:**
   - Standart çıktı (`stdout`) yalnızca tek satır saf JSON içermelidir.
   - Sayısal değerler JSON number türünde, double hassasiyetinde serialize edilmelidir. Keyfî yuvarlama yapılmamalıdır.
   - Başarı durumunda çıkış kodu: `0`.

---

## 4. Hata Yönetimi ve Çıkış Kodları

Geçersiz veya sözleşmeye uymayan çağrılarda program tek satır hata JSON'u basmalı ve uygun çıkış kodu ile sonlanmalıdır:

- **Hatalı Girdi / Sözleşme İhlali:** Çıkış kodu `2`
- **İç Sistem Hatası:** Çıkış kodu `1`

### 4.1 Hata Çıktı Formatı
```json
{"error":"Açıklama mesajı","code":"HATA_KODU","field":"ilgili_alan"}
```

### 4.2 Standart Hata Kodları

| Hata Kodu | Anlamı | Tetiklenme Durumu |
|---|---|---|
| `MISSING_PARAM` | Zorunlu parametre eksik | Mod için gereken zorunlu bir argüman sağlanmamış |
| `UNKNOWN_PARAM` | Bilinmeyen / modla ilgisiz parametre | Sözleşmede olmayan veya o modda beklenmeyen bir bayrak verilmiş |
| `INVALID_VALUE` | Tip / format hatası | Ondalık yerine metin girilmesi, ondalık ayırıcı virgül olması, `df` veya `n_total` için kesirli sayı verilmesi, `NaN` / `Infinity` |
| `OUT_OF_RANGE` | Değer aralık dışı | $w \le 0$, $\alpha \le 0$ veya $\ge 1$, $power \le 0$ veya $\ge 1$, $df < 1$, $n\_total < 2$ |
| `INCONSISTENT` | Parametreler mantıksal uyumsuz | $power \le \alpha$ gibi anlamsız/tutarsız kombinasyonlar |
| `UNSUPPORTED` | Desteklenmeyen test veya mod | `chi2-contingency` dışında test veya `a-priori`/`post-hoc` dışında mod istenmesi |
| `NO_SOLUTION` | Çözüm bulunamadı | A priori aramasında sayısal yakınsama sağlanamaması |

---

## 5. Sürüm Bilgisi Sözleşmesi

`gpower-clone --version` çağrıldığında çıkış kodu `0` olmalı ve stdout üzerinde şu JSON basılmalıdır:
```json
{"name":"gpower-clone","test_family":"chi2-contingency","version":"1.0.0","team":"K4"}
```
