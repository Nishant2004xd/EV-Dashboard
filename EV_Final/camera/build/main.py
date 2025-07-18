
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen Switcher")
        self.geometry("300x200")

        # Initialize the current frame
        self.current_frame = None
        self.switch_frame(Screen1)

    def switch_frame(self, frame_class):
        # Destroy the current frame and replace it with a new one
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill='both', expand=True)

class Screen1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        label = tk.Label(self, text="This is Screen 1")
        label.pack(pady=20)

        button = tk.Button(self, text="Go to Screen 2", command=lambda: master.switch_frame(Screen2))
        button.pack()

class Screen2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        label = tk.Label(self, text="This is Screen 2")
        label.pack(pady=20)

        button = tk.Button(self, text="Go to Screen 1", command=lambda: master.switch_frame(Screen1))
        button.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
