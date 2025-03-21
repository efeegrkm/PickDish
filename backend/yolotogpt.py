def yolo_model(images):
    return "13 23 85 11"

def api_ilet(prompt):
    return "Bugün: Bol yeşillikli salata ve ızgara tavuk öneriliyor!"

# Ürün kodlarını isimlere çeviren sözlük
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