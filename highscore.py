import tkinter as tk

def show_high_score(parent_window):
    parent_window.withdraw()  # Hide the main window

    def on_close():
        high_score_window.destroy()
        parent_window.deiconify()  # Show the main window again

    high_score_window = tk.Toplevel()
    high_score_window.title("High Scores")
    high_score_window.geometry("583x538")
    high_score_window.config(bg="#006400")

    # Your high score widgets here...

    high_score_window.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close
