import json
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Veriyi oku
with open("etiketli_veri.json", "r", encoding="utf-8") as f:
    veri = json.load(f)

print(f"✅ Toplam veri: {len(veri)}")

# KATEGORİ SIRASINI SABİT TUT
kategoriler = list(set([v["kategori"] for v in veri]))
kategori_index = {k: i for i, k in enumerate(sorted(kategoriler))}
print(f"📂 Kategoriler: {kategoriler}")

# Tokenizer yükle
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")

# Veriyi hazırla
metinler = [v["metin"] for v in veri]
etiketler = [kategori_index[v["kategori"]] for v in veri]

# Eğitim / test ayır
X_train, X_test, y_train, y_test = train_test_split(
    metinler, etiketler, test_size=0.2, random_state=42
)

print(f"🏋️ Eğitim verisi: {len(X_train)}")
print(f"🧪 Test verisi: {len(X_test)}")

# Dataset sınıfı
class UrunDataset(Dataset):
    def __init__(self, metinler, etiketler):
        self.encodings = tokenizer(
            metinler,
            truncation=True,
            padding=True,
            max_length=64
        )
        self.etiketler = etiketler

    def __len__(self):
        return len(self.etiketler)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.etiketler[idx])
        return item

train_dataset = UrunDataset(X_train, y_train)
test_dataset  = UrunDataset(X_test, y_test)

# Model yükle ve katmanlar 
print("\n🤖 BERTurk modeli yükleniyor...")
model = AutoModelForSequenceClassification.from_pretrained(
    "dbmdz/bert-base-turkish-cased",
    num_labels=len(kategoriler)
)

# Eğitim ayarları — eval_strategy kullanıyoruz
training_args = TrainingArguments(
    output_dir="./model_cikti",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_steps=10,
    load_best_model_at_end=True,
)

def metrikleri_hesapla(pred):
    tahminler = np.argmax(pred.predictions, axis=1)
    return {"accuracy": accuracy_score(pred.label_ids, tahminler)}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=metrikleri_hesapla,
)

# Eğitimi başlat
print("\n🚀 Eğitim başlıyor, bekleyin (~5-10 dakika)...")
trainer.train()

# Sonuçları göster
print("\n📊 Test sonuçları:")
sonuclar = trainer.evaluate()
print(f"✅ Doğruluk: {sonuclar['eval_accuracy']*100:.1f}%")

# Modeli kaydet
model.save_pretrained("./egitilmis_model")
tokenizer.save_pretrained("./egitilmis_model")

# KATEGORİ SIRASINI DA KAYDET
import json
with open("./egitilmis_model/kategori_index.json", "w", encoding="utf-8") as f:
    json.dump(kategori_index, f, ensure_ascii=False)

print("✅ Model ve kategori sırası kaydedildi!")
print(f"Kategori sırası: {kategori_index}")




from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# Tahminleri al
print("\n📊 Detaylı Metrikler hesaplanıyor...")
tahminler = trainer.predict(test_dataset)
y_pred = np.argmax(tahminler.predictions, axis=1)
y_true = tahminler.label_ids

# Kategori isimlerini al
index_kategori = {v: k for k, v in kategori_index.items()}
kategori_isimleri = [index_kategori[i] for i in range(len(kategoriler))]

# Precision, Recall, F1
print("\n📋 Classification Report:")
print(classification_report(y_true, y_pred, target_names=kategori_isimleri))

# Confusion Matrix
print("\n🔢 Confusion Matrix:")
cm = confusion_matrix(y_true, y_pred)
print(f"{'':20}", end="")
for k in kategori_isimleri:
    print(f"{k[:8]:10}", end="")
print()
for i, satir in enumerate(cm):
    print(f"{kategori_isimleri[i]:20}", end="")
    for deger in satir:
        print(f"{deger:10}", end="")
    print()
