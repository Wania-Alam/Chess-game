import tkinter as tk
from PIL import Image, ImageTk 
from Chess_game_1_player import ChessGUI  as ChessGUI1P
from Chess_game_2_players import ChessGUI as ChessGUI2P
import os


class MainScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game - Main Screen")
        self.root.geometry("600x500+400+100")
        self.root.resizable(False,False)
        background_image = "Assets/images/background.jpg"
        self.background_canvas = self.set_background_image(background_image)
        self.create_widgets()

    def set_background_image(self, image_path):
        # Load and resize the image
        image = Image.open(image_path)
        resized_image = image.resize((600, 500), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)

        # Create a canvas widget
        background_canvas = tk.Canvas(self.root, width=500, height=500)
        background_canvas.pack(fill='both', expand=True)

        # Set the image as the background
        background_canvas.create_image(0, 0, image=self.photo, anchor='nw')

        # Keep a reference to the canvas
        return background_canvas
    
    def create_widgets(self):
        # Add title text on the canvas
        self.background_canvas.create_text(150, 50, text="Chess", font=("Helvetica",50), fill="white")
        self.background_canvas.create_text(170, 110, text="Choose Game Mode:", font=("Helvetica", 18), fill="white")

        #Button for 1 Player mode
        one_player_button = tk.Button(self.root, text="1 Player", font=("Helvetica", 16), bg="gray", command=self.start_one_player)
        self.background_canvas.create_window(100, 170, window=one_player_button)

        #Button for 2 Players mode
        two_player_button = tk.Button(self.root, text="2 Players", font=("Helvetica", 16),bg="gray", command=self.start_two_player)
        self.background_canvas.create_window(100, 230, window=two_player_button)

    def start_one_player(self):
        # Open 1 Player game mode
        self.clear_screen()
        ChessGUI1P(self.root)  # Load the 1-player chess game GUI

    def start_two_player(self):
        # Open 2 Player game mode
        self.clear_screen()
        ChessGUI2P(self.root)  # Load the 2-player chess game GUI

    def clear_screen(self):
        # Clears the main screen widgets before loading the game screen
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainScreen(root)
    root.mainloop()
