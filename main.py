import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image, ImageTk

class SketchBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook")
  
        self.canvas = tk.Canvas(root, bg="white", width=100, height=400)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.setup_menu() 
        self.setup_color_button()
        self.setup_save_button()
        self.setup_bg_color_button()
        self.setup_import_image_button()
        self.setup_erase_button()
        self.setup_delete_button()

        self.prev_x = None
        self.prev_y = None
        self.drawing_color = "black"
        self.bg_color = "white"
        self.erasing = False

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def setup_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_drawing)
        file_menu.add_command(label="Exit", command=self.root.destroy)

    def setup_color_button(self):
        color_button = tk.Button(self.root, text="Select Color", command=self.choose_color)
        color_button.pack(side=tk.LEFT, padx=5, pady=5)

    def setup_save_button(self):
        save_button = tk.Button(self.root, text="Save Drawing", command=self.save_drawing)
        save_button.pack(side=tk.LEFT, padx=5, pady=5)

    def setup_bg_color_button(self):
        bg_color_button = tk.Button(self.root, text="Select BG Color", command=self.choose_bg_color)
        bg_color_button.pack(side=tk.LEFT, padx=5, pady=5)

    def setup_import_image_button(self):
        import_image_button = tk.Button(self.root, text="Import Image", command=self.import_image)
        import_image_button.pack(side=tk.LEFT, padx=5, pady=5)

    def setup_erase_button(self):
        self.erase_button = tk.Button(self.root, text="Erase", command=self.toggle_erase)
        self.erase_button.pack(side=tk.LEFT, padx=5, pady=5)

    def setup_delete_button(self):
        delete_button = tk.Button(self.root, text="Delete Canvas", command=self.delete_canvas)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

    def choose_color(self):
        color = colorchooser.askcolor(title="Select Color")
        if color[1]:
            self.drawing_color = color[1]

    def choose_bg_color(self):
        bg_color = colorchooser.askcolor(title="Select Background Color")
        if bg_color[1]:
            self.bg_color = bg_color[1]
            self.canvas.configure(bg=self.bg_color)

    def import_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image = Image.open(file_path)
            self.bg_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

    def toggle_erase(self):
        self.erasing = not self.erasing
        if self.erasing:
            self.canvas.configure(cursor="dotbox")
            self.erase_button.config(text="Drawing")  
        else:
            self.canvas.configure(cursor="")
            self.erase_button.config(text="Erase")  

    def paint(self, event):
        x, y = event.x, event.y

        if self.prev_x and self.prev_y:
            if self.erasing:
                self.canvas.create_line(self.prev_x, self.prev_y, x, y, width=10, fill=self.bg_color)
            else:
                self.canvas.create_line(self.prev_x, self.prev_y, x, y, width=2, fill=self.drawing_color)

        self.prev_x = x
        self.prev_y = y

    def reset(self, event):
        self.prev_x = None
        self.prev_y = None

    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas.postscript(file=file_path, colormode='color')

    def delete_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    sketchbook = SketchBook(root)
    root.mainloop()
