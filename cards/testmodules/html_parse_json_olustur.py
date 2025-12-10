import os
import json
import requests
import time
from bs4 import BeautifulSoup

# === Kart klasörleri ===
KLASORLER = [
    "Unit", "Token_Unit", "Token_Card", "Spell", "Signature_Unit", 
    "Signature_Spell", "Gear", "Legend", "Champion_Unit", "Battlefield", "Basic_Rune"
]

def html_ile_kart_bilgilerini_al(kart_adi):
    """Web sitesinden HTML parse ederek kart bilgilerini çeker"""
    # Kart araması için URL
    url = f"https://piltoverarchive.com/cards?search={kart_adi}"
    
    try:
        # İlk sayfayı al
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Kart kartını bul
        card_links = soup.select("a[href^='/cards/']")
        
        if not card_links:
            print(f"'{kart_adi}' kartı bulunamadı.")
            return None
            
        # İlk kartın detay sayfasına git
        card_url = "https://piltoverarchive.com" + card_links[0]['href']
        
        # Detay sayfasını al
        card_response = requests.get(card_url)
        card_soup = BeautifulSoup(card_response.text, 'html.parser')
        
        # Kart bilgilerini topla
        kart_bilgisi = {
            "isim": kart_adi
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
                    kart_bilgisi = html_ile_kart_bilgilerini_al(kart_adi)
                    
                    if kart_bilgisi:
                        kart_bilgisi["klasor"] = klasor
                        tum_kartlar.append(kart_bilgisi)
                        print(f"  ✓ {kart_adi} bilgileri alındı.")
                    else:
                        print(f"  ✗ {kart_adi} bilgileri alınamadı.")
                    
                    # Sunucuya fazla yük bindirmemek için biraz bekle
                    time.sleep(1)
    
    return tum_kartlar

def json_olustur(kartlar):
    """Kart bilgilerini JSON dosyasına kaydeder"""
    with open("kartlar_html.json", "w", encoding="utf-8") as f:
        json.dump(kartlar, f, ensure_ascii=False, indent=4)
    print(f"Toplam {len(kartlar)} kart bilgisi JSON dosyasına kaydedildi.")

if __name__ == "__main__":
    print("Kart bilgileri toplanıyor...")
    kartlar = tum_kartlari_tara()
    
    print("JSON dosyası oluşturuluyor...")
    json_olustur(kartlar)
    
    print("İşlem tamamlandı.")
