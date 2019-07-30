import tkinter
from PIL import Image, ImageDraw, ImageTk
import os

class Layer():
    def __init__(self, x, y, **kwargs):
        self.x = x
        self.y = y

        if "file" in kwargs:
            self.name = os.path.basename(kwargs["file"])
            self.image = Image.open(kwargs["file"])
            if self.image.format != "RGBA":
                self.image.convert("RGBA")
        else:
            self.name = kwargs["name"]
            self.image = Image.new("RGBA", (kwargs["width"], kwargs["height"]), (255, 255, 255, 0))
        self.width, self.height = self.image.size
    
    def apply(self, image):
        self.image.alpha_composite(image)

class DrawCanvas(tkinter.Canvas):
    layers = []
    layerindex = 0

    def __init__(self, master, **kwargs):
        if "file" in kwargs:
            self.layers.append(Layer(0, 0, file=kwargs["file"]))
        else:
            self.layers.append(Layer(0, 0, name="Background", width=kwargs["width"], height=kwargs["height"]))
        self.canvaswidth = self.layers[0].width
        self.canvasheight = self.layers[0].height

        super().__init__(master, width=self.canvaswidth, height=self.canvasheight, bg="gray")

        for x in range(self.canvaswidth // 16 + 1):
            for y in range(self.canvasheight // 16 + 1):
                self.create_rectangle(x * 16, y * 16, x * 16 + 8, y * 16 + 8, fill="white", width=0, tags="background")
                self.create_rectangle(x * 16 + 8, y * 16 + 8, (x + 1) * 16, (y + 1) * 16, fill="white", width=0, tags="background")

        self.update_image()

    def update_image(self):
        self.delete("image")
        for i in self.layers:
            self.imagetk = ImageTk.PhotoImage(i.image)
            self.create_image(i.x, i.y, image=self.imagetk, anchor="nw", tags="image")

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("ペイント")
        self.canvas = DrawCanvas(self, file="./poland.png")
        self.canvas.pack()

app = App()
app.mainloop()