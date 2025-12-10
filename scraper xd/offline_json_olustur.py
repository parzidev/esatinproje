import os
import json
from PIL import Image
import io

# === Kart klasörleri ===
KLASORLER = [
    "Unit", "Token_Unit", "Token_Card", "Spell", "Signature_Unit", 
    "Signature_Spell", "Gear", "Legend", "Champion_Unit", "Battlefield", "Basic_Rune"
]

def offline_kart_bilgilerini_topla():
    """Mevcut klasörlerdeki kart dosyalarından temel bilgileri toplar"""
    tum_kartlar = []
    
    for klasor in KLASORLER:
        if os.path.exists(klasor):
            print(f"{klasor} klasörü taranıyor...")
            for dosya in os.listdir(klasor):
                if dosya.endswith(".webp"):
                    kart_adi = os.path.splitext(dosya)[0]
                    dosya_yolu = os.path.join(klasor, dosya)
                    
                    # Temel kart bilgilerini oluştur
                    kart_bilgisi = {
                        "isim": kart_adi,
                        "klasor": klasor,
                        "dosya_yolu": dosya_yolu
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
                    
                    # Resim boyutunu al
                    try:
                        with Image.open(dosya_yolu) as img:
                            kart_bilgisi["genislik"] = img.width
                            kart_bilgisi["yukseklik"] = img.height
                    except Exception as e:
                        print(f"  Resim boyutu alınamadı: {e}")
                    
                    tum_kartlar.append(kart_bilgisi)
                    print(f"  ✓ {kart_adi} bilgileri alındı.")
    
    return tum_kartlar

def json_olustur(kartlar):
    """Kart bilgilerini JSON dosyasına kaydeder"""
    with open("kartlar_offline.json", "w", encoding="utf-8") as f:
        json.dump(kartlar, f, ensure_ascii=False, indent=4)
    print(f"Toplam {len(kartlar)} kart bilgisi JSON dosyasına kaydedildi.")

if __name__ == "__main__":
    print("Kart bilgileri toplanıyor...")
    kartlar = offline_kart_bilgilerini_topla()
    
    print("JSON dosyası oluşturuluyor...")
    json_olustur(kartlar)
    
    print("İşlem tamamlandı.")
