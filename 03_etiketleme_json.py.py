from transformers import AutoTokenizer

# BERTurk tokenizer'ı indir
print("BERTurk indiriliyor, bekleyin...")
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")

# Test
test_cumle = "Cata 36W 6400K Beyaz Işık Bant Armatür CT-2478B"
tokenlar = tokenizer.tokenize(test_cumle)

print(f"\n✅ BERTurk hazır!")
print(f"📝 Test cümlesi: {test_cumle}")
print(f"🔤 Tokenlar: {tokenlar}")
print(f"📊 Token sayısı: {len(tokenlar)}")


import pandas as pd

# Temiz veriyi oku
df = pd.read_excel("temiz_veri.xlsx")

# Her ürün için etiket oluştur
def etiket_olustur(satir):
    metin = str(satir["urun_adi"])
    etiketler = {
        "metin": metin,
        "marka": str(satir["marka"]) if pd.notna(satir["marka"]) else "",
        "guc": str(satir["guc_w"]) if pd.notna(satir["guc_w"]) else "",
        "renk_sicakligi": str(satir["renk_sicakligi_k"]) if pd.notna(satir["renk_sicakligi_k"]) else "",
        "duy": str(satir["duy_tipi"]) if pd.notna(satir["duy_tipi"]) else "",
        "isik_rengi": str(satir["isik_rengi"]) if pd.notna(satir["isik_rengi"]) else "",
    }
    return etiketler

# Tüm ürünlere uygula
etiketli_veri = [etiket_olustur(satir) for _, satir in df.iterrows()]

# İlk 3 ürünü göster
print("\n📋 Etiketli veri örneği:")
for urun in etiketli_veri[:3]:
    print(urun)
    print()

print(f"✅ Toplam etiketli ürün: {len(etiketli_veri)}")



import json

# JSON olarak kaydet
with open("etiketli_veri.json", "w", encoding="utf-8") as f:
    json.dump(etiketli_veri, f, ensure_ascii=False, indent=2)

print("✅ etiketli_veri.json kaydedildi!")

# Dosyayı okuyup kontrol et
with open("etiketli_veri.json", "r", encoding="utf-8") as f:
    kontrol = json.load(f)

print(f"📊 JSON'daki ürün sayısı: {len(kontrol)}")
print("\n📋 İlk kayıt:")
print(json.dumps(kontrol[0], ensure_ascii=False, indent=2))