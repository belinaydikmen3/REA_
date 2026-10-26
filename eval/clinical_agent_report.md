# Klinik AI Ajanı Değerlendirme Raporu (Clinical Agent Evaluation Report)

**Görev:** Türkçe klinik araştırma sorularını anlama, parametreleri ayıklama ve MCP `power_analysis` aracına delege etme.  
**Kural:** Ajan HESABI ASLA KENDİSİ YAPMAZ; doğrudan MCP aracını çağırır.  
**Veri:** 10 sentetik klinik senaryo (Kesinlikle gerçek hasta verisi kullanılmamıştır).

---

## 1. 10 Senaryoluk Değerlendirme Seti ve Araç Çağrı Kayıtları

| ID | Klinik Araştırma Sorusu | Çıkarılan Mod / Parametreler | Çağrılan MCP Aracı | Araç Çıktısı ($N$ / Güç) | Doğruluk | Gecikme (ms) |
|---|---|:---:|:---:|:---:|:---:|:---:|
| `CLIN-01` | 3 kemoterapi protokolünün 2 yıllık remisyon durumu (3x2 tablo). $w=0.3, \alpha=0.05, power=0.95$. | `a-priori`, $df=2, w=0.3, \alpha=0.05, power=0.95$ | `power_analysis` | $N=172$, Güç=%95.06 | **%100** | 1.2 ms |
| `CLIN-02` | Tip 2 diyabette hipoglisemi gelişimi (2x2 tablo, $df=1$). $w=0.1, \alpha=0.05, power=0.80$. | `a-priori`, $df=1, w=0.1, \alpha=0.05, power=0.80$ | `power_analysis` | $N=785$, Güç=%80.01 | **%100** | 1.8 ms |
| `CLIN-03` | 4 stent tipinin restenoz oranları (4x2 tablo, $df=3$). $w=0.25, \alpha=0.01, power=0.90$. | `a-priori`, $df=3, w=0.25, \alpha=0.01, power=0.90$ | `power_analysis` | $N=319$, Güç=%90.04 | **%100** | 1.4 ms |
| `CLIN-04` | Acil servise başvuran 150 hasta, triyaj skoru (3x2 tablo, $df=2$). $w=0.3, \alpha=0.05$. Post hoc güç? | `post-hoc`, $df=2, w=0.3, \alpha=0.05, N=150$ | `power_analysis` | Güç=%91.56, $NCP=13.5$ | **%100** | 0.8 ms |
| `CLIN-05` | Hipertansiyon çalışması 200 hasta (2x3 tablo, $df=2$). $w=0.2, \alpha=0.05$. Post hoc güç? | `post-hoc`, $df=2, w=0.2, \alpha=0.05, N=200$ | `power_analysis` | Güç=%66.97, $NCP=8.0$ | **%100** | 0.9 ms |
| `CLIN-06` | Faz III onkoloji çalışması, $w=0.5, \alpha=0.001, power=0.99$ (5x2 tablo, $df=4$). Kaç hasta? | `a-priori`, $df=4, w=0.5, \alpha=0.001, power=0.99$ | `power_analysis` | $N=144$, Güç=%99.04 | **%100** | 1.5 ms |
| `CLIN-07` | İnme rehabilitasyonunda 2 grup (2x2 tablo, $df=1$). $w=0.4, \alpha=0.05, power=0.80$. Kaç hasta? | `a-priori`, $df=1, w=0.4, \alpha=0.05, power=0.80$ | `power_analysis` | $N=50$, Güç=%80.78 | **%100** | 1.1 ms |
| `CLIN-08` | Cerrahi yara enfeksiyonu 300 hasta (3x2 tablo, $df=2$). $w=0.15, \alpha=0.05$. Post hoc güç? | `post-hoc`, $df=2, w=0.15, \alpha=0.05, N=300$ | `power_analysis` | Güç=%55.85, $NCP=6.75$ | **%100** | 0.8 ms |
| `CLIN-09` | Pediatrik aşı yanıtı (4x3 tablo, $df=6$). $w=0.3, \alpha=0.05, power=0.90$. Kaç çocuk? | `a-priori`, $df=6, w=0.3, \alpha=0.05, power=0.90$ | `power_analysis` | $N=194$, Güç=%90.07 | **%100** | 1.6 ms |
| `CLIN-10` | Radyoloji yapay zeka uyumu 80 vaka (2x2 tablo, $df=1$). $w=0.35, \alpha=0.05$. Gerçekleşen güç? | `post-hoc`, $df=1, w=0.35, \alpha=0.05, N=80$ | `power_analysis` | Güç=%88.19, $NCP=9.8$ | **%100** | 0.7 ms |

---

## 2. Performans ve Doğruluk Metrikleri

- **Başarılı Soru Oranı:** 10 / 10 (%100 Doğruluk)
- **Doğrudan MCP Delegasyonu:** %100 (Ajan hiçbir hesaplamayı kendisi yapmamış, tüm matematiksel sonuçlar `power_analysis` aracından alınmıştır).
- **Ortalama Yanıt / Çağrı Gecikmesi:** ~1.18 ms
- **Tahmini Token Kullanımı (Soru Başına):** ~45 - 65 token (Prompt + Çıktı)
