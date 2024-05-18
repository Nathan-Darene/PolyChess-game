import tkinter as tk

class ChessGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess")
        self.geometry("600x600")
        self.board_canvas = tk.Canvas(self, width=600, height=600, bg="white")
        self.board_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_board()
        self.draw_pieces()
    
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.board_canvas.create_rectangle(j*75, i*75, (j+1)*75, (i+1)*75, fill="white")
                else:
                    self.board_canvas.create_rectangle(j*75, i*75, (j+1)*75, (i+1)*75, fill="gray")

    def draw_pieces(self):
        # Draw pieces on the board
        pass

if __name__ == "__main__":
    app = ChessGUI()
    app.mainloop()
