import requests
import json

with open("etiketli_veri.json", "r", encoding="utf-8") as f:
    veri = json.load(f)

print("🔍 Yanlış sınıflandırılan ürünler:\n")

dogru = 0
yanlis = 0
yanlis_listesi = []

for urun in veri[:500]:
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json={"urun_adi": urun["metin"]}
    )
    sonuc = response.json()
    
    gercek = urun["kategori"]
    tahmin = sonuc["kategori"]
    guven = sonuc["guven_skoru"]
    
    if gercek == tahmin:
        dogru += 1
    else:
        yanlis += 1
        yanlis_listesi.append({
            "urun": urun["metin"],
            "gercek": gercek,
            "tahmin": tahmin,
            "guven": guven
        })

# Sadece yanlışları göster
for u in yanlis_listesi:
    print(f"❌ Ürün  : {u['urun'][:60]}")
    print(f"   Gerçek : {u['gercek']}")
    print(f"   Tahmin : {u['tahmin']} (%{u['guven']})")
    print()

print(f"📊 500 üründen:")
print(f"✅ Doğru : {dogru}")
print(f"❌ Yanlış: {yanlis}")
print(f"🎯 Başarı: %{round(dogru/500*100, 1)}")