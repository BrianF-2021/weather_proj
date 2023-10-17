import tkinter as tk
from tkinter import messagebox


def show_message():
    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button
    messagebox.showinfo("Info", "This is a popup message")
    root.protocol("WM_DELETE_WINDOW", root.quit)  # Enable close button


root = tk.Tk()
root.title("Main Window")

show_message_button = tk.Button(
    root, text="Show Message", command=show_message)
show_message_button.pack(pady=20)

root.mainloop()


def show_custom_message():
    custom_popup = Tk.Toplevel(root)
    custom_popup.title("Custom Popup")
    custom_popup.geometry("300x150")
    label = Tk.Label(custom_popup, text="This is a custom popup message")
    label.pack(pady=20)
    # Disable close button
    custom_popup.protocol("WM_DELETE_WINDOW", lambda: None)


root = tk.Tk()
root.title("Main Window")

show_custom_message_button = tk.Button(
    root, text="Show Custom Message", command=show_custom_message)
show_custom_message_button.pack(pady=20)

root.mainloop()


def show_message(self):
    # Disable close button
    self.root.protocol("WM_DELETE_WINDOW", lambda: None)
    messagebox.showinfo("PLAYERS", "PLAYER_1:  X\nAI:  O")
    # Enable close button
    self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
