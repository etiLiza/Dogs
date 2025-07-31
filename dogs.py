from tkinter import*
from tkinter import ttk
from tkinter import messagebox as mb
import requests
from PIL import Image, ImageTk
from io import BytesIO

tab = 0
def get_dog_image():
    try:# так как работаем с файлами, обрабатываем исключения
        response = requests.get("https://dog.ceo/api/breeds/image/random")#прилетит json вrespons
        response.raise_for_status()# если все хорошо то получает статус 200, 404 значит статус ошибка
        data = response.json()#в дате лежит ответ в формате json
        print(data) #в дату положили ссылку json
        print(data['message'])# по ключу message получили ссылку на изображение
        print(data["status"])
        return data['message']# возвращает по ключу message ссылку на изображение
    except Exception as e:
        mb.showerror("Ошибка", f"Возникла ошибка при запросе к API  {e}")
        return None


def show_image():
    status_label.config(text="Загрузка...")
    image_url = get_dog_image()# получаем ссылку на картинку, которая возвращает в формате json наш сайт
    if image_url:# если что то не пустое то значение будет true и будет выполнятся if
        try:
            response = requests.get(image_url, stream=True)#ответ будет равен запросу получаем ответ что то загруженное по этой ссылке, т.е. картинку
            response.raise_for_status()#получаем статус ответа
            img_data = BytesIO(response.content)#загрузили по этой ссылке загрузили это изображение в двоичном коде в переменную дата
            img = Image.open(img_data)# с помощью PIL обрабатываем, получаем картинку
            img_size = (int(width_spinbox.get()),int(height_spinbox.get()))
            img.thumbnail(img_size)
            img = ImageTk.PhotoImage(img)
            #new_window = Toplevel(window)
            #new_window.title("случайное изображение")
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"Картинка №{notebook.index("end")+1}")
            print(notebook.tabs())
            label = ttk.Label(tab,image=img)
            label.image = img
            label.pack(padx=10, pady=10)
            #label.config(image=img) выводит картинку в главном окне
            status_label.config(text="")

        except Exception as e:
            mb.showerror("Ошибка", f"Возникла ошибка при загрузке изображения {e}")
    progress.stop()

def prog():# программа для запуска виджета загрузки
    progress['value'] = 0
    progress.start(30)
    window.after(3000, show_image)


def close_all_tabs():
    for tab_id in notebook.tabs():  # Получаем ID вкладок
        tab_content = notebook.nametowidget(tab_id)  # Получаем сам виджет (Frame)
        notebook.forget(tab_id)
        tab_content.destroy()  # Уничтожаем содержимое вкладки


window = Tk()
window.title("Картинки с собачками")
window.geometry("360x420")

status_label = ttk.Label(window, text="")
status_label.pack(padx=10, pady=5)

label = ttk.Label()
label.pack(pady=10)

button = ttk.Button(text="Загрузить изображение", command=prog)
button.pack(pady=10)

button2 = ttk.Button(text="Удалить все вклады из Notebook", command=close_all_tabs)
button2.pack(pady=10)

progress = ttk.Progressbar(mode="determinate", length=300)#виджет загрузки
progress.pack(pady=10)

width_label = ttk.Label(text="Ширина")
width_label.pack(side="left", padx=(0,10))# у ттк другие параметры метка будет прижата слева с отступом слева 0, справа 10
width_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side="left", padx=(0,10))
width_spinbox.set(300)

height_label = ttk.Label(text="Высота:")
height_label.pack(side="left", padx=(0,10))
height_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side="left", padx=(0,10))
height_spinbox.set(300)

top_level_window = Toplevel(window)
top_level_window.title("Изображение собачек")

notebook = ttk.Notebook(top_level_window)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

window.mainloop()