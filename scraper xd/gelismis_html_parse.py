import os
import json
import requests
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import concurrent.futures
import re

# === Kart klasörleri ===
KLASORLER = [
    "Unit", "Token_Unit", "Token_Card", "Spell", "Signature_Unit", 
    "Signature_Spell", "Gear", "Legend", "Champion_Unit", "Battlefield", "Basic_Rune"
]

# Maksimum eş zamanlı istek sayısı
MAX_WORKERS = 5

def html_ile_kart_bilgilerini_al(kart_adi, klasor):
    """Web sitesinden HTML parse ederek kart bilgilerini çeker"""
    # Kart araması için URL
    url = f"https://piltoverarchive.com/cards?search={kart_adi}"
    
    try:
        # İlk sayfayı al
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Kart kartını bul
        card_links = soup.select("a[href^='/cards/']")
        
        if not card_links:
            return {"isim": kart_adi, "klasor": klasor, "dosya_yolu": os.path.join(klasor, f"{kart_adi}.webp"), "durum": "bulunamadi"}
            
        # İlk kartın detay sayfasına git
        card_url = "https://piltoverarchive.com" + card_links[0]['href']
        
        # Detay sayfasını al
        card_response = requests.get(card_url, timeout=10)
        card_soup = BeautifulSoup(card_response.text, 'html.parser')
        
        # Kart bilgilerini topla
        kart_bilgisi = {
            "isim": kart_adi,
            "klasor": klasor,
            "dosya_yolu": os.path.join(klasor, f"{kart_adi}.webp"),
            "durum": "basarili"
        }
        
        # Kart tipi ve nadir seviyesi
        badges = card_soup.select("span[data-slot='badge'] span.truncate")
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
        
        # Kart görsel URL'sini al
        img_element = card_soup.select_one(f"img[alt='{kart_adi}']")
        if img_element and 'src' in img_element.attrs:
            kart_bilgisi["gorsel_url"] = img_element['src']
            
            # Kart numarasını URL'den çıkarmaya çalış
            if "kart_numarasi" not in kart_bilgisi:
                url_match = re.search(r'cards%2F([A-Z0-9-]+)\.webp', img_element['src'])
                if url_match:
                    kart_bilgisi["kart_numarasi"] = url_match.group(1)
            
        return kart_bilgisi
        
    except Exception as e:
        return {"isim": kart_adi, "klasor": klasor, "dosya_yolu": os.path.join(klasor, f"{kart_adi}.webp"), "durum": f"hata: {str(e)}"}

def kart_bilgilerini_al_worker(args):
    """Thread worker fonksiyonu"""
    kart_adi, klasor = args
    return html_ile_kart_bilgilerini_al(kart_adi, klasor)

def tum_kartlari_tara():
    """Tüm klasörlerdeki kartları tarar ve bilgilerini toplar"""
    tum_kartlar = []
    kart_listesi = []
    
    # Önce tüm kartları listele
    for klasor in KLASORLER:
        if os.path.exists(klasor):
            for dosya in os.listdir(klasor):
                if dosya.endswith(".webp"):
                    kart_adi = os.path.splitext(dosya)[0]
                    kart_listesi.append((kart_adi, klasor))
    
    # İlerleme çubuğu oluştur
    pbar = tqdm(total=len(kart_listesi), desc="Kartlar işleniyor")
    
    # Thread havuzu ile paralel işlem
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # İşlemleri başlat
        future_to_kart = {executor.submit(kart_bilgilerini_al_worker, args): args for args in kart_listesi}
        
        # Sonuçları topla
        for future in concurrent.futures.as_completed(future_to_kart):
            kart_bilgisi = future.result()
            if kart_bilgisi:
                tum_kartlar.append(kart_bilgisi)
                
                # İlerleme çubuğunu güncelle
                pbar.update(1)
                
                # Durum bilgisini göster
                kart_adi = kart_bilgisi["isim"]
                durum = kart_bilgisi.get("durum", "bilinmiyor")
                
                if durum == "basarili":
                    pbar.set_postfix_str(f"✓ {kart_adi}")
                elif durum == "bulunamadi":
                    pbar.set_postfix_str(f"✗ {kart_adi} bulunamadı")
                else:
                    pbar.set_postfix_str(f"! {kart_adi} {durum}")
    
    pbar.close()
    return tum_kartlar

def json_olustur(kartlar):
    """Kart bilgilerini JSON dosyasına kaydeder"""
    # Durum bilgisini temizle
    for kart in kartlar:
        if "durum" in kart:
            del kart["durum"]
    
    with open("kartlar_detayli.json", "w", encoding="utf-8") as f:
        json.dump(kartlar, f, ensure_ascii=False, indent=4)
    
    # Başarılı ve başarısız kart sayılarını hesapla
    basarili_kartlar = [k for k in kartlar if k.get("energy") is not None or k.get("power") is not None or k.get("might") is not None]
    
    print(f"Toplam {len(kartlar)} kart tarandı.")
    print(f"Detaylı bilgileri alınan kart sayısı: {len(basarili_kartlar)}")
    print(f"Tüm kartlar 'kartlar_detayli.json' dosyasına kaydedildi.")

if __name__ == "__main__":
    print("Kart bilgileri toplanıyor...")
    kartlar = tum_kartlari_tara()
    
    print("JSON dosyası oluşturuluyor...")
    json_olustur(kartlar)
    
    print("İşlem tamamlandı.")
