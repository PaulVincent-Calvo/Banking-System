import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class GifAnimator:
    def __init__(self, root, gif_path, screen_width, screen_height):
        self.root = root
        self.root.title("Treasury Citadel")
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
        self.canvas.pack()

        # Load the gif image and store the frames
        self.gif = Image.open(gif_path)
        self.frames = [ImageTk.PhotoImage(image) for image in ImageSequence.Iterator(self.gif)]

        # Setting the initial counter
        self.counter = 0

    # Get the current frame and display it on the canvas
    def animate(self):
        frame = self.frames[self.counter]
        self.canvas.delete("all")
        self.canvas.create_image(screen_width//2, screen_height//2, image=frame)

        # Increment the counter and wrap it around if it reaches the end
        self.counter = (self.counter + 1) % len(self.frames)

        # Check if counter has reached the last frame
        if self.counter == len(self.frames) - 1:
            self.root.after(50, self.action_after) # Schedule a function after it reaches last frame (Should be used for calling a function for switching pages for Login Page)
        else:
            self.root.after(50, self.animate)

    # Function to be executed after last frame (Should be changed)
    def action_after(self):
        print("Done")

# Screen width and height
screen_width = 560
screen_height = 343

root = tk.Tk()
animator = GifAnimator(root, r"C:\Users\SSD\Desktop\login_assets\frame0\LoadingSplash.gif", screen_width, screen_height) # Change the path from where LoadingSplash.gif is located

# Start the animation
animator.animate()
root.mainloop()