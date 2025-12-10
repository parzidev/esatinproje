import os
import json
import argparse
import time
from tqdm import tqdm

# Kart bilgilerini çekme ve işleme modülleri
from kart_degerlerini_ekle_v2 import kartlari_isle
from nadirligi_ekle import nadirligi_ekle

def main():
    parser = argparse.ArgumentParser(description="Kart bilgilerini hazırlama aracı")
    parser.add_argument("--input", default="kartlar_detayli.json", 
                        help="Giriş JSON dosyası (varsayılan: kartlar_detayli.json)")
    parser.add_argument("--output", default="kartlar_tam.json", 
                        help="Çıkış JSON dosyası (varsayılan: kartlar_tam.json)")
    parser.add_argument("--skip-values", action="store_true",
                        help="Energy, power ve might değerlerini atlamak için")
    parser.add_argument("--skip-rarity", action="store_true",
                        help="Nadirlik bilgisini atlamak için")
    
    args = parser.parse_args()
    
    print("Kart bilgileri hazırlanıyor...")
    
    # Giriş dosyası mevcut değilse, offline JSON oluştur
    if not os.path.exists(args.input):
        print(f"'{args.input}' dosyası bulunamadı. Offline JSON oluşturuluyor...")
        os.system("python offline_json_olustur.py")
        args.input = "kartlar_offline.json"
    
    # Ara dosya
    ara_dosya = "kartlar_degerli_temp.json"
    
    # Kartları işle (energy, power, might değerleri)
    if not args.skip_values:
        print("Energy, power ve might değerleri ekleniyor...")
        kartlari_isle(args.input, ara_dosya)
    else:
        ara_dosya = args.input
    
    # Nadirlik bilgisini ekle
    if not args.skip_rarity:
        print("Nadirlik bilgisi ekleniyor...")
        nadirligi_ekle(ara_dosya, args.output)
    elif args.skip_values:
        # Hem değerler hem de nadirlik atlanırsa, giriş dosyasını çıkış dosyasına kopyala
        with open(args.input, "r", encoding="utf-8") as f_in:
            with open(args.output, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())
        print(f"Dosya kopyalandı: {args.input} -> {args.output}")
    else:
        # Sadece nadirlik atlanırsa, ara dosyayı çıkış dosyasına kopyala
        with open(ara_dosya, "r", encoding="utf-8") as f_in:
            with open(args.output, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())
        print(f"Dosya kopyalandı: {ara_dosya} -> {args.output}")
    
    # Geçici dosyayı temizle
    if os.path.exists(ara_dosya) and ara_dosya != args.input and ara_dosya != args.output:
        os.remove(ara_dosya)
    
    print("İşlem tamamlandı.")

if __name__ == "__main__":
    main()
