import tkinter as tk

class ChessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Polychess")
        self.geometry("800x800")  # Taille de la fenêtre
        self.chessboard = ChessboardWidget(self)
        self.chessboard.pack(expand=True, fill=tk.BOTH)
        self.chessboard.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.chessboard.draw_chessboard()

class ChessboardWidget(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.bind("<Button-1>", self.on_click)

    def draw_chessboard(self):
        self.delete("all")  # Efface tout sur le canevas avant de redessiner
        board_size = min(self.winfo_width(), self.winfo_height())  # Taille minimale pour s'adapter à la fenêtre
        square_size = board_size / 8  # Taille de chaque case
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = "white"
                else:
                    color = "black"  # Retour à la couleur noire
                x0 = col * square_size
                y0 = row * square_size
                x1 = (col + 1) * square_size
                y1 = (row + 1) * square_size
                self.create_rectangle(x0, y0, x1, y1, fill=color)

    def on_click(self, event):
        board_size = min(self.winfo_width(), self.winfo_height())  # Taille minimale pour s'adapter à la fenêtre
        square_size = board_size / 8  # Taille de chaque case
        col = event.x // square_size
        row = event.y // square_size
        print("Clicked on square:", row, col)

if __name__ == "__main__":
    app = ChessApp()
    app.mainloop()
