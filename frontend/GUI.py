import PySimpleGUI as sg
import time 

sg.theme("DarkGrey13")  # Koyu tema ayarı


def yolo_model(images):
    """YOLO modeline görüntüleri iletecek fonksiyon."""
    return "13 23 85 11"  # Örnek yemek kodları


def api_ilet(prompt):
    """OpenAI API'ye prompt iletip tarif önerisi döndüren fonksiyon."""
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

selected_images = []
layout = [
    [sg.Text("Lütfen resimlerinizi yükleyin:", font=("Helvetica", 14))],
    [sg.Input(key="-FILE-", enable_events=True, visible=False),
    sg.FilesBrowse(file_types=(("PNG Files", "*.png"),), size=(15, 1), font=("Helvetica", 12))],
    [sg.Button("Seç", key="-SELECT-", size=(15, 1), font=("Helvetica", 12))],
    [sg.Text("Şu resimleri seçtiniz:", font=("Helvetica", 14))],
    [sg.Listbox(values=selected_images, size=(60, 8), key="-LIST-", font=("Helvetica", 12))],
    [sg.Button("Resimleri İşle", key="-PROCESS-", size=(20, 1), font=("Helvetica", 12), disabled=True)],
    [sg.ProgressBar(100, orientation='h', size=(50, 20), key="-PROGRESS-")],
    [sg.Text("Yemek önerileri:", font=("Helvetica", 14))],
    [sg.Multiline(size=(60, 12), key="-OUTPUT-", font=("Helvetica", 12), disabled=True)],
]

window = sg.Window("PickDish", layout, size=(700, 600))

while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:
        break
    
    if event == "-SELECT-":
        files = values["-FILE-"].split(";")
        selected_images.extend([f for f in files if f and f not in selected_images])
        window["-LIST-"].update(selected_images)
        window["-PROCESS-"].update(disabled=len(selected_images) == 0)
    
    if event == "-PROCESS-":
        window["-PROCESS-"].update(disabled=True)
        window["-PROGRESS-"].update_bar(0)
        
        for i in range(101):
            time.sleep(0.02)
            window["-PROGRESS-"].update_bar(i)
        
        codes = yolo_model(selected_images).split()
        ingredients = [yemek_kodu_map.get(int(code), "") for code in codes]
        ingredients = [ing for ing in ingredients if ing.strip()]
        
        prompt = f"{', '.join(ingredients)} ürünleriyle ne tür yemekler yapabilirim tarifleri nelerdir?"
        suggestion = api_ilet(prompt)
        
        window["-OUTPUT-"].update(window["-OUTPUT-"].get() + "\n" + suggestion)
        
        selected_images.clear()
        window["-LIST-"].update(selected_images)
        window["-PROCESS-"].update(disabled=True)
        window["-PROGRESS-"].update_bar(0)
        
window.close()
