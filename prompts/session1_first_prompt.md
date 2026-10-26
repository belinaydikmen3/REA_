# Oturum 1: İnceleme ve Şartname (Reverse Engineering & Specification) Başlangıç Promptu

**Proje:** YZM301 Teardown Sprint  
**Test Ailesi:** K4 — `chi2-contingency` (G*Power: `χ² tests – Goodness-of-fit tests: Contingency tables`)  
**Görev Kapsamı:** İkili ve ortam incelemesi, literatür ve matematiksel modelleme, kanıt defteri (`LEDGER.md`), kabul kriterleri (`SPEC.md`) ve referans oracle veri seti (`oracle/gpower_vectors.csv`) üretimi.  
**Kısıtlama:** Kesinlikle bağımsız hesaplama motoru ve CLI kaynak kodları bu oturumda YAZILMAYACAKTIR.

---

## Talimatlar

Sen bir kıdemli tersine mühendislik uzmanı, istatistiksel hesaplama araştırmacısı ve sistem mimarısın. Aşağıdaki adımları sırasıyla yerine getir:

1. **Ortam ve Sözleşme Denetimi:**
   - `CONTRACT.md` dosyasını oku. CLI arayüzü, parametre adları, hata kodları ve sayısal toleransları doğrula.
   - Geliştirme ortamındaki araçları (Python, SciPy, pytest, G*Power, Ghidra, REA) denetle ve mevcut durumu `PROJECT_STATUS.md` dosyasına kaydet.
   - Mevcut olmayan araçları (ör. Ghidra, Java, kurulu G*Power) var gibi gösterme; eksiklikleri dürüstçe raporla.

2. **Matematiksel Davranış ve İnceleme:**
   - Ki-kare kontenjans analizinin matematiksel temelini (Faul et al., 2007; Cohen, 1988) çıkar.
   - Noncentrality parameter ($\lambda = w^2 \cdot N$), kritik ki-kare değeri ($F_{\chi^2(df)}^{-1}(1-\alpha)$), güç ($1 - F_{\chi^2(df,\lambda)}(\chi^2_{crit})$) ve tamsayı örneklem arama kurallarını kesinleştir.
   - Sözleşmedeki açık referans vektörleriyle bu ilişkileri doğrula.

3. **Kanıt Defteri (LEDGER.md):**
   - Her bulguyu `[DOK]`, `[REA]` veya `[AJAN]` etiketiyle kaydet.
   - REA kanıtı yoksa `[REA]` yazma. Hiçbir bellek adresi, PE dizesi veya fonksiyon uydurma.

4. **Davranışsal Şartname (SPEC.md):**
   - Gözlemlenen davranışı Gherkin kabul kriterleriyle yaz (`Given / When / Then`).
   - A priori, post hoc, geçersiz parametreler, sınır durumları ve deterministik çalışma senaryolarını ekle.

5. **Oracle ve Devir:**
   - En az 30 doğrulanmış test vektörünü `oracle/gpower_vectors.csv` dosyasına yaz.
   - İkinci oturum için temiz oda devir prompt'unu (`prompts/session2_first_prompt.md`) oluştur ve çalışmayı Oturum 2'ye devret.
