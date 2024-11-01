import tkinter as tk
from tkinter import messagebox
import chess
from PIL import Image, ImageTk

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.board = chess.Board()
        self.selected_square = None# Initialize the selected_square attribute
        self.move_history = []  # Initialize move history
        self.current_turn = chess.WHITE  # Track the current turn
        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=480, height=480)
        self.canvas.grid(row=0, column=0 )  # Span across two columns
        self.canvas.bind("<Button-1>", self.on_click)
        self.images = {}
        self.load_images()

        # New Game Button
        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.grid(row=0, column=1)

        # Undo Button
        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo_move)
        self.undo_button.grid(row=1, column=1)

         # Turn Indicator Label
        self.turn_label = tk.Label(self.root, text="Current Turn: White", font=("Arial", 14))
        self.turn_label.grid(row=2, column=0, columnspan=2)


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
        colors = ["white", "gray"]
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
       

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
