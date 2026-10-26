# SPEC.md: Davranışsal Şartname ve Kabul Kriterleri (K4 chi2-contingency)

Bu belge, `gpower-clone` bağımsız hesaplama motorunun Gherkin formatında yazılmış resmi kabul kriterlerini (acceptance criteria) ve davranışsal spesifikasyonunu içerir.

Tüm senaryolar `LEDGER.md` kanıtlarına ve `CONTRACT.md` sözleşmesine doğrudan bağlıdır.

---

## Özellik 1: A Priori Örneklem Büyüklüğü Hesaplama (`--mode a-priori`)

### Senaryo 1.1: Standart referans girdileri ile gerekli örneklem büyüklüğünün hesaplanması
- **Bağlantılı Kanıt:** `EVD-01`, `EVD-02`, `EVD-03`, `EVD-04`, `EVD-05`
- **Referans Vektörü:** `K4-REF-01`
```gherkin
Feature: Ki-kare testi için a priori örneklem büyüklüğü

Scenario: Standart orta etki büyüklüğü ile örneklem büyüklüğü hesaplama
  Given test ailesi "chi2-contingency"
  And hesaplama modu "a-priori"
  And etki büyüklüğü w 0.3
  And anlamlılık düzeyi alfa 0.05
  And hedef güç 0.95
  And serbestlik derecesi df 5
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 0 olmalıdır
  And stdout tek satır geçerli JSON olmalıdır
  And "n_total" tam olarak 220 olmalıdır
  And "ncp" mutlak veya bağıl farkı 1e-6 dahilinde 19.8 olmalıdır
  And "critical_chi2" mutlak veya bağıl farkı 1e-6 dahilinde 11.0704977 olmalıdır
  And "actual_power" mutlak veya bağıl farkı 1e-6 dahilinde 0.9502155 olmalıdır
```

### Senaryo 1.2: Küçük etki büyüklüğü ve yüksek serbestlik derecesi
- **Bağlantılı Kanıt:** `EVD-04`, `EVD-01`
- **Referans Vektörü:** `K4-AP-02` ($w=0.1, \alpha=0.01, \text{power}=0.80, df=10$)
```gherkin
Scenario: Küçük etki büyüklüğü ile büyük örneklem gereksinimi
  Given test ailesi "chi2-contingency"
  And hesaplama modu "a-priori"
  And etki büyüklüğü w 0.1
  And anlamlılık düzeyi alfa 0.01
  And hedef güç 0.80
  And serbestlik derecesi df 10
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 0 olmalıdır
  And "n_total" tamsayı olmalıdır
  And "actual_power" hedef güç olan 0.80 değerine eşit veya büyük olmalıdır
```

---

## Özellik 2: Post Hoc Güç Analizi (`--mode post-hoc`)

### Senaryo 2.1: Standart referans girdileri ile gerçekleşen test gücünün hesaplanması
- **Bağlantılı Kanıt:** `EVD-01`, `EVD-02`, `EVD-03`, `EVD-06`
- **Referans Vektörü:** `K4-REF-02`
```gherkin
Feature: Ki-kare testi için post hoc güç analizi

Scenario: Verilen örneklem büyüklüğü ile gerçekleşen gücü hesaplama
  Given test ailesi "chi2-contingency"
  And hesaplama modu "post-hoc"
  And etki büyüklüğü w 0.3
  And anlamlılık düzeyi alfa 0.05
  And toplam örneklem büyüklüğü n_total 100
  And serbestlik derecesi df 5
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 0 olmalıdır
  And stdout tek satır geçerli JSON olmalıdır
  And "ncp" mutlak veya bağıl farkı 1e-6 dahilinde 9.0 olmalıdır
  And "critical_chi2" mutlak veya bağıl farkı 1e-6 dahilinde 11.0704977 olmalıdır
  And "power" mutlak veya bağıl farkı 1e-6 dahilinde 0.6235846 olmalıdır
```

### Senaryo 2.2: Büyük örneklem büyüklüğünde güç doygunluğu
- **Bağlantılı Kanıt:** `EVD-14`
- **Referans Vektörü:** `K4-PH-03` ($w=0.5, \alpha=0.05, n\_total=500, df=2$)
```gherkin
Scenario: Yüksek etki ve yeterli örneklemde yüksek güç elde edilmesi
  Given test ailesi "chi2-contingency"
  And hesaplama modu "post-hoc"
  And etki büyüklüğü w 0.5
  And anlamlılık düzeyi alfa 0.05
  And toplam örneklem büyüklüğü n_total 500
  And serbestlik derecesi df 2
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 0 olmalıdır
  And "power" 0.9999 değerinden büyük olmalıdır
```

---

## Özellik 3: Girdi Doğrulama ve Hata Yönetimi

### Senaryo 3.1: Zorunlu parametrenin eksik olması
- **Bağlantılı Kanıt:** `EVD-13`
```gherkin
Feature: Girdi doğrulama ve hata yönetimi

Scenario: A priori modunda power parametresinin eksik verilmesi
  Given test ailesi "chi2-contingency"
  And hesaplama modu "a-priori"
  And etki büyüklüğü w 0.3
  And alfa 0.05
  And serbestlik derecesi df 5
  But hedef güç "power" parametresi verilmediğinde
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 2 olmalıdır
  And stdout JSON çıktısı "code": "MISSING_PARAM" içermelidir
  And "field": "power" belirtilmelidir
```

### Senaryo 3.2: Bilinmeyen veya modla ilgisiz parametre verilmesi
- **Bağlantılı Kanıt:** `EVD-13`
```gherkin
Scenario: Post hoc modunda n_total yerine alakasız tails parametresi verilmesi
  Given test ailesi "chi2-contingency"
  And hesaplama modu "post-hoc"
  And geçersiz bayrak "--tails 2" sağlandığında
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 2 olmalıdır
  And stdout JSON çıktısı "code": "UNKNOWN_PARAM" içermelidir
```

### Senaryo 3.3: Kesirli serbestlik derecesi (df) verilmesi
- **Bağlantılı Kanıt:** `EVD-10`
```gherkin
Scenario: Kesirli serbestlik derecesi girilmesi
  Given test ailesi "chi2-contingency"
  And hesaplama modu "a-priori"
  And serbestlik derecesi df "1.5" olarak verildiğinde
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 2 olmalıdır
  And stdout JSON çıktısı "code": "INVALID_VALUE" içermelidir
  And "field": "df" belirtilmelidir
```

### Senaryo 3.4: Örneklem büyüklüğünün 2'den küçük olması
- **Bağlantılı Kanıt:** `EVD-11`
```gherkin
Scenario: n_total değerinin 1 olarak girilmesi
  Given test ailesi "chi2-contingency"
  And hesaplama modu "post-hoc"
  And n_total 1 olarak verildiğinde
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 2 olmalıdır
  And stdout JSON çıktısı "code": "OUT_OF_RANGE" içermelidir
  And "field": "n_total" belirtilmelidir
```

### Senaryo 3.5: Gücün alfadan küçük veya eşit olması
- **Bağlantılı Kanıt:** `EVD-09`
```gherkin
Scenario: Hedef gücün alfadan küçük olması
  Given test ailesi "chi2-contingency"
  And hesaplama modu "a-priori"
  And alfa 0.05
  And hedef güç 0.04 olarak verildiğinde
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 2 olmalıdır
  And stdout JSON çıktısı "code": "INCONSISTENT" içermelidir
```

### Senaryo 3.6: Desteklenmeyen test ailesi veya mod girilmesi
- **Bağlantılı Kanıt:** `EVD-13`
```gherkin
Scenario: Desteklenmeyen test ailesi talep edilmesi
  Given test ailesi "t2-indep" sağlandığında
  When gpower-clone CLI komutu çalıştırıldığında
  Then çıkış kodu 2 olmalıdır
  And stdout JSON çıktısı "code": "UNSUPPORTED" içermelidir
```

---

## Özellik 4: Deterministik Çalışma ve Sayısal Hassasiyet

### Senaryo 4.1: Aynı girdilerle ardışık çağrılarda özdeş sonuçlar üretilmesi
- **Bağlantılı Kanıt:** `EVD-12`
```gherkin
Feature: Deterministik çalışma

Scenario: Ardışık iki a priori çağrısında bit düzeyinde özdeş JSON çıktısı
  Given geçerli bir a priori girdi seti
  When komut 1. kez çalıştırıldığında alınan JSON çıktısı
  And komut 2. kez çalıştırıldığında alınan JSON çıktısı
  Then iki çıktı karakteri karakterine özdeş olmalıdır
```

---

## Özellik 5: Sürüm Bilgisi Arayüzü

### Senaryo 5.1: Sürüm bilgisinin standart JSON formatında alınması
- **Bağlantılı Kanıt:** `CONTRACT.md` Bölüm 5
```gherkin
Feature: CLI sürüm arayüzü

Scenario: gpower-clone --version komutunun çalıştırılması
  When "gpower-clone --version" komutu çalıştırıldığında
  Then çıkış kodu 0 olmalıdır
  And stdout {"name":"gpower-clone","test_family":"chi2-contingency","version":"1.0.0","team":"K4"} JSON nesnesi olmalıdır
```
