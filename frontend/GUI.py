import PySimpleGUI as sg
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
import yolotogpt as ytg
sg.theme("DarkGrey13")

# GUI.py dosyasının bulunduğu klasör ile aynı klasöre dinamik erişim.
#Tüm UI imageları GUI.py ile aynı directorye konulacak.
script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir, "Logo.ico")



selected_images = []

# Font büyüklükleri artırıldı. Son commit
FONT_LARGE = ("Helvetica", 18)
FONT_MEDIUM = ("Helvetica", 16)
FONT_SMALL = ("Helvetica", 14)
FONT_XSMALL = ("Helvetica", 12)
#SOL SÜTUN (Dosya seçimi, liste, butonlar)
left_column = [
    [sg.Text("Lütfen resimlerinizi yükleyin:", font=FONT_LARGE, pad=((0,0),(0,20)))],
    [
        sg.Input(key="-FILE-", enable_events=True, visible=False),
        sg.FilesBrowse("PNG Ara", file_types=(("PNG Files", "*.png"),), size=(20, 2), font=FONT_MEDIUM)
    ],
    [
        sg.Text("Seçilecek dosya:", font=FONT_SMALL, pad=((0,5),(10,10))),
        sg.Text("", key="-FILENAME-", size=(60, 1), font=FONT_XSMALL)
    ],
    [sg.Button("Seç", key="-SELECT-", size=(12, 2), font=FONT_MEDIUM, pad=((0,0),(10,20)))],
    [sg.Text("Şu resimleri seçtiniz:", font=FONT_LARGE, pad=((0,0),(20,10)))],
    [sg.Listbox(values=selected_images, size=(50, 12), key="-LIST-", font=FONT_MEDIUM, expand_x=True)],
    [sg.Button("Öneri Al", key="-PROCESS-", size=(14, 2), font=FONT_MEDIUM, disabled=True, pad=((0,0),(20,20)))]
]

# Progress bar
middle_column = [
    [sg.ProgressBar(100, orientation='v', size=(30, 30), key="-PROGRESS-", pad=((20,20),(20,20)), expand_y=True)]
]

#SAĞ SÜTUN (Yemek önerileri) 
right_column = [
    [sg.Text("Yemek Önerileri:", font=FONT_LARGE, justification="center", pad=((0,0),(0,20)))],
    [sg.Multiline("", size=(50, 25), key="-OUTPUT-", font=FONT_MEDIUM, disabled=True, border_width=3)]
]

# Ana layout'u 3 sütun şeklinde tanımladom.
layout = [
    [
        sg.Column(left_column, vertical_alignment='top', element_justification='left', expand_y=True),
        sg.Column(middle_column, vertical_alignment='top', element_justification='center', expand_y=True),
        sg.Column(right_column, vertical_alignment='top', element_justification='center', expand_y=True),
    ]
]

window = sg.Window("PickDish", layout, size=(1350, 800), icon=logo_path, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    if event == "-FILE-":
        window["-FILENAME-"].update(values["-FILE-"])

    if event == "-SELECT-":
        if not values["-FILE-"]:
            sg.popup("Hiçbir dosya seçilmedi!", title="Uyarı", font=("Helvetica", 12))
            continue

        files = values["-FILE-"].split(";")
        new_files = []
        already_selected = []

        for f in files:
            if f and f not in selected_images:
                new_files.append(f)
            elif f in selected_images:
                already_selected.append(f)

        if already_selected:
            sg.popup("Dosya zaten seçili!", title="Hata", font=("Helvetica", 12))

        if new_files:
            selected_images.extend(new_files)
            window["-LIST-"].update(selected_images)
            window["-PROCESS-"].update(disabled=False)

    if event == "-PROCESS-":
        window["-PROCESS-"].update(disabled=True)
        # bar 0lama.
        window["-PROGRESS-"].update_bar(0)

        # Bar anim
        for i in range(101):
            time.sleep(0.02)
            window["-PROGRESS-"].update_bar(i)

        # YOLO çıktısı burada alınacak
        codes = ytg.yolo_model(selected_images).split()
        ingredients = [ytg.yemek_kodu_map.get(int(code), "") for code in codes]
        ingredients = [ing for ing in ingredients if ing.strip()]

        prompt = f"{', '.join(ingredients)} ürünleriyle ne tür yemekler yapabilirim tarifleri nelerdir?"
        suggestion = ytg.api_ilet(prompt)

        current_output = window["-OUTPUT-"].get().strip()
        new_text = suggestion if not current_output else current_output + "\n" + suggestion
        window["-OUTPUT-"].update(new_text)

        selected_images.clear()
        window["-LIST-"].update(selected_images)
        window["-PROCESS-"].update(disabled=True)
        window["-PROGRESS-"].update_bar(0)

window.close()