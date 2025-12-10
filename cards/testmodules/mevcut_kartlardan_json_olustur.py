import os
import json
from PIL import Image
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Kart klasörleri ===
KLASORLER = [
    "Unit", "Token_Unit", "Token_Card", "Spell", "Signature_Unit", 
    "Signature_Spell", "Gear", "Legend", "Champion_Unit", "Battlefield", "Basic_Rune"
]

# === Selenium ayarları ===
chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı gizli çalıştır
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

def kart_bilgilerini_al(kart_adi, klasor):
    """Web sitesinden kart bilgilerini çeker"""
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Kart araması için URL
        driver.get(f"https://piltoverarchive.com/cards?search={kart_adi}")
        time.sleep(2)
        
        # Kart kartını bulmaya çalış
        cards = driver.find_elements(By.CSS_SELECTOR, "div.group img")
        
        if not cards:
            print(f"'{kart_adi}' kartı bulunamadı.")
            return None
            
        # İlk kartı seç (arama sonucunda birden fazla kart olabilir)
        card = cards[0]
        
        # Kartı açmak için tıkla
        driver.execute_script("arguments[0].click();", card)
        time.sleep(1.5)
        
        # Kart bilgilerini topla
        kart_bilgisi = {
            "isim": kart_adi,
            "klasor": klasor
        }
        
        # Kart tipi ve nadir seviyesi
        try:
            badges = driver.find_elements(By.CSS_SELECTOR, "span[data-slot='badge'] span")
            badge_texts = [b.text.strip() for b in badges if b.text.strip()]
            
            if len(badge_texts) >= 1:
                kart_bilgisi["tip"] = badge_texts[0]
            if len(badge_texts) >= 2:
                kart_bilgisi["nadir"] = badge_texts[1]
        except:
            pass
            
        # Fae gibi etiketler
        try:
            tags = driver.find_elements(By.CSS_SELECTOR, "span[data-slot='badge'].inline-flex")
            if tags:
                kart_bilgisi["etiketler"] = [tag.text.strip() for tag in tags if tag.text.strip()]
        except:
            pass
        
        # Energy, Power, Might değerleri
        try:
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
        except:
            pass
        
        # Açıklama
        try:
            description_div = driver.find_element(By.CSS_SELECTOR, "div.space-y-2 p.text-base.text-zinc-300")
            kart_bilgisi["aciklama"] = description_div.text.strip()
        except:
            pass
            
        # Flavor text
        try:
            flavor_div = driver.find_element(By.CSS_SELECTOR, "div.space-y-2 p.text-base.italic")
            kart_bilgisi["flavor_text"] = flavor_div.text.strip()
        except:
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
        except:
            pass
            
        return kart_bilgisi
        
    except Exception as e:
        print(f"Hata: {e}")
        return None
        
    finally:
        driver.quit()

def tum_kartlari_tara():
    """Tüm klasörlerdeki kartları tarar ve bilgilerini toplar"""
    tum_kartlar = []
    
    for klasor in KLASORLER:
        if os.path.exists(klasor):
            print(f"{klasor} klasörü taranıyor...")
            for dosya in os.listdir(klasor):
                if dosya.endswith(".webp"):
                    kart_adi = os.path.splitext(dosya)[0]
                    print(f"  {kart_adi} bilgileri alınıyor...")
                    
                    # Kart bilgilerini al
                    kart_bilgisi = kart_bilgilerini_al(kart_adi, klasor)
                    
                    if kart_bilgisi:
                        tum_kartlar.append(kart_bilgisi)
                        print(f"  ✓ {kart_adi} bilgileri alındı.")
                    else:
                        print(f"  ✗ {kart_adi} bilgileri alınamadı.")
                    
                    # Sunucuya fazla yük bindirmemek için biraz bekle
                    time.sleep(1)
    
    return tum_kartlar

def json_olustur(kartlar):
    """Kart bilgilerini JSON dosyasına kaydeder"""
    with open("kartlar.json", "w", encoding="utf-8") as f:
        json.dump(kartlar, f, ensure_ascii=False, indent=4)
    print(f"Toplam {len(kartlar)} kart bilgisi JSON dosyasına kaydedildi.")

if __name__ == "__main__":
    print("Kart bilgileri toplanıyor...")
    kartlar = tum_kartlari_tara()
    
    print("JSON dosyası oluşturuluyor...")
    json_olustur(kartlar)
    
    print("İşlem tamamlandı.")
