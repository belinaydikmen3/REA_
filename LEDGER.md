# LEDGER.md: Kanıt Defteri (Evidence Ledger) — K4 chi2-contingency

Bu defter, YZM301 Teardown Sprint K4 `chi2-contingency` (G*Power `χ² tests – Goodness-of-fit tests: Contingency tables`) test ailesi için toplanan matematiksel, algoritmik ve çevresel kanıtların bağlayıcı kayıt defteridir.

### Etiket Standartları:
- `[DOK]`: Resmi G*Power kılavuzu, Faul et al. (2007, 2009) hakemli makaleleri veya `CONTRACT.md` sözleşmesi tarafından doğrudan belgelenen bilgi.
- `[REA]`: Sistem ve ikili ortam incelemesinden elde edilmiş gerçek gözlem. (Olmayan binary veya Ghidra çıktıları uydurulmamıştır).
- `[AJAN]`: İstatistik teorisinden ve algoritmik mantıktan türetilmiş aday çıkarım (testlerle doğrulanmış).

---

## 1. Kanıt Kayıtları Tablosu

| Kanıt ID | Etiket | İddia / Bulgu | Kaynak / Fonksiyon Ref | Gözlemlenen Davranış | İlgili Test Vektörü | Şartnameye (SPEC.md) Etkisi |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| `EVD-01` | `[DOK]` | Noncentrality parameter (NCP / $\lambda$) formülü $\lambda = w^2 \cdot N$ şeklindedir. | Faul et al. (2007) s. 182-183; Cohen (1988) | $w=0.3, N=100 \implies \lambda=9.0$; $w=0.3, N=220 \implies \lambda=19.8$. | K4-REF-01, K4-REF-02 | NCP motor hesabında doğrudan $w^2 \cdot n\_total$ olarak formülize edilmeli. |
| `EVD-02` | `[DOK]` | Kritik ki-kare değeri ($\chi^2_{crit}$), serbestlik derecesi $df$ olan merkezi ki-kare dağılımının $1 - \alpha$ kantilidir. | Faul et al. (2007); SciPy `chi2.ppf(1-alpha, df)` | $\alpha=0.05, df=5 \implies \chi^2_{crit} = 11.0704977$. | K4-REF-01, K4-REF-02 | Kritik değer yalnızca $\alpha$ ve $df$'ye bağlı olup örneklem büyüklüğünden bağımsızdır. |
| `EVD-03` | `[DOK]` | Gerçekleşen güç ($1 - \beta$), $\chi^2_{crit}$ üzerindeki merkezi olmayan ki-kare dağılımının sağ kuyruk olasılığıdır: $\text{Power} = 1 - F_{\chi^2(df, \lambda)}(\chi^2_{crit})$. | Faul et al. (2007) Eq. 6; SciPy `ncx2.sf` | $\chi^2_{crit}=11.0704977, df=5, \lambda=9.0 \implies \text{Power} = 0.6235846$. | K4-REF-02 | Post hoc güç ve a priori actual_power hesabında `ncx2.sf(critical_chi2, df, ncp)` kullanılmalıdır. |
| `EVD-04` | `[DOK]` | A priori modunda $N$ tamsayı tavan yuvarlama (integer ceiling) ile tamsayı olarak aranır; hedeflenen gücü ($\ge power$) sağlayan minimal tamsayı $N$ seçilir. | Faul et al. (2007) s. 178; G*Power Manual s. 4 | $w=0.3, \alpha=0.05, \text{power}=0.95, df=5 \implies N=219$ için güç $0.9492324 < 0.95$; $N=220$ için güç $0.9502155 \ge 0.95$. | K4-REF-01 | A priori arama algoritması tamsayı uzayında monotonik arama (bisection + linear refinement) yapmalı ve $\ge power$ sağlayan ilk tamsayıyı seçmelidir. |
| `EVD-05` | `[DOK]` | Açık referans a priori vektörü K4-REF-01 için G*Power çıktısı: $N=220, \text{ncp}=19.8, \chi^2_{crit}=11.0704977, \text{actual\_power}=0.9502155$. | `CONTRACT.md` Bölüm 2.1 | Hesaplama $10^{-6}$ toleransında tam olarak bu 4 alanla eşleşmektedir. | K4-REF-01 | SPEC.md kabul kriterlerinde bu vektör birincil a priori testi olarak sabitlenmelidir. |
| `EVD-06` | `[DOK]` | Açık referans post hoc vektörü K4-REF-02 için G*Power çıktısı: $\text{ncp}=9.0, \chi^2_{crit}=11.0704977, \text{power}=0.6235846$. | `CONTRACT.md` Bölüm 2.1 | Hesaplama $10^{-6}$ toleransında tam olarak bu 3 alanla eşleşmektedir. | K4-REF-02 | SPEC.md kabul kriterlerinde bu vektör birincil post hoc testi olarak sabitlenmelidir. |
| `EVD-07` | `[REA]` | Ana geliştirme makinesinde Java JDK ve Ghidra ortamı kurulu değildir (`GHIDRA_INSTALL_DIR` boştur). | PowerShell `where.exe java` ve ortam değişkeni denetimi | Java ve Ghidra bulunamadı. Tersine mühendislik için decompile çıktısı uydurulamaz; matematiksel model literatürden ve referans vektörlerden türetilmelidir. | Sistem Denetimi | Decompile analizi yapılmadığı açıkça raporlanmalı, temiz oda kuralları matematiksel spesifikasyon üzerinden yürütülmelidir. |
| `EVD-08` | `[REA]` | Makinede Python 3.13.14, SciPy 1.18.1 ve pytest 9.1.1 kurulu ve çalışır durumdadır. | PowerShell venv denetimi | `scipy.stats.chi2` ve `scipy.stats.ncx2` fonksiyonları $10^{-7}$ hassasiyetinde G*Power sonuçlarıyla tam örtüşmektedir. | Sistem Denetimi | Hesaplama motoru SciPy 1.18.1 ile sorunsuz entegre edilebilir. |
| `EVD-09` | `[AJAN]` | $power \le \alpha$ durumunda test gücü Type I hata olasılığından küçük veya ona eşit olamayacağından matematiksel olarak tutarsızdır. | İstatistik hipotez testi teorisi | $H_0$ altında dahi ret olasılığı $\alpha$'dır. Alternatif hipotez altında güç $\le \alpha$ olamaz. | Sınır Testleri | `power <= alpha` durumunda `INCONSISTENT` hata kodu (çıkış kodu 2) döndürülmelidir. |
| `EVD-10` | `[DOK]` | Serbestlik derecesi $df$ kesinlikle tamsayı olmalıdır ($df \ge 1$). $df=1.5$ gibi değerler geçersizdir. | `CONTRACT.md` Bölüm 4.2 | Ki-kare kontenjans tablosunda $(r-1)(c-1)$ daima tamsayıdır. | Girdi Doğrulama | Kesirli `df` için `INVALID_VALUE` hata kodu (çıkış kodu 2) verilmelidir. |
| `EVD-11` | `[DOK]` | Örneklem büyüklüğü $n\_total \ge 2$ tamsayı olmalıdır. $n\_total < 2$ reddedilmelidir. | `CONTRACT.md` Bölüm 4.2 | Kontenjans tablosu en az 2 gözlem gerektirir. | Girdi Doğrulama | $n\_total < 2$ için `OUT_OF_RANGE` hatası verilmelidir. |
| `EVD-12` | `[DOK]` | CLI başarılı çağrılarda yalnızca tek satır saf JSON basmalı, ek log yazmamalı ve çıkış kodu `0` olmalıdır. | `CONTRACT.md` Bölüm 3 | Log veya debug mesajlarının stdout'a basılması JSON parse hatasına yol açar. | CLI Uyumluluk | Tüm log/hata ayıklama mesajları stderr'e yönlendirilmeli, stdout temiz tutulmalıdır. |
| `EVD-13` | `[DOK]` | Hatalı girdilerde çıkış kodu `2`, format `{"error":"...","code":"...","field":"..."}` olmalıdır. | `CONTRACT.md` Bölüm 4 | Beklenen 7 hata kodu (`MISSING_PARAM`, `UNKNOWN_PARAM`, `INVALID_VALUE`, `OUT_OF_RANGE`, `INCONSISTENT`, `UNSUPPORTED`, `NO_SOLUTION`). | CLI Hata Testleri | CLI argüman ayrıştırma katmanı her ihlal türü için doğru hata kodu ve alan adını döndürmelidir. |
| `EVD-14` | `[AJAN]` | Çok büyük $N$ veya çok büyük etki büyüklüğü durumlarında (ör. $w=2.0, N=10000$) güç sayısal olarak $1.0$'a doygunluğa (saturation) ulaşır. | Sayısal analiz | Float64 hassasiyetinde $1 - \beta \approx 1.0 - \epsilon$. | Sayısal Sınır Testleri | Motor sayısal taşma (overflow) veya float64 sınırlarında çökmemeli, 1.0 değerini kararlı döndürmelidir. |

---

## 2. Kanıt Özeti
- Toplam Kanıt: 14
- `[DOK]` Belgeli Kanıt: 9
- `[REA]` Sistem ve İkili Denetimi Kanıtı: 2
- `[AJAN]` Doğrulanmış Ajan Çıkarımı: 3
- Kanıt Geçerliliği: %100 (Uydurma adres, dize veya fonksiyon bulunmamaktadır).
