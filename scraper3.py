import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Trendyol arama bazlı kategoriler
aramalar = [
    ("klemens",         "Klemens"),
    ("kontakt%c3%b6r",  "Kontaktör"),
    ("sigorta+otomat",  "Sigorta"),
    ("led+amp%c3%bcl",  "Led Ampul"),
    ("kablo+nym",       "Kablo"),
    ("armat%c3%bcr+led","Armatür"),
    ("anahtar+priz",    "Anahtar Priz"),
    ("termik+r%c3%b6le","Termik Röle"),
    ("ka%c3%a7ak+ak%c3%adm+r%c3%b6lesi", "Kaçak Akım Rölesi"),
    ("led+panel",       "Led Panel"),
    ("led+spot",        "Led Spot"),
    ("led+proje%c3%a7t%c3%b6r", "Led Projektör"),
    ("elektrik+panosu", "Pano"),
    ("spiral+boru",     "Boru"),
    ("kablo+kanal%c4%b1","Kablo Kanalı"),
]

tum_urunler = []

for arama, kategori_adi in aramalar:
    print(f"\n📂 Kategori: {kategori_adi}")
    onceki_sayfa = set()

    for sayfa in range(1, 30):
        url = f"https://www.trendyol.com/sr?q={arama}&pi={sayfa}"
        print(f"  📄 Sayfa {sayfa}...")

        driver.get(url)
        time.sleep(3)

        urunler = driver.find_elements(By.CLASS_NAME, "product-name")

        if not urunler:
            print(f"  ⚠️ Ürün bulunamadı, duruyorum.")
            break

        bu_sayfa = set()
        for el in urunler:
            ad = el.text.strip()
            if ad and len(ad) > 3:
                bu_sayfa.add(ad)

        if bu_sayfa == onceki_sayfa or not bu_sayfa:
            print(f"  ⚠️ Tekrar, duruyorum.")
            break

        onceki_sayfa = bu_sayfa

        for ad in bu_sayfa:
            tum_urunler.append({
                "urun_adi": ad,
                "kategori": kategori_adi,
                "kaynak_site": "trendyol.com"
            })

        print(f"  ✅ {len(bu_sayfa)} ürün | Toplam: {len(tum_urunler)}")
        time.sleep(2)

driver.quit()

df = pd.DataFrame(tum_urunler)
df = df.drop_duplicates(subset=["urun_adi"])

print(f"\n📦 Toplam benzersiz ürün: {len(df)}")
print("\n📊 Kategori özeti:")
print(df["kategori"].value_counts())

df.to_excel("scraping_sonuc3.xlsx", index=False)
print("\n✅ scraping_sonuc3.xlsx kaydedildi!")
