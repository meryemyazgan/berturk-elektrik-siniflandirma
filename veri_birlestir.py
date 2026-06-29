import pandas as pd
import json
import re

# Tüm scraping dosyalarını oku
df1 = pd.read_excel("scraping_sonuc.xlsx")   # elektrikmarket - 989 ürün
df2 = pd.read_excel("scraping_sonuc2.xlsx")  # e-dundar - 148 ürün
df3 = pd.read_excel("scraping_sonuc3.xlsx")  # trendyol - 7073 ürün
df4 = pd.read_excel("scraping_sonuc4.xlsx")
print(f"amazon: {len(df4)}")


print(f"elektrikmarket: {len(df1)}")
print(f"e-dundar: {len(df2)}")
print(f"trendyol: {len(df3)}")

# Birleştir
df_hepsi = pd.concat([df1, df2, df3, df4], ignore_index=True)
df_hepsi = df_hepsi.drop_duplicates(subset=["urun_adi"])

print(f"\n✅ Toplam benzersiz: {len(df_hepsi)}")

# Öznitelik fonksiyonları
def guc_cikar(metin):
    eslesme = re.search(r'(\d+[,\.]\d+|\d+)\s*(w|watt)', str(metin), re.IGNORECASE)
    if eslesme:
        return eslesme.group(1).replace(',', '.')
    return ""

def renk_sicakligi_cikar(metin):
    eslesme = re.search(r'(\d{4})\s*k', str(metin), re.IGNORECASE)
    if eslesme:
        return eslesme.group(1)
    return ""

def duy_cikar(metin):
    eslesme = re.search(r'(e27|e14|gu10|g95|g9)\b', str(metin), re.IGNORECASE)
    if eslesme:
        return eslesme.group(1).upper()
    return ""

def isik_rengi_cikar(metin):
    metin = str(metin).lower()
    if 'beyaz' in metin: return 'Beyaz'
    elif 'gün' in metin or 'gun' in metin: return 'Gün Işığı'
    elif 'sarı' in metin or 'sari' in metin: return 'Sarı'
    elif 'naturel' in metin: return 'Naturel Beyaz'
    return ""

def marka_cikar(metin):
    markalar = [
        "Cata", "Sylvania", "Osram", "Philips", "Viko", "Mutlusan",
        "Schneider", "Legrand", "ABB", "Siemens", "Hager",
        "Pelsan", "Foton", "Ledvance", "Opple", "Kanlux",
        "Panasonic", "Samsung", "General Electric", "Teco"
    ]
    for marka in markalar:
        if marka.lower() in str(metin).lower():
            return marka
    return ""

# Orijinal 27 manuel ürün
df_orijinal = pd.read_excel("temiz_veri.xlsx")
orijinal_veri = []
for _, satir in df_orijinal.iterrows():
    orijinal_veri.append({
        "metin": str(satir["urun_adi"]),
        "marka": str(satir["marka"]) if pd.notna(satir["marka"]) else "",
        "guc": str(satir["guc_w"]) if pd.notna(satir["guc_w"]) else "",
        "renk_sicakligi": str(satir["renk_sicakligi_k"]) if pd.notna(satir["renk_sicakligi_k"]) else "",
        "duy": str(satir["duy_tipi"]) if pd.notna(satir["duy_tipi"]) else "",
        "isik_rengi": str(satir["isik_rengi"]) if pd.notna(satir["isik_rengi"]) else "",
        "kategori": "Led Ampul",
        "kaynak": "manuel"
    })

# Scraping verisi
yeni_veri = []
for _, satir in df_hepsi.iterrows():
    urun_adi = str(satir["urun_adi"])
    yeni_veri.append({
        "metin": urun_adi,
        "marka": marka_cikar(urun_adi),
        "guc": guc_cikar(urun_adi),
        "renk_sicakligi": renk_sicakligi_cikar(urun_adi),
        "duy": duy_cikar(urun_adi),
        "isik_rengi": isik_rengi_cikar(urun_adi),
        "kategori": str(satir["kategori"]),
        "kaynak": str(satir.get("kaynak_site", "scraping"))
    })

# Birleştir ve tekrarları temizle
tum_veri = orijinal_veri + yeni_veri
gorulmus = set()
benzersiz = []
for u in tum_veri:
    if u["metin"] not in gorulmus:
        gorulmus.add(u["metin"])
        benzersiz.append(u)

print(f"✅ Final veri seti: {len(benzersiz)} ürün")

# Kategori dağılımı
kategoriler = {}
for u in benzersiz:
    k = u["kategori"]
    kategoriler[k] = kategoriler.get(k, 0) + 1
print("\n📊 Kategori dağılımı:")
for k, s in sorted(kategoriler.items(), key=lambda x: -x[1]):
    print(f"  {k}: {s}")

# Kaydet
with open("etiketli_veri.json", "w", encoding="utf-8") as f:
    json.dump(benzersiz, f, ensure_ascii=False, indent=2)

print("\n✅ etiketli_veri.json güncellendi!")
