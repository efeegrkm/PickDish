import os
from ultralytics import YOLO
import openai
from dotenv import load_dotenv

# .env dosyasından OpenAI API Key yükle
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    raise ValueError("OpenAI API anahtarı yüklenemedi. .env dosyasını kontrol edin!")

# YOLO Model Yükleme
model_path = os.path.join(os.path.dirname(__file__), 'best.pt')
if not os.path.exists(model_path):
    raise FileNotFoundError(f"{model_path} dosyası bulunamadı!")

model = YOLO(model_path)

#Ürün kodlarını isimlere çeviren sözlük
yemek_kodu_map = {
    0: "elma", 1: "muz", 2: " ", 3: "tahıl gevreği", 4: "havyar", 5: "portakal", 
    6: "elma", 7: "üzüm", 8: "kuzu eti", 9: "muz", 10: "çiğ kuşbaşı dana", 
    11: "tost ekmeği", 12: "yoğurt", 13: " ", 14: " ", 15: "süt mısır", 
    16: "konserve ton balığı", 17: "havuç", 18: "bisküvi", 19: "çiğ tavuk eti", 
    20: "kırmızı toz biber", 21: "çikolatalı kek", 22: " ", 23: "zeytinyağı", 
    24: "süt mısır", 25: "mısır gevreği", 26: "balık fileto", 27: "salatalık", 
    28: "safran", 29: " ", 30: "yumurta", 31: " ", 32: " ", 33: "sarımsak?", 
    34: "zencefil", 35: " ", 36: " ", 37: " ", 38: " ", 39: " ", 40: " ", 
    41: " ", 42: " ", 43: " ", 44: "portakal", 45: " ", 46: " ", 47: " ", 
    48: " ", 49: " ", 50: "Bal", 51: "Cips", 52: "Noodle", 53: " ", 54: "zeytinyağı", 
    55: "soğan", 56: "Oreo bisküvi", 57: " ", 58: " ", 59: "makarna", 60: " ", 
    61: " ", 62: "acı biber", 63: " ", 64: "salatalık turşusu", 65: " ", 66: "Dolma Biber", 
    67: "Elma", 68: "jambon", 69: "Kuru soğan", 70: "Noodle", 71: "şarap?", 72: "pirinç pilavı", 
    73: " ", 74: "dana sosis", 75: "yosun", 76: "ıspanak?", 77: " ", 78: " ", 79: "Soya sosu", 
    80: " ", 81: "çiğ tavuk eti", 82: "çilek", 83: " ", 84: "pancar", 85: " ", 
    86: "domates", 87: "wasabi?", 88: "karpuz"
}

# YOLO Model Çıktısını Al
def yolo_model(image_paths):
    detected_items = []
    
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"Hata: '{image_path}' dosyası bulunamadı.")
            continue
        
        results = model(image_path)
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                label = yemek_kodu_map.get(cls, f"Unknown-{cls}")
                if label not in detected_items:
                    detected_items.append(label)
    
    return detected_items

# OpenAI API Çıkışı İçin Prompt Oluştur
def api_ilet(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sen bir şefsin ve yemek tarifleri konusunda uzmansın."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Tarif üretirken bir hata oluştu: {str(e)}"

# Tarif Üretimi
def tarif_uret(image_paths):
    malzemeler = yolo_model(image_paths)
    
    if not malzemeler:
        return "Hiçbir malzeme algılanamadı."

    # Açık ve net bir prompt tanımla
    prompt = f"""
Tespit edilen malzemeler şunlar: "{', '.join(malzemeler)}" OpenAI çıktısında öncelikle bu kısmı çıktıda yaz -Tespit edilen malzemeler şunlar: "{', '.join(malzemeler)}"- Ardından aşağıdaki formata göre çıktı üret
Bu malzemelerle yalnızca ve yalnızca 3 farklı tarif önerisi ver.  
Tariflerin içeriğini detaylı yaz, ancak toplamda üçten fazla tarif verme.  
Açık ve net bir şekilde detaylandır, ancak yalnızca 3 tarif istiyorum.  
Ekstra tarif veya alternatif istemiyorum.  

Format şu şekilde olmalı:
1. [Yemek Adı]  
   - Malzemeler: ...  
   - Yapılışı: ...  
2. [Yemek Adı]  
   - Malzemeler: ...  
   - Yapılışı: ...  
3. [Yemek Adı]  
   - Malzemeler: ...  
   - Yapılışı: ...  
"""

    # Prompt'u terminale bas
    print(f"\n🔎 Gönderilen Prompt:\n{prompt}")

    tarif = api_ilet(prompt)
    
    # Tarifleri terminale bas
    print("\n🔎 Üretilen Tarifler:\n")
    print(tarif)
    
    return tarif
