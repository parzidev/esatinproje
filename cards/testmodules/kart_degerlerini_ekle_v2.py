import json
import os
import re
from PIL import Image
import io

def klasor_adina_gore_tip_ata(kart):
    """Klasör adına göre kart tipini atar"""
    klasor = kart.get("klasor", "")
    
    if klasor == "Unit":
        kart["tip"] = "Unit"
    elif klasor == "Token_Unit":
        kart["tip"] = "Token Unit"
    elif klasor == "Token_Card":
        kart["tip"] = "Token Card"
    elif klasor == "Spell":
        kart["tip"] = "Spell"
    elif klasor == "Signature_Unit":
        kart["tip"] = "Signature Unit"
    elif klasor == "Signature_Spell":
        kart["tip"] = "Signature Spell"
    elif klasor == "Gear":
        kart["tip"] = "Gear"
    elif klasor == "Legend":
        kart["tip"] = "Legend"
    elif klasor == "Champion_Unit":
        kart["tip"] = "Champion Unit"
    elif klasor == "Battlefield":
        kart["tip"] = "Battlefield"
    elif klasor == "Basic_Rune":
        kart["tip"] = "Basic Rune"
    
    return kart

def kart_tipine_gore_deger_ata(kart):
    """Kart tipine göre varsayılan değerler atar"""
    tip = kart.get("tip", "")
    
    # Varsayılan değerler
    energy = "0"
    power = "0"
    might = "0"
    
    # Kart tipine göre değerleri ayarla
    if tip == "Unit":
        # Normal birimler
        energy = "1"
        power = "1"
        might = "2"
    elif tip == "Champion Unit":
        # Şampiyon birimleri daha güçlüdür
        energy = "2"
        power = "2"
        might = "3"
    elif tip == "Token Unit":
        # Token birimler genellikle daha zayıftır
        energy = "0"
        power = "1"
        might = "1"
    elif tip == "Signature Unit":
        # Signature birimler güçlüdür
        energy = "2"
        power = "2"
        might = "3"
    elif tip == "Spell" or tip == "Signature Spell":
        # Büyüler genellikle sadece energy değerine sahiptir
        energy = "1"
        power = "0"
        might = "1"
    elif tip == "Gear":
        # Ekipmanlar genellikle enerji ve might değerlerine sahiptir
        energy = "1"
        power = "0"
        might = "2"
    elif tip == "Battlefield":
        # Savaş alanları genellikle might değerine sahiptir
        energy = "0"
        power = "0"
        might = "3"
    elif tip == "Basic Rune":
        # Runeler genellikle might değerine sahiptir
        energy = "0"
        power = "0"
        might = "2"
    elif tip == "Legend":
        # Legend kartları genellikle yüksek değerlere sahiptir
        energy = "3"
        power = "3"
        might = "5"
    
    # İsme göre özel durumlar
    isim = kart.get("isim", "").lower()
    
    # Legendary birimler genellikle daha güçlüdür
    if "legendary" in isim or "commander" in isim or "champion" in isim:
        energy = str(max(int(energy), 2))
        power = str(max(int(power), 2))
        might = str(max(int(might), 3))
    
    # Poro birimleri genellikle düşük değerlere sahiptir
    if "poro" in isim:
        energy = "0"
        power = "1"
        might = "1"
    
    # Değerleri karta ekle
    if "energy" not in kart or kart["energy"] == "0":
        kart["energy"] = energy
    if "power" not in kart or kart["power"] == "0":
        kart["power"] = power
    if "might" not in kart or kart["might"] == "0":
        kart["might"] = might
    
    return kart

def isime_gore_deger_ata(kart):
    """Kart ismine göre özel değerler atar"""
    isim = kart.get("isim", "").lower()
    
    # Büyük birimler
    if any(x in isim for x in ["giant", "colossus", "titan", "dragon", "leviathan", "behemoth"]):
        kart["energy"] = "3"
        kart["power"] = "3"
        kart["might"] = "4"
    
    # Küçük birimler
    elif any(x in isim for x in ["poro", "sprite", "fae", "yordle", "minion", "follower"]):
        kart["energy"] = "0"
        kart["power"] = "1"
        kart["might"] = "1"
    
    # Orta büyüklükte birimler
    elif any(x in isim for x in ["warrior", "soldier", "knight", "guard", "sentinel"]):
        kart["energy"] = "1"
        kart["power"] = "2"
        kart["might"] = "2"
    
    # Güçlü büyüler
    elif any(x in isim for x in ["ultimate", "cataclysm", "judgment", "vengeance", "ruination"]):
        kart["energy"] = "3"
        kart["power"] = "0"
        kart["might"] = "3"
    
    # Zayıf büyüler
    elif any(x in isim for x in ["minor", "small", "little", "flash", "spark"]):
        kart["energy"] = "0"
        kart["power"] = "0"
        kart["might"] = "1"
    
    return kart

def kartlari_isle(json_dosyasi, cikti_dosyasi):
    """Kartları işleyerek değerleri ekler"""
    try:
        # JSON dosyasını oku
        with open(json_dosyasi, "r", encoding="utf-8") as f:
            kartlar = json.load(f)
        
        print(f"{len(kartlar)} kart bulundu.")
        
        # Her kartı işle
        for i, kart in enumerate(kartlar):
            # Klasör adına göre tip ata
            kart = klasor_adina_gore_tip_ata(kart)
            
            # Kart tipine göre değerleri ata
            kart = kart_tipine_gore_deger_ata(kart)
            
            # İsime göre özel değerler ata
            kart = isime_gore_deger_ata(kart)
            
            # İşlenen kart sayısını göster
            if (i + 1) % 50 == 0:
                print(f"{i + 1} kart işlendi...")
        
        # Sonuçları kaydet
        with open(cikti_dosyasi, "w", encoding="utf-8") as f:
            json.dump(kartlar, f, ensure_ascii=False, indent=4)
        
        print(f"Tüm kartlar işlendi ve '{cikti_dosyasi}' dosyasına kaydedildi.")
        
        # Bazı örnek kartları göster
        print("\nÖrnek kartlar:")
        for i in range(min(5, len(kartlar))):
            kart = kartlar[i]
            print(f"{kart.get('isim', 'Bilinmeyen')} ({kart.get('tip', 'Bilinmeyen')}) - Energy: {kart.get('energy', 'N/A')}, Power: {kart.get('power', 'N/A')}, Might: {kart.get('might', 'N/A')}")
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    # Mevcut JSON dosyası
    json_dosyasi = "kartlar_detayli.json"
    
    # Çıktı dosyası
    cikti_dosyasi = "kartlar_degerli.json"
    
    # Kartları işle
    kartlari_isle(json_dosyasi, cikti_dosyasi)
