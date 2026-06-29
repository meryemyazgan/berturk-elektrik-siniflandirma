import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# e-dundar.com kategorileri
kategoriler = [
    ("ampul",                        "Led Ampul"),
    ("salt-urunler-sigortalar-vb",   "Sigorta"),
    ("panolar-buatlar-ve-kutular",   "Pano"),
    ("kablo",                        "Kablo"),
    ("aydinlatma",                   "Armatür"),
    ("tesisat-malzemeleri",          "Tesisat"),
    ("aspirator-fan",                "Vantilatör"),
]

tum_urunler = []

for kategori_url, kategori_adi in kategoriler:
    print(f"\n📂 Kategori: {kategori_adi}")
    onceki_sayfa = set()

    for sayfa in range(1, 30):
        url = f"https://www.e-dundar.com/kategori/{kategori_url}?page={sayfa}"
        print(f"  📄 Sayfa {sayfa}...")

        driver.get(url)
        time.sleep(3)

        # Ürün adlarını bul — farklı class olabilir
        urun_adlari = driver.find_elements(By.CSS_SELECTOR, ".product-name, .showcase-title, .name, h3")

        if not urun_adlari:
            print(f"  ⚠️ Ürün bulunamadı, duruyorum.")
            break

        bu_sayfa = set()
        for el in urun_adlari:
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
                "kaynak_site": "e-dundar.com"
            })

        print(f"  ✅ {len(bu_sayfa)} ürün | Toplam: {len(tum_urunler)}")
        time.sleep(1)

driver.quit()

df = pd.DataFrame(tum_urunler)
df = df.drop_duplicates(subset=["urun_adi"])

print(f"\n📦 Toplam: {len(df)}")
print(df["kategori"].value_counts())

df.to_excel("scraping_sonuc2.xlsx", index=False)
print("✅ scraping_sonuc2.xlsx kaydedildi!")
