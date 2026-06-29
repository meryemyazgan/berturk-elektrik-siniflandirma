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

aramalar = [
    ("klemens",           "Klemens"),
    ("kontaktör",         "Kontaktör"),
    ("sigorta+otomat",    "Sigorta"),
    ("led+ampul",         "Led Ampul"),
    ("nym+kablo",         "Kablo"),
    ("led+armatür",       "Armatür"),
    ("anahtar+priz",      "Anahtar Priz"),
    ("termik+röle",       "Termik Röle"),
    ("kaçak+akım+rölesi", "Kaçak Akım Rölesi"),
    ("led+panel",         "Led Panel"),
    ("led+spot",          "Led Spot"),
    ("led+projektör",     "Led Projektör"),
    ("elektrik+panosu",   "Pano"),
    ("kablo+kanalı",      "Kablo Kanalı"),
    ("spiral+boru",       "Boru"),
    ("vantilatör",        "Vantilatör"),
]

tum_urunler = []

for arama, kategori_adi in aramalar:
    print(f"\n📂 Kategori: {kategori_adi}")
    onceki_sayfa = set()

    for sayfa in range(1, 20):
        url = f"https://www.amazon.com.tr/s?k={arama}&page={sayfa}"
        print(f"  📄 Sayfa {sayfa}...")

        driver.get(url)
        time.sleep(3)

        # s-result-item içindeki h2 span'larını al
        urunler = driver.find_elements(By.CSS_SELECTOR, 
            ".s-result-item h2 span")

        if not urunler:
            print(f"  ⚠️ Ürün bulunamadı, duruyorum.")
            break

        bu_sayfa = set()
        for el in urunler:
            ad = el.text.strip()
            if ad and len(ad) > 5:
                bu_sayfa.add(ad)

        if bu_sayfa == onceki_sayfa or not bu_sayfa:
            print(f"  ⚠️ Tekrar, duruyorum.")
            break

        onceki_sayfa = bu_sayfa

        for ad in bu_sayfa:
            tum_urunler.append({
                "urun_adi": ad,
                "kategori": kategori_adi,
                "kaynak_site": "amazon.com.tr"
            })

        print(f"  ✅ {len(bu_sayfa)} ürün | Toplam: {len(tum_urunler)}")
        time.sleep(2)

driver.quit()

df = pd.DataFrame(tum_urunler)
df = df.drop_duplicates(subset=["urun_adi"])

print(f"\n📦 Toplam: {len(df)}")
print(df["kategori"].value_counts())

df.to_excel("scraping_sonuc4.xlsx", index=False)
print("✅ scraping_sonuc4.xlsx kaydedildi!")