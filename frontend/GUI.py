import PySimpleGUI as sg
import time
import sys
import os

# Backend dosyasını içeri aktar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
import yolotogpt as ytg

# Tema ayarı
sg.theme("DarkGrey13")

# Logo yolu
script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir, "Logo.ico")

# Seçilen dosyalar listesi
selected_images = []

# Font ayarları
FONT_LARGE = ("Helvetica", 18)
FONT_MEDIUM = ("Helvetica", 16)
FONT_SMALL = ("Helvetica", 14)
FONT_XSMALL = ("Helvetica", 12)

# Sol sütun (Dosya seçimi, liste, butonlar)
left_column = [
    [sg.Text("Lütfen resimlerinizi yükleyin:", font=FONT_LARGE)],
    [
        sg.Input(key="-FILE-", enable_events=True, visible=False),
        sg.FilesBrowse("PNG Ara", file_types=(("PNG Files", "*.png"),), size=(20, 2), font=FONT_MEDIUM)
    ],
    [
        sg.Text("Seçilecek dosya:", font=FONT_SMALL),
        sg.Text("", key="-FILENAME-", size=(60, 1), font=FONT_XSMALL)
    ],
    [sg.Button("Seç", key="-SELECT-", size=(12, 2), font=FONT_MEDIUM)],
    [sg.Text("Seçilen dosyalar:", font=FONT_LARGE)],
    [sg.Listbox(values=selected_images, size=(50, 12), key="-LIST-", font=FONT_MEDIUM, expand_x=True)],
    [sg.Button("Öneri Al", key="-PROCESS-", size=(14, 2), font=FONT_MEDIUM, disabled=True)]
]

# İlerleme çubuğu
middle_column = [
    [sg.ProgressBar(100, orientation='v', size=(30, 30), key="-PROGRESS-")]
]

# Sağ sütun (Tarif önerileri)
right_column = [
    [sg.Text("Yemek Önerileri:", font=FONT_LARGE)],
    [sg.Multiline("", size=(50, 25), key="-OUTPUT-", font=FONT_MEDIUM, disabled=True, border_width=3)]
]

# Ana Layout (3 sütun)
layout = [
    [
        sg.Column(left_column, vertical_alignment='top'),
        sg.Column(middle_column, vertical_alignment='top'),
        sg.Column(right_column, vertical_alignment='top')
    ]
]

# Pencere oluştur
window = sg.Window("PickDish", layout, size=(1350, 800), icon=logo_path, resizable=True)

# ✅ Ana döngü
while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:
        break
    
    if event == "-FILE-":
        window["-FILENAME-"].update(values["-FILE-"])
    
    if event == "-SELECT-":
        files = values["-FILE-"].split(";")
        new_files = [f for f in files if f and f not in selected_images]
        
        if new_files:
            selected_images.extend(new_files)
            window["-LIST-"].update(selected_images)
            window["-PROCESS-"].update(disabled=False)
    
    if event == "-PROCESS-":
        window["-PROCESS-"].update(disabled=True)
        window["-PROGRESS-"].update_bar(0)
        
        # ✅ Bar animasyonu
        for i in range(101):
            time.sleep(0.02)
            window["-PROGRESS-"].update_bar(i)
        
        # ✅ YOLO ile malzemeleri algıla
        ingredients = ytg.yolo_model(selected_images)

        if ingredients:
            # ✅ Prompt'u terminale yazdır
            print(f"\n✅ Gönderilen Prompt:\n{ingredients}")

            suggestion = ytg.tarif_uret(selected_images)

            # ✅ OpenAI cevabı terminale yazdır
            print(f"\n✅ OpenAI Yanıtı:\n{suggestion}")

            if suggestion:
                new_text = suggestion
            else:
                new_text = "Hiçbir malzeme algılanamadı."
        else:
            new_text = "Hiçbir malzeme algılanamadı."

        # ✅ Çıktıyı GUI'ye güncelle
        window["-OUTPUT-"].update(new_text)
        
        # ✅ Listeyi sıfırla
        selected_images.clear()
        window["-LIST-"].update(selected_images)
        window["-PROCESS-"].update(disabled=True)
        window["-PROGRESS-"].update_bar(0)

window.close()
