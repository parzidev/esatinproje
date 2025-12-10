import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# === Selenium ayarları ===
chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı gizli çalıştır
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://piltoverarchive.com/cards")
time.sleep(5)  # sayfanın yüklenmesi için bekle

# === Tüm kartları bul ===
cards = driver.find_elements(By.CSS_SELECTOR, "div.group img")

print(f"{len(cards)} kart bulundu.")

for idx, card in enumerate(cards, start=1):
    try:
        # Kart ismi
        name = card.get_attribute("alt").strip()
        
        # Kart görseli
        img_url = card.get_attribute("src")
        
        # Kartı açmak için tıkla
        driver.execute_script("arguments[0].click();", card)
        time.sleep(1.5)

        # Badge'leri al
        badges = driver.find_elements(By.CSS_SELECTOR, "span[data-slot='badge'] span")
        badge_names = [b.text.strip() for b in badges if b.text.strip()]

        # Eğer badge yoksa "Unknown" ata
        folder = badge_names[0] if badge_names else "Unknown"
        folder = folder.replace(" ", "_")

        # Klasör oluştur
        os.makedirs(folder, exist_ok=True)

        # Resim kaydet
        img_data = requests.get(img_url).content
        file_path = os.path.join(folder, f"{name}.webp")
        with open(file_path, "wb") as f:
            f.write(img_data)

        print(f"[{idx}] {name} -> {folder}/")

        # Kart detayını kapat
        close_btn = driver.find_element(By.CSS_SELECTOR, "button[data-slot='dialog-close']")
        driver.execute_script("arguments[0].click();", close_btn)
        time.sleep(0.5)

    except Exception as e:
        print(f"Hata: {e}")
        continue

driver.quit()
