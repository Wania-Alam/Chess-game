import tkinter as tk
from tkinter import messagebox
import chess
from PIL import Image, ImageTk
from tkinter import PhotoImage

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.root.configure(bg="#DEB887")
        self.root.geometry("640x540+100+100")
        self.board = chess.Board()
        self.selected_square = None# Initialize the selected_square attribute
        self.move_history = []  # Initialize move history
        self.current_turn = chess.WHITE  # Track the current turn
        self.white_score = 0  # Track White's score
        self.black_score = 0  # Track Black's score
        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=480, height=480)
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="w")  # Span across two columns
        self.canvas.bind("<Button-1>", self.on_click)
        self.images = {}
        self.load_images()
         
         # Set a common width for both buttons
        button_width = 10

        # New Game Button
        self.new_game_button = tk.Button(self.root,bg="#D2691E",fg="white", text="New Game", command=self.new_game, width=button_width)
        self.new_game_button.grid(row=0, column=1, sticky="n", padx=(10,50), pady=(250, 2))  # Reduce gap with smaller pady

        # Undo Button
        self.undo_button = tk.Button(self.root,bg="#D2691E",fg="white", text="Undo", command=self.undo_move, width=button_width)
        self.undo_button.grid(row=0, column=1, sticky="n", padx=(10,50), pady=(350, 2))  # Reduce gap with smaller pady

         # Turn Indicator Label
        self.turn_label = tk.Label(self.root, bg= "#DEB887", text="Current Turn: White", font=("Arial", 14))
        self.turn_label.grid(row=2, column=0, columnspan=2, pady=(10, 0), padx=(50, 280))

        # Image Labels
        self.image1_label = tk.Label(self.root, bg= "#DEB887", image=self.images["image1"])
        self.image1_label.grid(row=0, column=1, sticky="n", pady=(300, 2), padx=(0,35))  # Position above Undo button

        self.image2_label = tk.Label(self.root, bg= "#DEB887", image=self.images["image2"])
        self.image2_label.grid(row=0, column=1, sticky="n", pady=(200, 20),padx=(0,35))  # Position above New Game button

        self.image_main_label = tk.Label(self.root, bg= "#DEB887", image=self.images["image_main"])
        self.image_main_label.grid(row=0, column=1, sticky="n", pady=(40, 2),padx=(10,50))  # Center position

        # Scoreboard Labels

        # White Score Label
        self.white_score_label = tk.Label(self.root, bg= "#DEB887", text="White Score: 0", font=("Arial", 12))
        self.white_score_label.grid(row=1, column=1, sticky="n", padx=(10, 50), pady=(0, 2))

        # Black Score Label
        self.black_score_label = tk.Label(self.root, bg= "#DEB887", text="Black Score: 0", font=("Arial", 12))
        self.black_score_label.grid(row=1, column=1, sticky="n", padx=(10, 50), pady=(30, 2))

        self.return_button = tk.Button(self.root, bg="#D2691E", fg="white", text="Return", command=self.return_to_main, width=button_width)
        self.return_button.grid(row=1, column=1, sticky="n", padx=(10, 50), pady=(60, 2))  # Position it below the Undo button
        
        # Scoreboard Functions 
    def update_score(self, captured_piece):
        
        # Piece values for scoring
        piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9}
        piece_type = captured_piece.symbol().lower()
        score = piece_values.get(piece_type, 0)

        if captured_piece.color == chess.WHITE:
            self.black_score += score
            self.black_score_label.config(text=f"Black Score: {self.black_score}")
        else:
            self.white_score += score
            self.white_score_label.config(text=f"White Score: {self.white_score}")

    def on_click(self, event):
        col = event.x // 60
        row = 7 - (event.y // 60)
        square = chess.square(col, row)

        if self.selected_square is not None:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                captured_piece = self.board.piece_at(square)
                if captured_piece:  # Check if a piece was captured
                    self.update_score(captured_piece)

                self.move_history.append(move)
                self.board.push(move)
                self.selected_square = None
                self.current_turn = not self.current_turn
                self.update_turn_label()
            else:
                messagebox.showwarning("Invalid Move", "That move is not legal!")
                self.selected_square = None
        else:
            if self.board.piece_at(square) and self.board.piece_at(square).color == self.current_turn:
                self.selected_square = square

        self.update_board()

    def new_game(self):
        self.board = chess.Board()
        self.selected_square = None
        self.move_history = []
        self.white_score = 0
        self.black_score = 0
        self.white_score_label.config(text="White Score: 0")
        self.black_score_label.config(text="Black Score: 0")
        self.update_board()    

    def load_images(self):
        pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk',
                  'bp', 'br', 'bn', 'bb', 'bq', 'bk']
        for piece in pieces:
            try:
                image = Image.open(f"Assets/images/{piece}.png").convert("RGBA")
                image = image.resize((60, 60), Image.Resampling.LANCZOS)
                self.images[piece] = ImageTk.PhotoImage(image)
            except Exception as e:
                print(f"Error loading image {piece}.png: {e}")
             # Load custom images for button positions and center display
        try:
            image1 = Image.open("Assets/images/Undo.png").resize((30, 30), Image.Resampling.LANCZOS)
            self.images["image1"] = ImageTk.PhotoImage(image1)

            image2 = Image.open("Assets/images/New Game.png").resize((60, 40), Image.Resampling.LANCZOS)
            self.images["image2"] = ImageTk.PhotoImage(image2)

            image_main = Image.open("Assets/images/Logo.png").resize((150, 150), Image.Resampling.LANCZOS)
            self.images["image_main"] = ImageTk.PhotoImage(image_main)
        except Exception as e:
            print(f"Error loading custom images: {e}")    

    def remove_background(self, image):
        # Create a new image with transparency
        data = image.getdata()
        new_data = []
        for item in data:
            if len(item) == 4:  # Ensure the pixel has 4 channels (RGBA)
                # Check if the pixel is a very dark color (indicating background)
                if item[0] < 50 and item[1] < 50 and item[2] < 50 and item[3] > 0:
                    new_data.append((255, 255, 255, 0))  # Change to transparent
                else:
                    new_data.append(item)  # Keep the original color
            else:
                new_data.append(item)  # Keep the original color if not RGBA
        image.putdata(new_data)
        return image

    def update_board(self):
        self.canvas.delete("all")
        colors = ["#D2691E", "#DEB887"]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1 = col * 60
                y1 = row * 60
                x2 = x1 + 60
                y2 = y1 + 60
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    image_name = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"
                    if image_name in self.images:
                        self.canvas.create_image(x1, y1, anchor="nw", image=self.images[image_name])

        # Highlight the selected piece and its possible moves
        if self.selected_square is not None:
            selected_row, selected_col = divmod(self.selected_square, 8)
            self.highlight_square(selected_row, selected_col, color="cyan")  # Highlight selected piece

            # Highlight possible moves for the selected piece
            piece = self.board.piece_at(self.selected_square)
            if piece and piece.color == self.current_turn:  # Only highlight for current player's pieces
                for move in self.board.legal_moves:
                    if move.from_square == self.selected_square:
                        target_row, target_col = divmod(move.to_square, 8)
                        self.highlight_square(target_row, target_col, color="yellow")  # Highlight possible moves

    def highlight_square(self, row, col, color):
        x1 = col * 60
        y1 = (7 - row) * 60
        x2 = x1 + 60
        y2 = y1 + 60
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, stipple="gray25")  # Use stipple for visibility

    def on_click(self, event):
        col = event.x // 60
        row = 7 - (event.y // 60)
        square = chess.square(col, row)

        if self.selected_square is not None:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.move_history.append(move)  # Store the move in history
                self.board.push(move)
                self.selected_square = None
                # Switch turns
                self.current_turn = not self.current_turn  # Toggle turn
                self.update_turn_label()
            else:
                messagebox.showwarning("Invalid Move", "That move is not legal!")
                self.selected_square = None
        else:
            if self.board.piece_at(square) and self.board.piece_at(square).color == self.current_turn:  # Check if there is a piece of the current player
                self.selected_square = square  # Select the piece

        self.update_board()

    def update_turn_label(self):
        if self.current_turn == chess.WHITE:
            self.turn_label.config(text="Current Turn: White")
        else:
            self.turn_label.config(text="Current Turn: Black")

    def new_game(self):
        self.board = chess.Board()  # Reset the chess board
        self.selected_square = None  # Reset selected square
        self.move_history = []  # Clear move history
        self.update_board()  # Update the GUI to reflect the new game

    def undo_move(self):
        if self.move_history:
            last_move = self.move_history.pop()  # Get the last move
            self.board.pop()  # Undo the last move on the board
            self.selected_square = None  # Reset selected square
            self.update_board()  # Update the GUI
        else:
            messagebox.showinfo("Undo", "No moves to undo!")

    def return_to_main(self):
        from main import MainScreen  # Local import
        self.clear_screen()
        MainScreen(self.root)

    def clear_screen(self):
        # Clears the main screen widgets before loading the game screen
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
