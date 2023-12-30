import tkinter as tk

def open_settings(parent_window):
    parent_window.withdraw()  # Hide the main window

    def on_close():
        settings_window.destroy()
        parent_window.deiconify()  # Show the main window again

    settings_window = tk.Toplevel()
    settings_window.title("Settings")
    settings_window.geometry("583x538")
    settings_window.config(bg="#006400")

    # Your settings widgets here...

    settings_window.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close
