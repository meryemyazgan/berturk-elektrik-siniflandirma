import pandas as pd

# index 3'ten itibaren direkt oku
df = pd.read_excel("elektrik_urun_veri_seti.xlsx", sheet_name="Ham_Veri", header=None, skiprows=3)

# Sütun adlarını manuel ver
df.columns = [
    "urun_adi", "marka", "model_kodu", "urun_tipi",
    "guc_w", "gerilim_v", "duy_tipi",
    "renk_sicakligi_k", "isik_rengi", "ampul_tipi",
    "model_serisi", "ozel_ozellik", "kaynak", "notlar"
]

# Boş satırları temizle
df = df.dropna(subset=["marka"])

# Kontrol
print("📦 İlk 5 ürün:")
print(df[["urun_adi", "marka", "guc_w", "renk_sicakligi_k"]].head())

print(f"\n✅ Toplam ürün sayısı: {len(df)}")
print(f"\n🏷️ Markalar: {df['marka'].unique()}")