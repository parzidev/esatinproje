# Kart Tahmin Oyunu

Bu proje, Legends of Runeterra kartları için Loldle benzeri bir tahmin oyunudur.

## Nasıl Oynanır?

1. `index.html` dosyasını bir web tarayıcısında açın.
2. Arama çubuğuna bir kart ismi yazın.
3. Tahmininizi yapın ve ipuçlarını takip edin:
   - **Yeşil**: Tam eşleşme.
   - **Kırmızı**: Eşleşme yok.
   - **Turuncu**: Kısmi eşleşme (Tip için).
   - **Oklar (↑/↓)**: Sayısal değerin daha yüksek veya daha düşük olması gerektiğini gösterir.

## Dosyalar

- `index.html`: Oyunun ana sayfası.
- `style.css`: Oyunun tasarımı (Karanlık tema).
- `script.js`: Oyun mantığı.
- `kartlar_tam.json`: Kart verileri.

## Notlar

- Oyunun düzgün çalışması için `kartlar_tam.json` dosyasının `index.html` ile aynı klasörde olması gerekir.
- Kart resimleri `Unit`, `Spell` vb. klasörler altında aranır. Eğer resim bulunamazsa gri bir kutu gösterilir.
