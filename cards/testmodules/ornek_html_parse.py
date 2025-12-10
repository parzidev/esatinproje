import os
import json
import re
from bs4 import BeautifulSoup

# Verilen HTML örneği
ORNEK_HTML = """
<div role="dialog" id="radix-«r121»" aria-describedby="radix-«r123»" aria-labelledby="radix-«r122»" data-state="open" data-slot="dialog-content" class="bg-background data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 fixed top-[50%] left-[50%] z-50 grid max-w-[calc(100%-2rem)] translate-x-[-50%] translate-y-[-50%] gap-4 rounded-lg border shadow-lg duration-200 sm:max-w-lg max-h-[90vh] w-full md:min-w-[50vw] md:w-[50vw] md:max-w-[95vw] overflow-y-auto p-4 pb-8 md:p-6 md:pb-12" tabindex="-1" style="pointer-events: auto;"><div data-slot="dialog-header" class="flex flex-col gap-2 text-center sm:text-left relative bg-background pb-4"><h2 id="radix-«r122»" data-slot="dialog-title" class="font-semibold text-xl md:text-2xl pr-8">Sprite</h2></div><div class="grid gap-4 md:gap-8 md:grid-cols-2"><div class="flex flex-col"><div class="relative w-full overflow-hidden rounded-[3.8%]" style="aspect-ratio: 63 / 88;"><img alt="Sprite" draggable="false" decoding="async" data-nimg="fill" class="object-contain transition-opacity duration-300" sizes="100vw" srcset="/_next/image?url=https%3A%2F%2Fcdn.piltoverarchive.com%2Fcards%2FOGN-274.webp&amp;w=640&amp;q=75 640w, /_next/image?url=https%3A%2F%2Fcdn.piltoverarchive.com%2Fcards%2FOGN-274.webp&amp;w=750&amp;q=75 750w, /_next/image?url=https%3A%2F%2Fcdn.piltoverarchive.com%2Fcards%2FOGN-274.webp&amp;w=828&amp;q=75 828w, /_next/image?url=https%3A%2F%2Fcdn.piltoverarchive.com%2Fcards%2FOGN-274.webp&amp;w=1080&amp;q=75 1080w, /_next/image?url=https%3A%2F%2Fcdn.piltoverarchive.com%2Fcards%2FOGN-274.webp&amp;w=1200&amp;q=75 1200w, /_next/image?url=https%3A%2F%2Fcdn.piltoverarchive.com%2Fcards%2FOGN-274.webp&amp;w=1920&amp;q=75 1920w, /_next/image?url=https%3A%2F%2Fcdn.piltoverarchive.com%2Fcards%2FOGN-274.webp&amp;w=2048&amp;q=75 2048w, /_next/image?url=https%3A%2F%2Fcdn.piltoverarchive.com%2Fcards%2FOGN-274.webp&amp;w=3840&amp;q=75 3840w" src="https://piltoverarchive.com/_next/image?url=https%3A%2F%2Fcdn.piltoverarchive.com%2Fcards%2FOGN-274.webp&amp;w=3840&amp;q=75" style="position: absolute; height: 100%; width: 100%; inset: 0px; color: transparent; opacity: 1;"></div></div><div class="flex flex-col overflow-y-auto pr-2 md:pr-4"><div class="space-y-6 md:space-y-8"><div class="flex flex-wrap items-center gap-2 mb-2"><span data-slot="badge" class="justify-center rounded-md border text-xs font-medium w-fit whitespace-nowrap shrink-0 [&amp;&gt;svg]:size-3 [&amp;&gt;svg]:pointer-events-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive transition-[color,box-shadow] overflow-hidden text-foreground [a&amp;]:hover:bg-accent [a&amp;]:hover:text-accent-foreground flex min-w-0 items-center gap-1.5 px-2 py-1"><img alt="Unit" draggable="false" loading="lazy" width="24" height="24" decoding="async" data-nimg="1" class="shrink-0" srcset="/_next/image?url=%2Ftypes%2Funit.webp&amp;w=32&amp;q=75 1x, /_next/image?url=%2Ftypes%2Funit.webp&amp;w=48&amp;q=75 2x" src="/_next/image?url=%2Ftypes%2Funit.webp&amp;w=48&amp;q=75" style="color: transparent;"><span class="truncate text-base font-medium">Token Unit</span></span><span data-slot="badge" class="justify-center rounded-md border text-xs font-medium w-fit whitespace-nowrap shrink-0 [&amp;&gt;svg]:size-3 [&amp;&gt;svg]:pointer-events-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive transition-[color,box-shadow] overflow-hidden text-foreground [a&amp;]:hover:bg-accent [a&amp;]:hover:text-accent-foreground flex min-w-0 items-center gap-1.5 px-2 py-1"><img alt="Common" draggable="false" loading="lazy" width="24" height="24" decoding="async" data-nimg="1" class="shrink-0" srcset="/_next/image?url=%2Frarities%2Fcommon.webp&amp;w=32&amp;q=75 1x, /_next/image?url=%2Frarities%2Fcommon.webp&amp;w=48&amp;q=75 2x" src="/_next/image?url=%2Frarities%2Fcommon.webp&amp;w=48&amp;q=75" style="color: transparent;"><span class="truncate text-base font-medium">Common</span></span></div><div class="flex flex-wrap gap-2 mb-4"><span data-slot="badge" class="inline-flex items-center justify-center rounded-md border px-2 py-0.5 font-medium w-fit whitespace-nowrap shrink-0 [&amp;&gt;svg]:size-3 gap-1 [&amp;&gt;svg]:pointer-events-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive transition-[color,box-shadow] overflow-hidden border-transparent bg-secondary text-secondary-foreground [a&amp;]:hover:bg-secondary/90 text-sm">Fae</span></div><div class="grid grid-cols-3 gap-6 rounded-lg bg-zinc-800/50 p-4"><div class="space-y-1 text-center"><span class="text-sm text-zinc-400">Energy</span><div class="text-3xl font-bold">0</div></div><div class="space-y-1 text-center"><span class="text-sm text-zinc-400">Power</span><div class="text-3xl font-bold">0</div></div><div class="space-y-1 text-center"><span class="text-sm text-zinc-400">Might</span><div class="text-3xl font-bold">3</div></div></div><div class="space-y-2"><h3 class="text-lg font-medium">Description</h3><p class="text-base text-zinc-300 whitespace-pre-wrap leading-relaxed"><span class="inline-block px-2 py-0.5 mx-0.5 my-[-2px] transform -skew-x-12" style="background-color: rgb(147, 173, 47); color: rgb(0, 0, 0); font-weight: bold; border-radius: 0px;">TEMPORARY</span> <span class="italic">(Kill me at the start of your Beginning Phase, before scoring.)</span></p></div></div><div class="mt-auto space-y-8 pt-8"><div class="space-y-2"><h3 class="text-lg font-medium">Flavor Text</h3><p class="text-base italic text-zinc-400">Dreams rarely linger, but the dreamer is still changed.</p></div><div class="rounded-lg bg-zinc-800/50 p-4"><h3 class="mb-3 text-lg font-medium">Card Information</h3><div class="space-y-2 text-sm text-zinc-400"><p class="flex items-center gap-2"><span class="font-medium">Artist:</span>Envar Studio</p><p class="flex items-center gap-2"><span class="font-medium">Set:</span>Origin</p><p class="flex items-center gap-2"><span class="font-medium">Card Number:</span>OGN-274</p></div></div></div></div></div><button type="button" data-slot="dialog-close" class="ring-offset-background focus:ring-ring data-[state=open]:bg-accent data-[state=open]:text-muted-foreground absolute top-4 right-4 rounded-xs opacity-70 transition-opacity hover:opacity-100 focus:ring-2 focus:ring-offset-2 focus:outline-hidden disabled:pointer-events-none [&amp;_svg]:pointer-events-none [&amp;_svg]:shrink-0 [&amp;_svg:not([class*='size-'])]:size-4"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x" aria-hidden="true"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg><span class="sr-only">Close</span></button></div>
"""

def ornek_html_parse():
    """Verilen HTML örneğinden kart bilgilerini çıkarır"""
    soup = BeautifulSoup(ORNEK_HTML, 'html.parser')
    
    # Kart bilgilerini topla
    kart_bilgisi = {}
    
    # Kart ismi
    title_element = soup.select_one("h2[data-slot='dialog-title']")
    if title_element:
        kart_bilgisi["isim"] = title_element.get_text().strip()
    
    # Kart tipi ve nadir seviyesi
    badges = soup.select("span[data-slot='badge'] span.truncate")
    badge_texts = [b.get_text().strip() for b in badges if b.get_text().strip()]
    
    if len(badge_texts) >= 1:
        kart_bilgisi["tip"] = badge_texts[0]
    if len(badge_texts) >= 2:
        kart_bilgisi["nadir"] = badge_texts[1]
        
    # Fae gibi etiketler
    tags = soup.select("span[data-slot='badge'].inline-flex")
    if tags:
        kart_bilgisi["etiketler"] = [tag.get_text().strip() for tag in tags if tag.get_text().strip()]
    
    # Energy, Power, Might değerleri
    stats_div = soup.select_one("div.grid.grid-cols-3")
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
    description_div = soup.select_one("div.space-y-2 p.text-base.text-zinc-300")
    if description_div:
        kart_bilgisi["aciklama"] = description_div.get_text().strip()
        
    # Flavor text
    flavor_div = soup.select_one("div.space-y-2 p.text-base.italic.text-zinc-400")
    if flavor_div:
        kart_bilgisi["flavor_text"] = flavor_div.get_text().strip()
        
    # Kart bilgileri (Artist, Set, Card Number)
    info_div = soup.select_one("div.rounded-lg.bg-zinc-800\\/50 div.space-y-2")
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
    img_element = soup.select_one("img[alt='" + kart_bilgisi["isim"] + "']")
    if img_element and 'src' in img_element.attrs:
        kart_bilgisi["gorsel_url"] = img_element['src']
        
        # Kart numarasını URL'den çıkarmaya çalış
        if "kart_numarasi" not in kart_bilgisi:
            url_match = re.search(r'cards%2F([A-Z0-9-]+)\.webp', img_element['src'])
            if url_match:
                kart_bilgisi["kart_numarasi"] = url_match.group(1)
    
    return kart_bilgisi

def mevcut_klasorler_ile_eslestir(kart_bilgisi):
    """Kart bilgisini mevcut klasörlerle eşleştirir"""
    # Klasör adını tip bilgisinden tahmin et
    tip = kart_bilgisi.get("tip", "")
    
    if tip == "Unit":
        kart_bilgisi["klasor"] = "Unit"
    elif tip == "Token Unit":
        kart_bilgisi["klasor"] = "Token_Unit"
    elif tip == "Token Card":
        kart_bilgisi["klasor"] = "Token_Card"
    elif tip == "Spell":
        kart_bilgisi["klasor"] = "Spell"
    elif tip == "Signature Unit":
        kart_bilgisi["klasor"] = "Signature_Unit"
    elif tip == "Signature Spell":
        kart_bilgisi["klasor"] = "Signature_Spell"
    elif tip == "Gear":
        kart_bilgisi["klasor"] = "Gear"
    elif tip == "Legend":
        kart_bilgisi["klasor"] = "Legend"
    elif tip == "Champion Unit":
        kart_bilgisi["klasor"] = "Champion_Unit"
    elif tip == "Battlefield":
        kart_bilgisi["klasor"] = "Battlefield"
    elif tip == "Basic Rune":
        kart_bilgisi["klasor"] = "Basic_Rune"
    else:
        kart_bilgisi["klasor"] = "Unknown"
    
    return kart_bilgisi

def json_olustur(kart_bilgisi):
    """Kart bilgisini JSON dosyasına kaydeder"""
    with open("ornek_kart.json", "w", encoding="utf-8") as f:
        json.dump(kart_bilgisi, f, ensure_ascii=False, indent=4)
    print("Kart bilgisi JSON dosyasına kaydedildi.")

if __name__ == "__main__":
    print("HTML örneğinden kart bilgileri çıkarılıyor...")
    kart_bilgisi = ornek_html_parse()
    
    print("Kart bilgisi klasörlerle eşleştiriliyor...")
    kart_bilgisi = mevcut_klasorler_ile_eslestir(kart_bilgisi)
    
    print("JSON dosyası oluşturuluyor...")
    json_olustur(kart_bilgisi)
    
    print("İşlem tamamlandı.")
    print("Kart bilgileri:", json.dumps(kart_bilgisi, ensure_ascii=False, indent=4))
