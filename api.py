import json
import torch
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = FastAPI(title="Teknik Ürün Sınıflandırma API", version="1.0")

print("🤖 Model yükleniyor...")
tokenizer = AutoTokenizer.from_pretrained("./egitilmis_model")
model = AutoModelForSequenceClassification.from_pretrained("./egitilmis_model")
model.eval()

# KATEGORİ SIRASINI DOĞRUDAN JSON'DAN OKU
with open("./egitilmis_model/kategori_index.json", "r", encoding="utf-8") as f:
    kategori_index = json.load(f)

# int key ile eşleştir
index_kategori = {int(v): k for k, v in kategori_index.items()}
kategoriler = list(kategori_index.keys())

print(f"✅ Model hazır!")
print(f"📋 Kategori sırası: {kategori_index}")

class UrunIstegi(BaseModel):
    urun_adi: str

@app.get("/")
def ana_sayfa():
    return {"kategoriler": kategori_index}

@app.post("/predict")
def tahmin_et(istek: UrunIstegi):
    inputs = tokenizer(
        istek.urun_adi,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    )
    with torch.no_grad():
        outputs = model(**inputs)
        tahmin_idx = int(np.argmax(outputs.logits.numpy()))
        guven = float(torch.softmax(outputs.logits, dim=1).max().item())

    print(f"Tahmin index: {tahmin_idx}, Kategori: {index_kategori[tahmin_idx]}")

    return {
        "urun_adi": istek.urun_adi,
        "kategori": index_kategori[tahmin_idx],
        "guven_skoru": round(guven * 100, 1)
    }
