from PIL import Image, ImageDraw
import os


class ImageBoard:
    
    def __init__(self, matrix, image_count=0):
        self.x = 1000
        self.y = 1000

        self._n = len(matrix)
        self._matrix = matrix

        self.size_block = self.x // self._n
        self.extra_pixels = self.x % self._n

        self.image = Image.new('RGB', (self.x, self.y), self._hex_to_rgb('#242424'))
        self.draw = ImageDraw.Draw(self.image)

        self._draw_table()

        folder_path = "images"

        if image_count == 0:
            files = os.listdir(folder_path)
            for file in files:
                file_path = os.path.join(folder_path, file)

                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):
                    os.remove(file_path)

        file_name = f"{image_count}_board.png"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.image.save(os.path.join(folder_path, file_name)) 


    def _draw_table(self):
        coord_x, coord_y = 0, 0
        for i in range(self._n):
            for j in range(self._n):
                size_adjust = 1 if j < self.extra_pixels else 0
                size = self.size_block + size_adjust
                
                if self._matrix[i][j] == 0:
                    fill_color = '#242424'
                elif self._matrix[i][j] == 1:
                    fill_color = '#5948c6'
                elif self._matrix[i][j] == 2:
                    fill_color = '#b6042a'

                self.draw.rectangle(
                    [(coord_x + 2, coord_y + 2), (coord_x + size - 2, coord_y + size - 2)], 
                    fill=fill_color
                )
                coord_x += size
            coord_y += self.size_block
            coord_x = 0


    def _hex_to_rgb(self, color):
        return tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
