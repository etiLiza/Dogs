from tkinter import*
from tkinter import messagebox as mb
import requests
from PIL import Image, ImageTk
from io import BytestIO




def show_image():
    image_url = get_dog_image()# получаем ссылку
    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img.thumbnail((300,300))
            label.config(image=img)
            label.image = img
        except Exception as e:
            mb.showerror("Ошибка", f"Возникла ошибка {e}")





window = Tk()
window.title("Картинки с собачками")
window.geometry("360*420")

label = Label()
label.pack(pady=10)

button = Button(text="Загрузить изображение", command=show_image)
button.pack(pady=10)

window.mainloop()