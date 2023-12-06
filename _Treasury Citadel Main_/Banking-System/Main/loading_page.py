import time
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class Loading_Page:
    def __init__(self):
        self.root = None
        self.gif_path = None
        self.screen_width = None
        self.screen_height = None
        self.canvas = None
        self.gif = None
        self.frames = None
        self.counter = None

    def initialize(self, root, gif_path, screen_width, screen_height):
        self.root = root
        self.root.title("Treasury Citadel")
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
        self.canvas.pack()

        self.gif_path = gif_path
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.gif = Image.open(self.gif_path)
        self.frames = [ImageTk.PhotoImage(image) for image in ImageSequence.Iterator(self.gif)]

        self.counter = 0

    def animate(self):
        frame = self.frames[self.counter]
        self.canvas.delete("all")
        self.canvas.create_image(self.screen_width // 2, self.screen_height // 2, image=frame)
        self.counter = (self.counter + 1) % len(self.frames)

        if self.counter == len(self.frames) - 1:
            self.root.after(50, self.action_after)
        else:
            self.root.after(50, self.animate)

    def action_after(self):
        print("Done")
        self.root.after(200, self.destroy_root)  # Schedule destruction after 0.2 seconds

    def destroy_root(self):
        self.root.destroy()

    def run_loading_page(self):
        screen_width = 560
        screen_height = 343
        root = tk.Tk()
        animator = Loading_Page()
        animator.initialize(root, r"C:\Users\ace\Downloads\OOP Recent Commits\Banking-System\gui\GUI Assets\LoadingSplash.gif", screen_width, screen_height)
        animator.animate()
        root.mainloop()
