import json
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.utils.data import Dataset
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Veriyi oku
with open("etiketli_veri.json", "r", encoding="utf-8") as f:
    veri = json.load(f)

# Kategori sırasını yükle
with open("./egitilmis_model/kategori_index.json", "r", encoding="utf-8") as f:
    kategori_index = json.load(f)

index_kategori = {int(v): k for k, v in kategori_index.items()}
kategori_isimleri = [index_kategori[i] for i in range(len(kategori_index))]

# Model yükle
tokenizer = AutoTokenizer.from_pretrained("./egitilmis_model")
model = AutoModelForSequenceClassification.from_pretrained("./egitilmis_model")
model.eval()

# Test verisini hazırla
metinler = [v["metin"] for v in veri]
etiketler = [kategori_index[v["kategori"]] for v in veri]

_, X_test, _, y_test = train_test_split(
    metinler, etiketler, test_size=0.2, random_state=42
)

# Dataset
class UrunDataset(Dataset):
    def __init__(self, metinler, etiketler):
        self.encodings = tokenizer(metinler, truncation=True, padding=True, max_length=64)
        self.etiketler = etiketler
    def __len__(self):
        return len(self.etiketler)
    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.etiketler[idx])
        return item

from torch.utils.data import DataLoader

test_dataset = UrunDataset(X_test, y_test)
test_loader = DataLoader(test_dataset, batch_size=32)

# Tahmin yap
y_pred = []
y_true = []

print("🔍 Test ediliyor...")
with torch.no_grad():
    for batch in test_loader:
        labels = batch.pop("labels")
        outputs = model(**batch)
        preds = np.argmax(outputs.logits.numpy(), axis=1)
        y_pred.extend(preds)
        y_true.extend(labels.numpy())

# Rapor
print("\n📋 Classification Report:")
print(classification_report(y_true, y_pred, target_names=kategori_isimleri, labels=list(range(len(kategori_isimleri))), zero_division=0))

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