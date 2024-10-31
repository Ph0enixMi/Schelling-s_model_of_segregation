from model import SchellingModel
import customtkinter as ctk
from PIL import Image, ImageTk
import os, re


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Модель Шеллинга")
        self.geometry("540x640")

        self._get_images()

        label_font = ctk.CTkFont(size=16)
        btn_font = ctk.CTkFont(size=14)

        self._size_enty = ctk.CTkEntry(self, placeholder_text="Размер", font=label_font)
        self._size_enty.grid(row=0, column=0, sticky="ew", pady=10, padx=20)

        self._iteration_enty = ctk.CTkEntry(self, placeholder_text="Итерации", font=label_font)
        self._iteration_enty.grid(row=0, column=1, sticky="ew", pady=10, padx=5)

        self._model_btn = ctk.CTkButton(self, text='Сгенерировать', font=btn_font, command=self._model_btn_click, width=10)
        self._model_btn.grid(row=0, column=2)
        
        self._image_index = 0
        self._image_label = ctk.CTkLabel(self, text='')
        self._image_label.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

        self._slider = ctk.CTkSlider(self, from_=0, to=len(self._image_files) - 1, command=self._update_image, number_of_steps=len(self._image_files) - 1)
        self._slider.grid(row=2, column=0, sticky="ew", columnspan=3, pady=10, padx=20)
        self._slider.set(0)

        self._iteration_label = ctk.CTkLabel(self, text=0, font=label_font)
        self._iteration_label.grid(row=3, column=0, sticky="ew", columnspan=3, padx=20)

        self._update_image(0)


    def _get_images(self):
        self._folder_path = "images"
        self._image_files = sorted(
            [f for f in os.listdir(self._folder_path) if f.endswith(('png', 'jpg', 'jpeg'))],
            key=lambda x: int(re.findall(r'\d+', x)[0])
        )


    def _update_image(self, value):
        self._image_index = int(value)
        self._iteration_label.configure(text=self._image_index)
        image_path = os.path.join(self._folder_path, self._image_files[self._image_index])

        image = Image.open(image_path)
        image = image.resize((500, 500))
        photo = ImageTk.PhotoImage(image)

        self._image_label.configure(image=photo)
        self._image_label.image = photo

    
    def _model_btn_click(self):
        size = self._size_enty.get()
        iteration = self._iteration_enty.get()

        try:
            model = SchellingModel(int(size), int(iteration))
            
            try:
                for _ in range(int(iteration)):
                    model.__next__()
            except StopIteration:
                pass
            
            self._get_images()
            self._slider.configure(to=len(self._image_files) - 1, number_of_steps=len(self._image_files) - 1)
            self._slider.set(0) 

        except Exception as e:
            print(f"Error: {e}")

        self._update_image(0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
