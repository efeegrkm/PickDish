import pytest
import PySimpleGUI as sg
from frontend import yolo_model, api_ilet, yemek_kodu_map 


# UnitTest: yolo_model
def test_yolo_model():
    images = ["image1.png", "image2.png"]
    result = yolo_model(images)
    assert result == "13 23 85 11", f"Beklenen sonuç: '13 23 85 11', ancak alınan sonuç: {result}"


# UnitTest: api_ilet 
def test_api_ilet():
    prompt = "elma, muz, portakal ile yemek önerileri"
    result = api_ilet(prompt)
    assert result == "Bugün: Bol yeşillikli salata ve ızgara tavuk öneriliyor!", \
        f"Beklenen sonuç: 'Bugün: Bol yeşillikli salata ve ızgara tavuk öneriliyor!', ancak alınan sonuç: {result}"


# UnitTest: yemek_kodu_map 
def test_yemek_kodu_map():
    test_codes = [0, 1, 5, 86, 44]  # Elma, Muz, Portakal, Domates, Portakal
    expected = ["elma", "muz", "portakal", "domates", "portakal"]
    
    for code, exp in zip(test_codes, expected):
        result = yemek_kodu_map.get(code, "")
        assert result == exp, f"Beklenen: {exp}, ancak alınan: {result}"


# UnitTest: Dosya seçimi ve liste güncelleme
def test_file_selection():
    values = {"-FILE-": "image1.png;image2.png"}
    selected_images = []
    
    # Dosya seçim işlemi simüle ediliyor.
    files = values["-FILE-"].split(";")
    new_files = []
    already_selected = []

    for f in files:
        if f and f not in selected_images:
            new_files.append(f)
        elif f in selected_images:
            already_selected.append(f)

    selected_images.extend(new_files)

    assert "image1.png" in selected_images
    assert "image2.png" in selected_images


# UnitTest: Progress bar güncellenmesi
def test_progress_bar_update():
    window = sg.Window("Test", [[sg.ProgressBar(100, orientation='v', size=(30, 30), key="-PROGRESS-")]])
    for i in range(101):
        window["-PROGRESS-"].update_bar(i)
        assert window["-PROGRESS-"].get() == i, f"Progress bar değeri hatalı: {i}"


# UnitTest: Output text güncellenmesi
def test_output_text_update():
    window = sg.Window("Test", [[sg.Multiline("", size=(50, 25), key="-OUTPUT-", font=("Helvetica", 16), disabled=True)]])
    
    # İlk öneriyi ekle
    window["-OUTPUT-"].update("Bugün: Bol yeşillikli salata ve ızgara tavuk öneriliyor!")#elle update.
    assert window["-OUTPUT-"].get() == "Bugün: Bol yeşillikli salata ve ızgara tavuk öneriliyor!", "İlk çıktı hatalı!"

    # Yeni öneriyi ekle
    window["-OUTPUT-"].update(window["-OUTPUT-"].get() + "\nBugün: Makarna ve sebzeler öneriliyor!")
    assert window["-OUTPUT-"].get() == "Bugün: Bol yeşillikli salata ve ızgara tavuk öneriliyor!\nBugün: Makarna ve sebzeler öneriliyor!", "Çıktı birleştirilmedi!"


# UnitTest: Öneri al butonunun aktifliği
def test_process_button_disabled():
    window = sg.Window("Test", [[sg.Button("Öneri Al", key="-PROCESS-", disabled=True)]])
    
    # Buton başlangıçta pasif olmasi lazim
    assert window["-PROCESS-"].Widget.cget("state") == "disabled", "Buton aktif durumda!"
    
    # Dosya seçildiğinde buton aktif olmasi lazm.
    window["-PROCESS-"].update(disabled=False)
    assert window["-PROCESS-"].Widget.cget("state") == "normal", "Buton hala pasif!"


if __name__ == "__main__":
    pytest.main()
