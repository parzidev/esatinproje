import json
import os
import random

def nadirligi_ekle(json_dosyasi, cikti_dosyasi):
    """Kartlara nadirlik bilgisi ekler"""
    try:
        # JSON dosyasını oku
        with open(json_dosyasi, "r", encoding="utf-8") as f:
            kartlar = json.load(f)
        
        print(f"{len(kartlar)} kart bulundu.")
        
        # Nadirlik seviyeleri
        nadirlikler = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
        
        # Kart tipine göre nadirlik olasılıkları
        nadirlik_olasiliklari = {
            "Unit": {"Common": 0.5, "Uncommon": 0.3, "Rare": 0.15, "Epic": 0.04, "Legendary": 0.01},
            "Champion Unit": {"Common": 0.0, "Uncommon": 0.1, "Rare": 0.3, "Epic": 0.4, "Legendary": 0.2},
            "Token Unit": {"Common": 0.9, "Uncommon": 0.1, "Rare": 0.0, "Epic": 0.0, "Legendary": 0.0},
            "Signature Unit": {"Common": 0.0, "Uncommon": 0.2, "Rare": 0.4, "Epic": 0.3, "Legendary": 0.1},
            "Spell": {"Common": 0.5, "Uncommon": 0.3, "Rare": 0.15, "Epic": 0.04, "Legendary": 0.01},
            "Signature Spell": {"Common": 0.0, "Uncommon": 0.2, "Rare": 0.4, "Epic": 0.3, "Legendary": 0.1},
            "Gear": {"Common": 0.3, "Uncommon": 0.4, "Rare": 0.2, "Epic": 0.08, "Legendary": 0.02},
            "Legend": {"Common": 0.0, "Uncommon": 0.0, "Rare": 0.0, "Epic": 0.3, "Legendary": 0.7},
            "Battlefield": {"Common": 0.3, "Uncommon": 0.3, "Rare": 0.2, "Epic": 0.15, "Legendary": 0.05},
            "Basic Rune": {"Common": 0.4, "Uncommon": 0.3, "Rare": 0.2, "Epic": 0.08, "Legendary": 0.02},
            "Token Card": {"Common": 1.0, "Uncommon": 0.0, "Rare": 0.0, "Epic": 0.0, "Legendary": 0.0}
        }
        
        # İsme göre nadirlik belirleme
        isim_nadirlik_eslesmeleri = {
            "legendary": "Legendary",
            "ancient": "Legendary",
            "mythic": "Legendary",
            "divine": "Epic",
            "epic": "Epic",
            "rare": "Rare",
            "uncommon": "Uncommon",
            "common": "Common",
            "token": "Common"
        }
        
        # Her karta nadirlik ekle
        for i, kart in enumerate(kartlar):
            tip = kart.get("tip", "Unit")
            isim = kart.get("isim", "").lower()
            
            # Eğer karta zaten nadirlik atanmışsa, atla
            if "nadir" in kart and kart["nadir"]:
                continue
            
            # İsme göre nadirlik belirle
            isim_nadirlik = None
            for anahtar, deger in isim_nadirlik_eslesmeleri.items():
                if anahtar in isim:
                    isim_nadirlik = deger
                    break
            
            # Eğer isimden nadirlik belirlenemezse, tipe göre rastgele belirle
            if not isim_nadirlik:
                # Varsayılan olasılıkları kullan
                olasiliklar = nadirlik_olasiliklari.get(tip, {"Common": 0.6, "Uncommon": 0.25, "Rare": 0.1, "Epic": 0.04, "Legendary": 0.01})
                
                # Rastgele bir sayı seç
                sayi = random.random()
                
                # Kümülatif olasılığa göre nadirlik belirle
                kumulatif = 0
                for nadirlik, olasilik in olasiliklar.items():
                    kumulatif += olasilik
                    if sayi <= kumulatif:
                        isim_nadirlik = nadirlik
                        break
            
            # Nadirliği karta ekle
            kart["nadir"] = isim_nadirlik
            
            # İşlenen kart sayısını göster
            if (i + 1) % 50 == 0:
                print(f"{i + 1} kart işlendi...")
        
        # Sonuçları kaydet
        with open(cikti_dosyasi, "w", encoding="utf-8") as f:
            json.dump(kartlar, f, ensure_ascii=False, indent=4)
        
        print(f"Tüm kartlara nadirlik bilgisi eklendi ve '{cikti_dosyasi}' dosyasına kaydedildi.")
        
        # Nadirlik istatistiklerini göster
        nadirlik_sayilari = {}
        for nadirlik in nadirlikler:
            nadirlik_sayilari[nadirlik] = sum(1 for kart in kartlar if kart.get("nadir") == nadirlik)
        
        print("\nNadirlik İstatistikleri:")
        for nadirlik, sayi in nadirlik_sayilari.items():
            yuzde = sayi / len(kartlar) * 100
            print(f"{nadirlik}: {sayi} kart ({yuzde:.1f}%)")
        
        # Bazı örnek kartları göster
        print("\nÖrnek kartlar:")
        for i in range(min(5, len(kartlar))):
            kart = kartlar[i]
            print(f"{kart.get('isim', 'Bilinmeyen')} ({kart.get('tip', 'Bilinmeyen')}) - Nadirlik: {kart.get('nadir', 'N/A')}, Energy: {kart.get('energy', 'N/A')}, Power: {kart.get('power', 'N/A')}, Might: {kart.get('might', 'N/A')}")
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    # Mevcut JSON dosyası
    json_dosyasi = "kartlar_degerli.json"
    
    # Çıktı dosyası
    cikti_dosyasi = "kartlar_tam.json"
    
    # Kartlara nadirlik ekle
    nadirligi_ekle(json_dosyasi, cikti_dosyasi)
