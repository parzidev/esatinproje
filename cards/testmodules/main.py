import os
import json
import argparse
import time
from tqdm import tqdm

# Kart bilgilerini çekme yöntemleri
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# === Kart klasörleri ===
KLASORLER = [
    "Unit", "Token_Unit", "Token_Card", "Spell", "Signature_Unit", 
    "Signature_Spell", "Gear", "Legend", "Champion_Unit", "Battlefield", "Basic_Rune"
]

def selenium_ile_kart_bilgilerini_al(kart_adi, klasor):
    """Selenium ile web sitesinden kart bilgilerini çeker"""
    if not SELENIUM_AVAILABLE:
        print("Selenium kütüphanesi yüklü değil. 'pip install selenium' komutu ile yükleyebilirsiniz.")
        return None
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Kart araması için URL
        driver.get(f"https://piltoverarchive.com/cards?search={kart_adi}")
        time.sleep(2)
        
        # Kart kartını bulmaya çalış
        cards = driver.find_elements(By.CSS_SELECTOR, "div.group img")
        
        if not cards:
            return None
            
        # İlk kartı seç
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

def html_ile_kart_bilgilerini_al(kart_adi, klasor):
    """BeautifulSoup ile web sitesinden kart bilgilerini çeker"""
    if not REQUESTS_AVAILABLE:
        print("Requests ve BeautifulSoup kütüphaneleri yüklü değil. 'pip install requests beautifulsoup4' komutu ile yükleyebilirsiniz.")
        return None
    
    # Kart araması için URL
    url = f"https://piltoverarchive.com/cards?search={kart_adi}"
    
    try:
        # İlk sayfayı al
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Kart kartını bul
        card_links = soup.select("a[href^='/cards/']")
        
        if not card_links:
            return None
            
        # İlk kartın detay sayfasına git
        card_url = "https://piltoverarchive.com" + card_links[0]['href']
        
        # Detay sayfasını al
        card_response = requests.get(card_url)
        card_soup = BeautifulSoup(card_response.text, 'html.parser')
        
        # Kart bilgilerini topla
        kart_bilgisi = {
            "isim": kart_adi,
            "klasor": klasor
        }
        
        # Kart tipi ve nadir seviyesi
        badges = card_soup.select("span[data-slot='badge'] span")
        badge_texts = [b.get_text().strip() for b in badges if b.get_text().strip()]
        
        if len(badge_texts) >= 1:
            kart_bilgisi["tip"] = badge_texts[0]
        if len(badge_texts) >= 2:
            kart_bilgisi["nadir"] = badge_texts[1]
            
        # Fae gibi etiketler
        tags = card_soup.select("span.inline-flex.items-center")
        if tags:
            kart_bilgisi["etiketler"] = [tag.get_text().strip() for tag in tags if tag.get_text().strip()]
        
        # Energy, Power, Might değerleri
        stats_div = card_soup.select_one("div.grid.grid-cols-3")
        if stats_div:
            stats = stats_div.select("div.space-y-1")
            
            for stat in stats:
                stat_name = stat.select_one("span").get_text().strip()
                stat_value = stat.select_one("div").get_text().strip()
                
                if stat_name == "Energy":
                    kart_bilgisi["energy"] = stat_value
                elif stat_name == "Power":
                    kart_bilgisi["power"] = stat_value
                elif stat_name == "Might":
                    kart_bilgisi["might"] = stat_value
        
        # Açıklama
        description_div = card_soup.select_one("div.space-y-2 p.text-base.text-zinc-300")
        if description_div:
            kart_bilgisi["aciklama"] = description_div.get_text().strip()
            
        # Flavor text
        flavor_div = card_soup.select_one("div.space-y-2 p.text-base.italic")
        if flavor_div:
            kart_bilgisi["flavor_text"] = flavor_div.get_text().strip()
            
        # Kart bilgileri (Artist, Set, Card Number)
        info_div = card_soup.select_one("div.rounded-lg.bg-zinc-800\\/50 div.space-y-2")
        if info_div:
            info_items = info_div.select("p.flex")
            
            for item in info_items:
                label_span = item.select_one("span")
                if label_span:
                    label = label_span.get_text().strip().replace(":", "")
                    value = item.get_text().replace(label + ":", "").strip()
                    
                    if label == "Artist":
                        kart_bilgisi["artist"] = value
                    elif label == "Set":
                        kart_bilgisi["set"] = value
                    elif label == "Card Number":
                        kart_bilgisi["kart_numarasi"] = value
            
        return kart_bilgisi
        
    except Exception as e:
        print(f"Hata: {e}")
        return None

def offline_kart_bilgilerini_al(kart_adi, klasor):
    """Offline olarak kart bilgilerini oluşturur"""
    # Temel kart bilgilerini oluştur
    kart_bilgisi = {
        "isim": kart_adi,
        "klasor": klasor,
        "dosya_yolu": os.path.join(klasor, f"{kart_adi}.webp")
    }
    
    # Kart tipini klasör adından tahmin et
    if klasor == "Unit":
        kart_bilgisi["tip"] = "Unit"
    elif klasor == "Token_Unit":
        kart_bilgisi["tip"] = "Token Unit"
    elif klasor == "Token_Card":
        kart_bilgisi["tip"] = "Token Card"
    elif klasor == "Spell":
        kart_bilgisi["tip"] = "Spell"
    elif klasor == "Signature_Unit":
        kart_bilgisi["tip"] = "Signature Unit"
    elif klasor == "Signature_Spell":
        kart_bilgisi["tip"] = "Signature Spell"
    elif klasor == "Gear":
        kart_bilgisi["tip"] = "Gear"
    elif klasor == "Legend":
        kart_bilgisi["tip"] = "Legend"
    elif klasor == "Champion_Unit":
        kart_bilgisi["tip"] = "Champion Unit"
    elif klasor == "Battlefield":
        kart_bilgisi["tip"] = "Battlefield"
    elif klasor == "Basic_Rune":
        kart_bilgisi["tip"] = "Basic Rune"
    
    return kart_bilgisi

def tum_kartlari_tara(method="html"):
    """Tüm klasörlerdeki kartları tarar ve bilgilerini toplar"""
    tum_kartlar = []
    toplam_kart_sayisi = 0
    
    # Toplam kart sayısını hesapla
    for klasor in KLASORLER:
        if os.path.exists(klasor):
            toplam_kart_sayisi += len([f for f in os.listdir(klasor) if f.endswith(".webp")])
    
    # İlerleme çubuğu oluştur
    progress_bar = tqdm(total=toplam_kart_sayisi, desc="Kartlar işleniyor")
    
    for klasor in KLASORLER:
        if os.path.exists(klasor):
            for dosya in os.listdir(klasor):
                if dosya.endswith(".webp"):
                    kart_adi = os.path.splitext(dosya)[0]
                    
                    # Kart bilgilerini seçilen yönteme göre al
                    if method == "selenium" and SELENIUM_AVAILABLE:
                        kart_bilgisi = selenium_ile_kart_bilgilerini_al(kart_adi, klasor)
                    elif method == "html" and REQUESTS_AVAILABLE:
                        kart_bilgisi = html_ile_kart_bilgilerini_al(kart_adi, klasor)
                    else:
                        kart_bilgisi = offline_kart_bilgilerini_al(kart_adi, klasor)
                    
                    if kart_bilgisi:
                        tum_kartlar.append(kart_bilgisi)
                    
                    progress_bar.update(1)
                    
                    # Sunucuya fazla yük bindirmemek için biraz bekle
                    if method != "offline":
                        time.sleep(1)
    
    progress_bar.close()
    return tum_kartlar

def json_olustur(kartlar, dosya_adi="kartlar.json"):
    """Kart bilgilerini JSON dosyasına kaydeder"""
    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(kartlar, f, ensure_ascii=False, indent=4)
    print(f"Toplam {len(kartlar)} kart bilgisi '{dosya_adi}' dosyasına kaydedildi.")

def main():
    parser = argparse.ArgumentParser(description="Kart bilgilerini çekip JSON dosyasına kaydeder")
    parser.add_argument("--method", choices=["selenium", "html", "offline"], default="html", 
                        help="Kart bilgilerini çekme yöntemi (varsayılan: html)")
    parser.add_argument("--output", default="kartlar.json", 
                        help="JSON dosyasının adı (varsayılan: kartlar.json)")
    
    args = parser.parse_args()
    
    # Seçilen yöntemin kullanılabilirliğini kontrol et
    if args.method == "selenium" and not SELENIUM_AVAILABLE:
        print("Selenium kütüphanesi yüklü değil. HTML yöntemi kullanılacak.")
        args.method = "html"
    
    if args.method == "html" and not REQUESTS_AVAILABLE:
        print("Requests ve BeautifulSoup kütüphaneleri yüklü değil. Offline yöntemi kullanılacak.")
        args.method = "offline"
    
    print(f"Kart bilgileri '{args.method}' yöntemi ile toplanıyor...")
    kartlar = tum_kartlari_tara(args.method)
    
    print("JSON dosyası oluşturuluyor...")
    json_olustur(kartlar, args.output)
    
    print("İşlem tamamlandı.")

if __name__ == "__main__":
    main()
