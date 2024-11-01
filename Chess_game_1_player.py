import tkinter as tk
from tkinter import messagebox
import chess
import random
from PIL import Image, ImageTk


class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.board = chess.Board()
        self.selected_square = None  # Initialize the selected_square attribute
        self.history = []  # Track history for undo functionality
        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=480, height=480)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.on_click)
        self.images = {}
        self.load_images()

        # Buttons
        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.grid(row=0, column=1)

        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo_move)
        self.undo_button.grid(row=1, column=1)

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

    def update_board(self):
        self.canvas.delete("all")  # Clear previous drawings

        # Draw the squares
        colors = ["white", "brown"]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1 = col * 60
                y1 = row * 60
                x2 = x1 + 60
                y2 = y1 + 60
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        # Draw the pieces
        for row in range(8):
            for col in range(8):
                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    image_name = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"
                    if image_name in self.images:
                        self.canvas.create_image(col * 60, row * 60, anchor="nw", image=self.images[image_name])

        # Highlight the selected piece and possible moves
        if self.selected_square is not None:
            selected_row, selected_col = divmod(self.selected_square, 8)
            piece = self.board.piece_at(self.selected_square)

            # Only highlight for the selected piece
            if piece and piece.color:  # Ensure it's a white piece
                self.highlight_square(selected_row, selected_col, color="cyan")  # Highlight selected piece

                # Highlight possible moves for the selected piece
                for move in self.board.legal_moves:
                    if move.from_square == self.selected_square:
                        target_row, target_col = divmod(move.to_square, 8)
                        self.highlight_square(target_row, target_col, color="yellow")  # Highlight possible moves

    def highlight_square(self, row, col, color):
        x1 = col * 60
        y1 = (7-row) * 60
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
                self.history.append(self.board.san(move))  # Record the move in history
                self.board.push(move)
                self.selected_square = None
                self.ai_move()  # AI makes its move after player move
            else:
                messagebox.showwarning("Invalid Move", "That move is not legal!")
                self.selected_square = None
        else:
            # Only allow selection of white pieces
            if self.board.piece_at(square) and self.board.piece_at(square).color:  # Check if there is a white piece
                self.selected_square = square  # Select the piece
            else:
                self.selected_square = None  # Deselect if clicking on empty square or black piece

        self.update_board()

    def ai_move(self):
        if not self.board.is_game_over():
            legal_moves = list(self.board.legal_moves)
            move = random.choice(legal_moves)  # Randomly choose a legal move for AI
            self.history.append(self.board.san(move))  # Record AI move in history
            self.board.push(move)
            self.update_board()

    def new_game(self):
        self.board.reset()  # Reset the chessboard to the initial position
        self.history.clear()  # Clear the move history
        self.selected_square = None  # Reset selected square
        self.update_board()

    def undo_move(self):
        if self.history:
            self.board.pop()  # Undo the last move
            self.history.pop()  # Remove the last move from history
            if self.history:  # Check if there's a move to undo
                self.board.pop()  # Undo AI move as well
                self.history.pop()  # Remove the AI move from history
            self.update_board()


if __name__ == "__main__":  # Corrected __name__ check
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
