import PySimpleGUI as sg
import time 
layout = [
    [sg.Text("Lütfen PNG resminizi yükleyin:")],
    [sg.Input(key="-FILE-", enable_events=True, change_submits=True),
     sg.FilesBrowse(file_types=(("PNG Files", "*.png"),))],
    [sg.Button("Resmi İşle", key="-PROCESS-")],
    [sg.ProgressBar(100, orientation='h', size=(40, 20), key="-PROGRESS-")],
    [sg.Text("Yemek önerileri:")],
    [sg.Multiline(size=(50, 10), key="-OUTPUT-")],
]

window = sg.Window("Yemek Öneri AI", layout)

while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:
        break

    if event == "-PROCESS-":
        file_path = values["-FILE-"]
        if not file_path:
            sg.popup("Lütfen bir dosya seçin veya sürükleyin!")
            continue

        window["-PROGRESS-"].update_bar(0)
        
        # Görüntü işleme burada yapılacak file path AI'ya iletilcek
        for i in range(101):
            time.sleep(0.02)  
            window["-PROGRESS-"].update_bar(i)
        
        # AI dan gelen output suggestiona yazılacak.
        suggestion = "Bugün: Bol yeşillikli salata ve ızgara tavuk öneriliyor!"
        window["-OUTPUT-"].update(suggestion)

window.close()
