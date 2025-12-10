import os
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# === Selenium ayarları ===
chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı gizli çalıştır
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Kartların bilgilerini saklayacak liste
tum_kartlar = []

# Mevcut klasörler
klasorler = [
    "Unit", "Token_Unit", "Token_Card", "Spell", "Signature_Unit", 
    "Signature_Spell", "Gear", "Legend", "Champion_Unit", "Battlefield", "Basic_Rune"
]

# Web sitesinden kart bilgilerini çeken fonksiyon
def kart_bilgilerini_cek():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://piltoverarchive.com/cards")
    
    try:
        # Sayfanın yüklenmesini bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.group img"))
        )
        
        # Tüm kartları bul
        cards = driver.find_elements(By.CSS_SELECTOR, "div.group img")
        print(f"{len(cards)} kart bulundu.")
        
        for idx, card in enumerate(cards, start=1):
            try:
                # Kart ismi
                name = card.get_attribute("alt").strip()
                
                # Kart görseli
                img_url = card.get_attribute("src")
                
                # Kartı açmak için tıkla
                driver.execute_script("arguments[0].click();", card)
                time.sleep(1.5)
                
                # Kart detaylarını çek
                kart_bilgisi = kart_detaylarini_al(driver, name, img_url)
                tum_kartlar.append(kart_bilgisi)
                
                print(f"[{idx}] {name} bilgileri alındı")
                
                # Kart detayını kapat
                close_btn = driver.find_element(By.CSS_SELECTOR, "button[data-slot='dialog-close']")
                driver.execute_script("arguments[0].click();", close_btn)
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Hata: {e}")
                continue
                
    finally:
        driver.quit()

# Kart detaylarını çeken fonksiyon
def kart_detaylarini_al(driver, name, img_url):
    kart_bilgisi = {
        "isim": name,
        "gorsel_url": img_url
    }
    
    try:
        # Kart tipi ve nadir seviyesi
        badges = driver.find_elements(By.CSS_SELECTOR, "span[data-slot='badge'] span")
        badge_texts = [b.text.strip() for b in badges if b.text.strip()]
        
        if len(badge_texts) >= 1:
            kart_bilgisi["tip"] = badge_texts[0]
        if len(badge_texts) >= 2:
            kart_bilgisi["nadir"] = badge_texts[1]
            
        # Fae gibi etiketler
        tags = driver.find_elements(By.CSS_SELECTOR, "span[data-slot='badge'].inline-flex")
        if tags:
            kart_bilgisi["etiketler"] = [tag.text.strip() for tag in tags if tag.text.strip()]
        
        # Energy, Power, Might değerleri
        stats_div = driver.find_element(By.CSS_SELECTOR, "div.grid.grid-cols-3")
        if stats_div:
            stats = stats_div.find_elements(By.CSS_SELECTOR, "div.space-y-1")
            
            for stat in stats:
                stat_name = stat.find_element(By.CSS_SELECTOR, "span").text.strip()
                stat_value = stat.find_element(By.CSS_SELECTOR, "div").text.strip()
                
                if stat_name == "Energy":
                    kart_bilgisi["energy"] = stat_value
                elif stat_name == "Power":
                    kart_bilgisi["power"] = stat_value
                elif stat_name == "Might":
                    kart_bilgisi["might"] = stat_value
        
        # Açıklama
        try:
            description_div = driver.find_element(By.CSS_SELECTOR, "div.space-y-2 p.text-base.text-zinc-300")
            kart_bilgisi["aciklama"] = description_div.text.strip()
        except NoSuchElementException:
            pass
            
        # Flavor text
        try:
            flavor_div = driver.find_element(By.CSS_SELECTOR, "div.space-y-2 p.text-base.italic")
            kart_bilgisi["flavor_text"] = flavor_div.text.strip()
        except NoSuchElementException:
            pass
            
        # Kart bilgileri (Artist, Set, Card Number)
        try:
            info_div = driver.find_element(By.CSS_SELECTOR, "div.rounded-lg.bg-zinc-800\\/50 div.space-y-2")
            info_items = info_div.find_elements(By.CSS_SELECTOR, "p.flex")
            
            for item in info_items:
                label = item.find_element(By.CSS_SELECTOR, "span").text.strip().replace(":", "")
                value = item.text.replace(label + ":", "").strip()
                
                if label == "Artist":
                    kart_bilgisi["artist"] = value
                elif label == "Set":
                    kart_bilgisi["set"] = value
                elif label == "Card Number":
                    kart_bilgisi["kart_numarasi"] = value
        except NoSuchElementException:
            pass
            
    except Exception as e:
        print(f"Kart detayı alınırken hata: {e}")
        
    return kart_bilgisi

# Mevcut klasörlerdeki kart dosyalarını JSON ile eşleştirme
def klasor_kart_eslestir():
    for klasor in klasorler:
        if os.path.exists(klasor):
            for dosya in os.listdir(klasor):
                if dosya.endswith(".webp"):
                    kart_adi = os.path.splitext(dosya)[0]
                    
                    # JSON'da bu kart adını ara
                    for kart in tum_kartlar:
                        if kart["isim"] == kart_adi:
                            kart["klasor"] = klasor
                            break

# JSON dosyasını oluştur
def json_olustur():
    with open("kartlar.json", "w", encoding="utf-8") as f:
        json.dump(tum_kartlar, f, ensure_ascii=False, indent=4)
    print(f"Toplam {len(tum_kartlar)} kart bilgisi JSON dosyasına kaydedildi.")

if __name__ == "__main__":
    print("Kart bilgileri çekiliyor...")
    kart_bilgilerini_cek()
    
    print("Kart bilgileri klasörlerle eşleştiriliyor...")
    klasor_kart_eslestir()
    
    print("JSON dosyası oluşturuluyor...")
    json_olustur()
    
    print("İşlem tamamlandı.")
