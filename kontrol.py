import json

with open("etiketli_veri.json", "r", encoding="utf-8") as f:
    veri = json.load(f)

kategoriler = list(set([v["kategori"] for v in veri]))
kategori_index = {k: i for i, k in enumerate(kategoriler)}
print("Eğitimde kullanılan kategori sırası:")
print(kategori_index)

