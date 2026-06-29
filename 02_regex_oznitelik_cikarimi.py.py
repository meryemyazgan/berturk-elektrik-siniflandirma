import pandas as pd
import re

# Veriyi oku
df = pd.read_excel("elektrik_urun_veri_seti.xlsx", sheet_name="Ham_Veri", header=None, skiprows=3)

df.columns = [
    "urun_adi", "marka", "model_kodu", "urun_tipi",
    "guc_w", "gerilim_v", "duy_tipi",
    "renk_sicakligi_k", "isik_rengi", "ampul_tipi",
    "model_serisi", "ozel_ozellik", "kaynak", "notlar"
]

df = df.dropna(subset=["marka"])

# Temizleme (sadece gösterim için)
df["urun_adi_temiz"] = df["urun_adi"].str.lower().str.strip()

# Fonksiyonlar — HAM METİN üzerinde çalışıyor
def guc_cikar(metin):
    eslesme = re.search(r'(\d+[,\.]\d+|\d+)\s*(w|watt)', str(metin), re.IGNORECASE)
    if eslesme:
        return eslesme.group(1).replace(',', '.')
    return None

def renk_sicakligi_cikar(metin):
    eslesme = re.search(r'(\d{4})\s*k', str(metin), re.IGNORECASE)
    if eslesme:
        return eslesme.group(1)
    return None

def duy_cikar(metin):
    eslesme = re.search(r'(e27|e14|gu10|g95|g9)\b', str(metin), re.IGNORECASE)
    if eslesme:
        return eslesme.group(1).upper()
    return None

def isik_rengi_cikar(metin):
    metin = str(metin).lower()
    if 'beyaz' in metin:
        return 'Beyaz'
    elif 'gün' in metin or 'gun' in metin:
        return 'Gün Işığı'
    elif 'sarı' in metin or 'sari' in metin:
        return 'Sarı'
    elif 'naturel' in metin:
        return 'Naturel Beyaz'
    return None

# HAM urun_adi üzerinde uygula
df["guc_otomatik"]            = df["urun_adi"].apply(guc_cikar)
df["renk_sicakligi_otomatik"] = df["urun_adi"].apply(renk_sicakligi_cikar)
df["duy_otomatik"]            = df["urun_adi"].apply(duy_cikar)
df["isik_rengi_otomatik"]     = df["urun_adi"].apply(isik_rengi_cikar)

print("\n🔍 Otomatik çıkarılan öznitelikler:")
print(df[["urun_adi", "guc_otomatik", "renk_sicakligi_otomatik", "duy_otomatik", "isik_rengi_otomatik"]].to_string())



# Sonuçları yeni Excel'e kaydet
df_kayit = df[[
    "urun_adi", "marka", "model_kodu", "urun_tipi",
    "guc_otomatik", "renk_sicakligi_otomatik",
    "duy_otomatik", "isik_rengi_otomatik", "notlar"
]]

df_kayit.columns = [
    "urun_adi", "marka", "model_kodu", "urun_tipi",
    "guc_w", "renk_sicakligi_k",
    "duy_tipi", "isik_rengi", "notlar"
]

df_kayit.to_excel("temiz_veri.xlsx", index=False)
print("\n✅ temiz_veri.xlsx kaydedildi!")