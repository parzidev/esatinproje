import json
import os
import re
from PIL import Image
import io

def kart_tipine_gore_deger_ata(kart):
    """Kart tipine göre varsayılan değerler atar"""
    tip = kart.get("tip", "")
    
    # Varsayılan değerler
    energy = "0"
    power = "0"
    might = "0"
    
    # Kart tipine göre değerleri ayarla
    if tip == "Unit" or tip == "Champion Unit" or tip == "Token Unit" or tip == "Signature Unit":
        # Birimler genellikle energy ve power değerlerine sahiptir
        energy = "1"  # Varsayılan enerji değeri
        power = "1"   # Varsayılan güç değeri
        might = "2"   # Varsayılan might değeri
    elif tip == "Spell" or tip == "Signature Spell":
        # Büyüler genellikle sadece energy değerine sahiptir
        energy = "1"  # Varsayılan enerji değeri
        power = "0"   # Büyülerin genellikle gücü yoktur
        might = "1"   # Varsayılan might değeri
    elif tip == "Gear":
        # Ekipmanlar genellikle enerji ve might değerlerine sahiptir
        energy = "1"  # Varsayılan enerji değeri
        power = "0"   # Ekipmanların genellikle gücü yoktur
        might = "2"   # Varsayılan might değeri
    elif tip == "Battlefield":
        # Savaş alanları genellikle might değerine sahiptir
        energy = "0"  # Savaş alanlarının genellikle enerji maliyeti yoktur
        power = "0"   # Savaş alanlarının genellikle gücü yoktur
        might = "3"   # Varsayılan might değeri
    elif tip == "Basic Rune":
        # Runeler genellikle might değerine sahiptir
        energy = "0"  # Runelerin genellikle enerji maliyeti yoktur
        power = "0"   # Runelerin genellikle gücü yoktur
        might = "2"   # Varsayılan might değeri
    elif tip == "Legend":
        # Legend kartları genellikle yüksek değerlere sahiptir
        energy = "3"  # Varsayılan enerji değeri
        power = "3"   # Varsayılan güç değeri
        might = "5"   # Varsayılan might değeri
    
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
    if "energy" not in kart:
        kart["energy"] = energy
    if "power" not in kart:
        kart["power"] = power
    if "might" not in kart:
        kart["might"] = might
    
    return kart

def dosya_adina_gore_deger_ata(kart):
    """Dosya adından ipuçları alarak değerleri atar"""
    dosya_yolu = kart.get("dosya_yolu", "")
    
    # Dosya adından sayıları çıkar
    sayilar = re.findall(r'\d+', os.path.basename(dosya_yolu))
    
    # Sayılar varsa ve 1-10 arasındaysa, bunları değer olarak kullan
    if sayilar:
        for sayi in sayilar:
            sayi_int = int(sayi)
            if 0 <= sayi_int <= 10:
                # İlk sayıyı energy, ikinci sayıyı power, üçüncü sayıyı might olarak ata
                if "energy" not in kart:
                    kart["energy"] = str(sayi_int)
                elif "power" not in kart:
                    kart["power"] = str(sayi_int)
                elif "might" not in kart:
                    kart["might"] = str(sayi_int)
    
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
            # Kart tipine göre değerleri ata
            kart = kart_tipine_gore_deger_ata(kart)
            
            # Dosya adına göre değerleri ata
            kart = dosya_adina_gore_deger_ata(kart)
            
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
            print(f"{kart.get('isim', 'Bilinmeyen')} - Energy: {kart.get('energy', 'N/A')}, Power: {kart.get('power', 'N/A')}, Might: {kart.get('might', 'N/A')}")
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    # Mevcut JSON dosyası
    json_dosyasi = "kartlar_detayli.json"
    
    # Çıktı dosyası
    cikti_dosyasi = "kartlar_degerli.json"
    
    # Kartları işle
    kartlari_isle(json_dosyasi, cikti_dosyasi)
