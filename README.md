# BERTürk Tabanlı Türkçe Elektrik Ürünlerinin Otomatik Sınıflandırılması

Türkçe e-ticaret platformlarından toplanan elektrik/elektroteknik ürün adlarının BERTürk (`dbmdz/bert-base-turkish-cased`) fine-tuning yöntemiyle otomatik kategorize edilmesi üzerine yürütülen bitirme çalışması.

Bu repo, ilgili akademik makalenin **veri ve kod erişilebilirliği** beyanı kapsamında paylaşılmaktadır.

## Proje Özeti

- **Veri**: 4 e-ticaret platformundan web scraping ile toplanan 11.160 ürün, 20 kategori
- **Model**: `dbmdz/bert-base-turkish-cased` fine-tuning, %92,5 test doğruluğu
- **Servis**: FastAPI REST API ile gerçek zamanlı kategori tahmini

## Eğitilmiş Model

Eğitilmiş model dosyaları Hugging Face Hub'da barındırılmaktadır:

👉 [https://huggingface.co/meryyzgn/berturk-elektrik-siniflandirma](https://huggingface.co/meryyzgn/berturk-elektrik-siniflandirma)

Modeli kullanmak için:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch, json, numpy as np

tokenizer = AutoTokenizer.from_pretrained("meryyzgn/berturk-elektrik-siniflandirma")
model = AutoModelForSequenceClassification.from_pretrained("meryyzgn/berturk-elektrik-siniflandirma")
model.eval()

urun_adi = "Schneider 40A Kontaktör"
inputs = tokenizer(urun_adi, return_tensors="pt", truncation=True, padding=True, max_length=64)
with torch.no_grad():
    outputs = model(**inputs)
    tahmin_idx = int(np.argmax(outputs.logits.numpy()))
    guven = float(torch.softmax(outputs.logits, dim=1).max().item()) * 100
print(f"Kategori indeksi: {tahmin_idx}, Güven: %{guven:.1f}")
```

Kategori isimlerine ulaşmak için `kategori_index.json` dosyasını kullanın.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `scraper.py` | elektrikmarket.com.tr veri toplama betiği |
| `scraper2.py` | e-dundar.com veri toplama betiği (site taksonomisi tabanlı) |
| `scraper3.py` | trendyol.com veri toplama betiği (arama sorgusu tabanlı) |
| `scraper4.py` | amazon.com.tr veri toplama betiği (arama sorgusu tabanlı) |
| `01_ham_veri_okuma.py` | Ham veri (Excel) okuma |
| `02_regex_oznitelik_cikarimi.py` | Regex tabanlı teknik öznitelik çıkarımı |
| `03_etiketleme_json.py` | Etiketleme ve `etiketli_veri.json` oluşturma |
| `veri_birlestir.py` | Tüm kaynakların birleştirilmesi ve tekilleştirme |
| `04_model_egitimi.py` | BERTürk fine-tuning, classification report, confusion matrix |
| `kontrol.py` | Kategori-indeks eşleşmesinin kontrolü |
| `yanlis.py` | Yanlış sınıflandırılan ürünlerin incelenmesi |
| `api.py` | FastAPI REST servisi (`/predict` endpoint) |
| `test_api.py` | API test betiği |
| `rapor.py` | Sonuç raporlama yardımcı betiği |
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
python 01_ham_veri_okuma.py
python 02_regex_oznitelik_cikarimi.py
python 03_etiketleme_json.py
python veri_birlestir.py
```

### 3. Model eğitimi
```bash
python 04_model_egitimi.py
```

### 4. API servisini başlatma
```bash
uvicorn api:app --reload
```

## Bilinen Sınırlılıklar

- `scraper3.py` ve `scraper4.py` arama sorgusu adına göre, `scraper2.py` sitenin kendi kategori taksonomisinden etiketlenmiştir.
- Kategoriler arasında ciddi sınıf dengesizliği bulunmaktadır (Halojen Ampul: 1 örnek).
- `yanlis.py`, modelin resmî test bölünmesini değil, veri setinin sıralı son %20'sini kullanmaktadır.

## Atıf

> Yazğan, M. (2026). BERTürk Tabanlı Türkçe Elektrik Ürünlerinin Otomatik Sınıflandırılması. Karadeniz Teknik Üniversitesi, Yazılım Mühendisliği Bölümü, Bitirme Çalışması.
