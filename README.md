# BERTürk Tabanlı Türkçe Elektrik Ürünlerinin Otomatik Sınıflandırılması

Türkçe e-ticaret platformlarından toplanan elektrik/elektroteknik ürün adlarının BERTürk (`dbmdz/bert-base-turkish-cased`) fine-tuning yöntemiyle otomatik kategorize edilmesi üzerine TÜBİTAK 2209-A kapsamında desteklenen bitirme çalışması.

Bu repo, ilgili akademik makalenin **veri ve kod erişilebilirliği** beyanı kapsamında paylaşılmaktadır.

## Proje Özeti

- **Veri**: 4 e-ticaret platformundan (Trendyol, Amazon, elektrikmarket.com.tr, e-dundar.com) web scraping ile toplanan 11.160 ürün, 20 kategori
- **Model**: `dbmdz/bert-base-turkish-cased` fine-tuning, %92,5 test doğruluğu
- **Servis**: FastAPI REST API ile gerçek zamanlı kategori tahmini

## Eğitilmiş Model

Eğitilmiş model dosyaları (`model.safetensors`, tokenizer, config) boyut nedeniyle bu repoda **değil**, Hugging Face Hub'da barındırılmaktadır:

👉 **[HUGGINGFACE-LINKI-BURAYA-GELECEK]**

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
tokenizer = AutoTokenizer.from_pretrained("KULLANICI_ADI/MODEL_ADI")
model = AutoModelForSequenceClassification.from_pretrained("KULLANICI_ADI/MODEL_ADI")
```

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `scraper.py` | elektrikmarket.com.tr veri toplama betiği |
| `scraper2.py` | e-dundar.com veri toplama betiği (site taksonomisi tabanlı etiketleme) |
| `scraper3.py` | trendyol.com veri toplama betiği (arama sorgusu tabanlı etiketleme) |
| `scraper4.py` | amazon.com.tr veri toplama betiği (arama sorgusu tabanlı etiketleme) |
| `hafta1.py` | Ham veri (Excel) okuma |
| `hafta2.py` | Regex tabanlı teknik öznitelik çıkarımı (güç, renk sıcaklığı, duy, ışık rengi) |
| `hafta3.py` | Etiketleme ve `etiketli_veri.json` oluşturma, BERTürk tokenizer testi |
| `veri_birlestir.py` | Tüm kaynakların birleştirilmesi ve tekilleştirme |
| `hafta4.py` | BERTürk fine-tuning (3 epoch), classification report ve confusion matrix |
| `kontrol.py` | Kategori-indeks eşleşmesinin kontrolü |
| `yanlis.py` | Yanlış sınıflandırılan ürünlerin incelenmesi (hata analizi) |
| `api.py` | FastAPI REST servisi (`/predict` endpoint) |
| `test_api.py` | API test betiği |
| `rapor.py` | Sonuç raporlama yardımcı betiği |
| `oku_log.py` | Eğitim log dosyalarının okunması |
| `etiketli_veri.json` | Tam etiketli veri seti (11.160 ürün, 20 kategori) |

## Kurulum

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install torch transformers fastapi uvicorn pydantic pandas scikit-learn selenium webdriver-manager openpyxl
```

## Kullanım

### 1. Veri toplama
```bash
python scraper.py
python scraper2.py
python scraper3.py
python scraper4.py
```

### 2. Veri ön işleme
```bash
python hafta1.py
python hafta2.py
python hafta3.py
python veri_birlestir.py
```

### 3. Model eğitimi
```bash
python hafta4.py
```

### 4. API servisini başlatma
```bash
uvicorn api:app --reload
```
Ardından:
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"urun_adi": "Schneider 40A Kontaktör"}'
```

## Veri Toplama Hakkında Not

Bu çalışmada yalnızca herkese açık biçimde yayınlanan ürün adı ve kategori bilgisi toplanmıştır; kişisel veri (kullanıcı bilgisi, yorum, vb.) toplanmamıştır. Veri, akademik/araştırma amaçlı kullanım için paylaşılmaktadır.

## Bilinen Sınırlılıklar

- `scraper3.py` (Trendyol) ve `scraper4.py` (Amazon) verileri **arama sorgusu adına göre**, `scraper2.py` (e-dundar) verisi ise **sitenin kendi kategori taksonomisinden** etiketlenmiştir.
- Kategoriler arasında ciddi sınıf dengesizliği bulunmaktadır (örn. Halojen Ampul: 1 örnek).
- `yanlis.py`, modelin resmî test bölünmesini (`random_state=42`) değil, veri setinin sıralı son %20'lik dilimini kullanmaktadır.

Ayrıntılı tartışma için ilgili makaleye bakınız.

## Atıf

Bu çalışmayı kullanırsanız lütfen ilgili makaleyi/tezi kaynak gösteriniz:

> Yazğan, M. (2026). BERTürk Tabanlı Türkçe Elektrik Ürünlerinin Otomatik Sınıflandırılması: Web Scraping ile Oluşturulan Alan-Özel Veri Seti Üzerinde Deneysel Bir Çalışma. Karadeniz Teknik Üniversitesi, Yazılım Mühendisliği Bölümü, Bitirme Çalışması.

