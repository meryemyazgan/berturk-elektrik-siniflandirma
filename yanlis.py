import json
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("egitilmis_model")
model = AutoModelForSequenceClassification.from_pretrained("egitilmis_model")
model.eval()

with open("egitilmis_model/kategori_index.json", encoding="utf-8") as f:
    kategori_index = json.load(f)
index_kategori = {int(v): k for k, v in kategori_index.items()}

with open("etiketli_veri.json", encoding="utf-8") as f:
    veri = json.load(f)

test_veri = veri[int(len(veri)*0.8):]

print("🔍 Yanlış Sınıflandırılan Ürünler:")
print("=" * 65)

dogru = yanlis = 0
for urun in test_veri[:300]:
    gercek_idx = kategori_index[urun["kategori"]]
    inputs = tokenizer(urun["metin"], return_tensors="pt", truncation=True, padding=True, max_length=64)
    with torch.no_grad():
        output = model(**inputs)
    tahmin_idx = int(np.argmax(output.logits.numpy()))
    guven = float(torch.softmax(output.logits, dim=1).max().item()) * 100

    if gercek_idx != tahmin_idx:
        yanlis += 1
        print(f"❌ Ürün  : {urun['metin'][:55]}")
        print(f"   Gerçek : {urun['kategori']}")
        print(f"   Tahmin : {index_kategori[tahmin_idx]} (%{guven:.1f})")
        print()
    else:
        dogru += 1

print("=" * 65)
print(f"✅ Doğru : {dogru}  |  ❌ Yanlış: {yanlis}  |  🎯 Başarı: %{round(dogru/(dogru+yanlis)*100,1)}")