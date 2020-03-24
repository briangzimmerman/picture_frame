import tkinter as tk

class MainWindow(tk.Tk):
    CLOSE_BUTTON = '<Escape>'
    _window      = None

    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-fullscreen', True)
        self.bind(self.CLOSE_BUTTON, lambda e: self.destroy())
        self.canvas = tk.Canvas(
            self,
            width=self.winfo_screenwidth(),
            height=self.winfo_screenheight(),
            highlightthickness=0
        )
        self.canvas.pack()

    @staticmethod
    def get() -> 'MainWindow':
        if not MainWindow._window:
            MainWindow._window = MainWindow()
        
        return MainWindow._window
