import os
import json
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.simpledialog as simpledialog

class MemeCreatorApp:
    def __init__(self, root, save_folder):
        self.root = root
        self.root.title("Meme Creator - JSON Data and Image Save")

        self.save_folder = os.path.abspath(save_folder)
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        self.image_path = ""
        self.text_areas = []
        self.canvas = None
        self.image_data = {}
        self.resized_image = None

        self.json_file_path = os.path.join(self.save_folder, "image_data.json")
        self.load_existing_data()

        self.open_button = Button(self.root, text="Open Image", command=self.open_image)
        self.open_button.pack(pady=10)

        self.canvas = Canvas(self.root, width=550, height=450)
        self.canvas.pack(padx=10, pady=10)

        self.save_button = Button(self.root, text="Save Data and Image", command=self.save_data_and_image)
        self.save_button.pack(pady=10)

        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        self.rect = None
        self.start_x = None
        self.start_y = None
    def load_existing_data(self):
        """Load existing JSON data if available"""
        try:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r') as f:
                    self.image_data = json.load(f)
            else:
                self.image_data = {}
        except json.JSONDecodeError as e:
            print(f"Error loading existing data: {e}")
            self.image_data = {}

    def open_image(self):
        self.text_areas.clear()
        self.canvas.delete("all")

        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image_path = file_path
            # Only initialize boxes if image path doesn't exist in data
            if self.image_path not in self.image_data:
                self.image_data[self.image_path] = {"boxes": []}
            else:
                # Load existing boxes for this image
                self.text_areas = [(box["coords"][0], box["coords"][1], 
                                  box["coords"][2], box["coords"][3], 
                                  box["area"]) for box in self.image_data[self.image_path]["boxes"]]
            self.show_image_on_canvas()
            # Draw existing boxes if any
            self.draw_existing_boxes()
    def draw_existing_boxes(self):
        """Draw existing boxes when loading an image"""
        for x1, y1, x2, y2, _ in self.text_areas:
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

    def show_image_on_canvas(self):
        try:
            img = Image.open(self.image_path)
            self.resized_image = img.resize((550, 450), Image.ANTIALIAS)
            self.image_tk = ImageTk.PhotoImage(self.resized_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)
        except Exception as e:
            print(f"Error loading image: {e}")

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def draw_rectangle(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def end_draw(self, event):
        if self.rect:
            x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            area = width * height
            self.text_areas.append((x1, y1, x2, y2, area))
            self.image_data[self.image_path]["boxes"].append({"coords": (x1, y1, x2, y2), "area": area})
            self.rect = None

    def save_data_and_image(self):
        if self.resized_image and self.image_data:
            # Update existing JSON file
            try:
                with open(self.json_file_path, "w") as f:
                    json.dump(self.image_data, f, indent=4)
                print(f"Data updated in {self.json_file_path}")

                image_name = simpledialog.askstring("Save Image", "Enter the name for the image (without extension):")
                if image_name:
                    image_name += ".png"
                    image_path = os.path.join(self.save_folder, image_name)
                    self.resized_image.save(image_path)
                    print(f"Resized image saved to {image_path}")
            except Exception as e:
                print(f"Error saving data: {e}")
        else:
            print("No resized image or data to save.")

if __name__ == "__main__":
    save_folder = "Desktop/meme generator/PO"
    root = Tk()
    app = MemeCreatorApp(root, save_folder)
    root.mainloop()