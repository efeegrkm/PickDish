import random
import PySimpleGUI as sg
import time
import sys
import os
import threading
from io import BytesIO
from PIL import Image

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

# Küçük önizleme resmi oluşturmak için yardımcı fonksiyon
def get_thumbnail_data(image_path, size=(100, 100)):
    """
    Belirtilen dosya yolundaki resmi Pillow ile açar, belirlenen boyuta küçültür ve PNG formatında byte verisi döner.
    """
    try:
        img = Image.open(image_path)
        img.thumbnail(size)
        with BytesIO() as bio:
            img.save(bio, format="PNG")
            return bio.getvalue()
    except Exception as e:
        print(f"Önizleme oluşturulurken hata: {e}")
        return None

# Sol sütun (Dosya seçimi, liste, butonlar)
left_column = [
    [sg.Text("Lütfen resimlerinizi yükleyin:", font=FONT_LARGE)],
    [
        sg.Input(key="-FILE-", enable_events=True, visible=False),
        sg.FilesBrowse("Resim Seç", file_types=(("Image Files", "*.png;*.jpg;*.jpeg"),), size=(20, 2), font=FONT_MEDIUM)
    ],
    [
        sg.Text("Seçilecek dosya:", font=FONT_SMALL),
        sg.Text("", key="-FILENAME-", size=(60, 1), font=FONT_XSMALL)
    ],
    # Küçük önizleme için Image öğesi (veri ile güncellenecek)
    [sg.Image(key="-IMAGE_PREVIEW-", visible=False)],
    [sg.Button("Seç", key="-SELECT-", size=(12, 2), font=FONT_MEDIUM)],
    [sg.Text("Seçilen dosyalar:", font=FONT_LARGE)],
    [sg.Listbox(values=selected_images, size=(50, 12), key="-LIST-", font=FONT_MEDIUM, expand_x=True)],
    [sg.Button("Öneri Al", key="-PROCESS-", size=(14, 2), font=FONT_MEDIUM, disabled=True)]
]

# İlerleme çubuğu (expand_y ile dikeyde pencereyi kaplayacak şekilde ayarlandı)
middle_column = [
    [sg.ProgressBar(100, orientation='v', size=(100, 20), key="-PROGRESS-", expand_y=True)]
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

# Event bayrağı: progress bar'ın çalışmasını durdurmak için
stop_progress = threading.Event()

# Progress bar güncellemesini ayrı thread'de çalıştıran fonksiyon
def progress_bar_thread():
    progress_value = 0
    while not stop_progress.is_set():
        time.sleep(0.02)
        progress_value = (progress_value + random.choice([0.001, 0.01, 0.04, 0.08, 0.1, 0.5])) % 100001
        window.write_event_value("-THREAD_PROGRESS-", progress_value)
    # İşlem tamamlandığında progress bar'ı sıfırla
    window.write_event_value("-THREAD_PROGRESS-", 0)

# İşlem thread'i: YOLO ve tarif üretimini gerçekleştirir.
def processing_thread():
    global stop_progress
    stop_progress.clear()
    progress_thread = threading.Thread(target=progress_bar_thread, daemon=True)
    progress_thread.start()
    
    # Yoğun işlem: YOLO ile malzeme tespiti ve tarif üretimi
    ingredients = ytg.yolo_model(selected_images)
    if ingredients:
        print(f"\n Gönderilen Prompt:\n{ingredients}")
        suggestion = ytg.tarif_uret(selected_images)
        print(f"\n OpenAI Yanıtı:\n{suggestion}")
        result_text = suggestion if suggestion else "Hiçbir malzeme algılanamadı."
    else:
        result_text = "Hiçbir malzeme algılanamadı."
    
    stop_progress.set()
    
    window.write_event_value("-PROCESS_DONE-", result_text)

# Ana döngü
while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:
        break
    
    if event == "-FILE-":
        file_value = values["-FILE-"]
        window["-FILENAME-"].update(file_value)
        first_file = file_value.split(";")[0] if file_value else ""
        if first_file and os.path.exists(first_file):
            if first_file.lower().endswith(('.jpg', '.jpeg')):
                converted_file = ytg.convert_jpeg_to_png(first_file)
                if converted_file and os.path.exists(converted_file):
                    thumb = get_thumbnail_data(converted_file)
                    if thumb:
                        window["-IMAGE_PREVIEW-"].update(data=thumb, visible=True)
                    else:
                        window["-IMAGE_PREVIEW-"].update(visible=False)
                else:
                    window["-IMAGE_PREVIEW-"].update(visible=False)
            else:
                thumb = get_thumbnail_data(first_file)
                if thumb:
                    window["-IMAGE_PREVIEW-"].update(data=thumb, visible=True)
                else:
                    window["-IMAGE_PREVIEW-"].update(visible=False)
        else:
            window["-IMAGE_PREVIEW-"].update(visible=False)
    
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
        threading.Thread(target=processing_thread, daemon=True).start()
    
    if event == "-THREAD_PROGRESS-":
        progress_val = values["-THREAD_PROGRESS-"]
        window["-PROGRESS-"].update_bar(progress_val)
    
    if event == "-PROCESS_DONE-":
        result = values["-PROCESS_DONE-"]
        window["-OUTPUT-"].update(result)
        
        # Seçilen dosya listesini temizle
        selected_images.clear()
        window["-LIST-"].update(selected_images)
        
        # Path ve önizleme korunacak, bu yüzden aşağıdakiler kaldırıldı:
        # window["-IMAGE_PREVIEW-"].update(visible=False)
        # window["-FILENAME-"].update("")

window.close()
