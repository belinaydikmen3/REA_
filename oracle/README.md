# Oracle: Referans Veri Seti ve Doğrulama Kılavuzu (K4 chi2-contingency)

Bu dizin, `gpower-clone` motorunun doğrulanması ve diferansiyel testleri için kullanılan referans test vektörlerini ve doğrulama metadatasını içerir.

---

## 1. Dizin Yapısı

- `gpower_vectors.csv`: 39 adet doğrulanmış referans vektörü (A priori, Post hoc ve Sınır/Hata durumları).
- `screenshots/`: G*Power arayüz ekran görüntüleri klasörü.
- `README.md`: Bu açıklama dosyası.

---

## 2. Referans Vektörleri Özeti

| Kategori | Vektör Sayısı | Açıklama |
|---|---|---|
| **Sözleşme Açık Vektörleri** | 2 | `CONTRACT.md` içinde tanımlı K4-REF-01 (a-priori) ve K4-REF-02 (post-hoc) |
| **A Priori Izgara Vektörleri** | 16 | Farklı $w$ (0.05 - 0.8), $\alpha$ (0.001 - 0.10), güç (0.80 - 0.99) ve $df$ (1 - 8) kombinasyonları |
| **Post Hoc Izgara Vektörleri** | 15 | Farklı $w$, $\alpha$, $N$ (40 - 1000) ve $df$ (1 - 6) kombinasyonları |
| **Sınır ve Hata Vektörleri** | 6 | Negatif etki büyüklüğü, geçersiz alfa, kesirli serbestlik derecesi, power <= alpha, yetersiz örneklem |
| **TOPLAM** | **39** | Şartname ve diferansiyel testler için hazır |

---

## 3. Ekran Görüntüleri ve Sistem Durumu Notu

> **Önemli Etik ve Teknik Beyan:**  
> Teardown sprint ortamı denetiminde (`PROJECT_STATUS.md` ve `LEDGER.md` EVD-07 / EVD-13) geliştirme makinesinde G*Power 3.1.9.7 GUI arayüzünün kurulu olmadığı tespit edilmiştir.  
> Temiz oda ve akademik dürüstlük kuralları uyarınca **olmayan ekran görüntüleri sahte veya yapay olarak üretilmemiş**, arayüzden ekran görüntüsü alınmış gibi gösterilmemiştir.  
> Referans vektörler, G*Power'ın yayınlanmış makalesi (Faul et al., 2007, Behavior Research Methods) ve sözleşmedeki açık referans değerleriyle matematiksel olarak tam örtüşen çift duyarlıklı sayısal modelden türetilmiştir.  
> Kullanıcı arzu ederse fiziksel G*Power yazılımından aldığı `.png` ekran görüntülerini `screenshots/` klasörüne ekleyebilir.
