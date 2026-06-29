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

kategoriler = [
    ("led-ampul",               "Led Ampul"),
    ("rustik-led-ampul",        "Rustik Led Ampul"),
    ("halojen-ampul",           "Halojen Ampul"),
    ("led-projektor",           "Led Projektör"),
    ("led-spot",                "Led Spot"),
    ("sigortalar",              "Sigorta"),
    ("kontaktor",               "Kontaktör"),
    ("klemens",                 "Klemens"),
    ("kacak-akim-rolesi",       "Kaçak Akım Rölesi"),
    ("termik-role",             "Termik Röle"),
    ("nyaf-kablo",              "Kablo"),
    ("nya-kablo",               "Kablo"),
    ("nym-kablo",               "Kablo"),
    ("viko-karre-serisi",       "Anahtar Priz"),
    ("mutlusan-anahtar-priz",   "Anahtar Priz"),
    ("led-etanj-armatur",       "Armatür"),
    ("siva-alti-led-armatur",   "Armatür"),
    ("siva-ustu-led-armatur",   "Armatür"),
    ("led-trafo",               "Trafo"),
    ("vantilatorler",           "Vantilatör"),
    ("aspiratorler",            "Vantilatör"),
    ("60x60-led-panel",         "Led Panel"),
    ("siva-alti-panel-led-armaturler", "Led Panel"),
    ("ray-tipi-led-spot-armaturler",   "Led Spot"),
    ("kaçak-akim-rolesi",       "Kaçak Akım Rölesi"),
    ("dijital-sayac",           "Sayaç"),
    ("kablo-baglari",           "Kablo Aksesuarı"),
    ("spiral-boru",             "Boru"),
]

tum_urunler = []

for kategori_url, kategori_adi in kategoriler:
    print(f"\n📂 Kategori: {kategori_adi} ({kategori_url})")
    onceki_sayfa_urunleri = set()

    for sayfa in range(1, 30):
        url = f"https://www.elektrikmarket.com.tr/kategori/{kategori_url}?page={sayfa}"

        driver.get(url)
        time.sleep(2)

        kartlar = driver.find_elements(By.CLASS_NAME, "showcase")

        if not kartlar:
            print(f"  ⚠️ Sayfa {sayfa}: Ürün yok, duruyorum.")
            break

        # Bu sayfadaki ürün adlarını al
        bu_sayfa_urunleri = set()
        for kart in kartlar:
            try:
                ad = kart.find_element(By.CLASS_NAME, "showcase-title").text.strip()
                bu_sayfa_urunleri.add(ad)
            except:
                continue

        # Önceki sayfayla aynıysa dur
        if bu_sayfa_urunleri == onceki_sayfa_urunleri:
            print(f"  ⚠️ Sayfa {sayfa}: Aynı ürünler tekrar geliyor, duruyorum.")
            break

        onceki_sayfa_urunleri = bu_sayfa_urunleri

        # Ürünleri kaydet
        for kart in kartlar:
            try:
                ad = kart.find_element(By.CLASS_NAME, "showcase-title").text.strip()
                try:
                    fiyat = kart.find_element(By.CLASS_NAME, "showcase-price-new").text.strip()
                except:
                    fiyat = ""
                try:
                    link = kart.find_element(By.TAG_NAME, "a").get_attribute("href")
                except:
                    link = ""

                if ad:
                    tum_urunler.append({
                        "urun_adi": ad,
                        "fiyat": fiyat,
                        "kategori": kategori_adi,
                        "kaynak_url": link,
                        "kaynak_site": "elektrikmarket.com.tr"
                    })
            except:
                continue

        print(f"  ✅ Sayfa {sayfa}: {len(kartlar)} ürün | Toplam: {len(tum_urunler)}")
        time.sleep(1)

driver.quit()

# Tekrarları temizle
df = pd.DataFrame(tum_urunler)
df = df.drop_duplicates(subset=["urun_adi"])

print(f"\n📦 Toplam benzersiz ürün: {len(df)}")
print("\n📊 Kategori özeti:")
print(df["kategori"].value_counts())

df.to_excel("scraping_sonuc.xlsx", index=False)
print("\n✅ scraping_sonuc.xlsx kaydedildi!")