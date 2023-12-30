import tkinter as tk
import settings
import highscore
import game

def run_menu():
    def quit_game():
        window.destroy()

    # Create the main window
    window = tk.Tk()
    window.title("Snake Game")


    # Set initial size (A5 size in pixels) and make it non-scalable
    window.geometry("583x538")  # A5 size in pixels at 72 PPI
    window.resizable(False, False)  # Prevent the window from being resizable

    # Set dark mode colors
    dark_background = "#006400"  # Dark green
    light_text = "#FFFFFF"  # White

    # Configure the window for dark mode
    window.config(bg=dark_background)

    # Configure grid rows and columns
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(4, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Add a title label with padding and larger font
    title_label = tk.Label(window, text="SNAKE GAME", font=("Comic Sans MS", 48), bg=dark_background, fg=light_text)
    title_label.grid(row=0, column=0, sticky="nsew", pady=20)

    # Define button font and style (no borders)
    button_font = ("Comic Sans MS", 20)
    button_style = {'font': button_font, 'bg': dark_background, 'fg': light_text, 'borderwidth': 0, 'highlightthickness': 0}

    # Add buttons with adjusted width, dark mode styling, increased font size, and no borders
    start_button = tk.Button(window, text="Start Game", command=lambda: game.start_game(window), **button_style)
    start_button.grid(row=1, column=0, sticky="nsew", padx=100, pady=10)

    high_score_button = tk.Button(window, text="High Score", command=lambda: highscore.show_high_score(window), **button_style)
    high_score_button.grid(row=2, column=0, sticky="nsew", padx=100, pady=10)

    settings_button = tk.Button(window, text="Settings", command=lambda: settings.open_settings(window), **button_style)
    settings_button.grid(row=3, column=0, sticky="nsew", padx=100, pady=10)

    quit_button = tk.Button(window, text="Quit", command=quit_game, **button_style)
    quit_button.grid(row=4, column=0, sticky="nsew", padx=100, pady=10)

    # Run the application
    window.mainloop()
