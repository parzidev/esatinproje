import requests
import json
from bs4 import BeautifulSoup

def kart_detaylarini_cek(kart_url):
    """Doğrudan kart URL'sinden detayları çeker"""
    try:
        # Kart sayfasını al
        response = requests.get(kart_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Kart adını al
        title = soup.select_one("h1.text-4xl")
        if not title:
            title = soup.select_one("h1")
        
        kart_bilgisi = {}
        
        if title:
            kart_bilgisi["isim"] = title.get_text().strip()
        
        # Kart tipi ve nadir seviyesi
        badges = soup.select(".flex.items-center.gap-2 span.truncate")
        badge_texts = [b.get_text().strip() for b in badges if b.get_text().strip()]
        
        if len(badge_texts) >= 1:
            kart_bilgisi["tip"] = badge_texts[0]
        if len(badge_texts) >= 2:
            kart_bilgisi["nadir"] = badge_texts[1]
            
        # Fae gibi etiketler
        tags = soup.select(".flex.flex-wrap.gap-2 span.text-sm")
        if tags:
            kart_bilgisi["etiketler"] = [tag.get_text().strip() for tag in tags if tag.get_text().strip()]
        
        # Energy, Power, Might değerleri
        stats_div = soup.select_one(".grid.grid-cols-3")
        if stats_div:
            stats = stats_div.select(".space-y-1")
            
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
        description_div = soup.select_one(".space-y-2 p.text-base.text-zinc-300")
        if description_div:
            kart_bilgisi["aciklama"] = description_div.get_text().strip()
            
        # Flavor text
        flavor_div = soup.select_one(".space-y-2 p.text-base.italic")
        if flavor_div:
            kart_bilgisi["flavor_text"] = flavor_div.get_text().strip()
            
        # Kart bilgileri (Artist, Set, Card Number)
        info_div = soup.select_one(".rounded-lg.bg-zinc-800\\/50 .space-y-2")
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

# Örnek bir kart URL'si
kart_url = "https://piltoverarchive.com/cards/OGN-274"  # Sprite kartı

# Kart detaylarını çek
kart_bilgisi = kart_detaylarini_cek(kart_url)

# Sonuçları göster
if kart_bilgisi:
    print(json.dumps(kart_bilgisi, indent=4, ensure_ascii=False))
    
    # JSON dosyasına kaydet
    with open("ornek_kart_detay.json", "w", encoding="utf-8") as f:
        json.dump(kart_bilgisi, f, ensure_ascii=False, indent=4)
    
    print("Kart detayları 'ornek_kart_detay.json' dosyasına kaydedildi.")
else:
    print("Kart detayları alınamadı.")
