import tkinter as tk
import random


class SnakeGame:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.game_window = tk.Toplevel(parent_window)
        self.game_window.title("Snake Game")
        self.running = False  # Start with the game paused
        self.update_id = None  # Initialize update_id
        self.is_game_over = False  # Flag to track if the game over pop-up is already displayed
        self.parent_window = parent_window

        # Setting the window size to fit 20x20 grid, each cell 20 pixels
        self.grid_size = 20
        self.cell_size = 20
        self.window_size = self.grid_size * self.cell_size
        self.game_window.geometry(f"{self.window_size}x{self.window_size}")

        # Creating a canvas with a frame
        self.frame = tk.Frame(self.game_window, bg="black")
        self.frame.pack(padx=10, pady=10)  # Padding for frame

        self.canvas = tk.Canvas(self.frame, width=self.window_size, height=self.window_size, bg="black")
        self.canvas.pack()

        # Draw the initial grid
        self.draw_grid()

        self.game_window.wait_visibility()  # Wait until the window is visible
        self.game_window.grab_set()  # Direct all input to this window
        self.focus_attempts = 0
        # Set focus to the game window immediately after it's created
        self.game_window.focus_force()
        self.set_focus_to_game()

        # Snake initialization
        self.direction = 'Right'  # Initial direction
        middle_y = self.window_size // 2  # Calculate the middle y-coordinate
        segment_length = 4  # Number of initial segments
        self.snake = [(i * self.cell_size, middle_y) for i in range(segment_length)]

        # Draw the initial state of the snake
        self.draw_snake()

        # Initialize apple coordinates
        self.apple_x, self.apple_y = None, None
        self.spawn_apple()  # Ensures an apple is on the board

        # Bind arrow keys for movement
        self.game_window.bind("<Up>", self.change_direction)
        self.game_window.bind("<Down>", self.change_direction)
        self.game_window.bind("<Left>", self.change_direction)
        self.game_window.bind("<Right>", self.change_direction)

        self.update()  # Start the game loop

    def set_focus_to_game(self):
        if self.focus_attempts < 5:  # Limit the number of attempts
            self.game_window.focus_set()  # Set focus to the game window
            self.focus_attempts += 1
            self.game_window.after(100, self.set_focus_to_game)

    def draw_grid(self):
        light_green = "#ccffcc"  # Very light green
        darker_green = "#99cc99"  # Darker green

        for i in range(0, self.window_size, self.cell_size):
            for j in range(0, self.window_size, self.cell_size):
                color = light_green if (i // self.cell_size + j // self.cell_size) % 2 == 0 else darker_green
                self.canvas.create_rectangle(i, j, i + self.cell_size, j + self.cell_size, fill=color, outline="")

    def change_direction(self, event):
        """Change snake direction and start the game if paused."""
        if not self.running:
            self.running = True
            self.update()  # Start the game loop if it was paused
        """Change snake direction based on arrow key press, prevent reversing"""
        opposite_directions = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        new_direction = event.keysym  # Use the actual event keysym

        # Change direction if not opposite to current direction to avoid self-collision
        if new_direction in opposite_directions and new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

    def move_snake(self):
        # Calculate the new head position based on the current direction
        old_head_x, old_head_y = self.snake[-1]
        if self.direction == 'Up':
            new_head_y = old_head_y - self.cell_size
            new_head_x = old_head_x
        elif self.direction == 'Down':
            new_head_y = old_head_y + self.cell_size
            new_head_x = old_head_x
        elif self.direction == 'Left':
            new_head_x = old_head_x - self.cell_size
            new_head_y = old_head_y
        elif self.direction == 'Right':
            new_head_x = old_head_x + self.cell_size
            new_head_y = old_head_y

        # Move the snake by adding the new head (front of the list)
        self.snake.append((new_head_x, new_head_y))

        # Check for wall collisions
        if (new_head_x < 0 or new_head_x >= self.window_size or
                new_head_y < 0 or new_head_y >= self.window_size):
            self.game_over()
            return

        # Check for self collisions (compare new head position to the rest of the body)
        if (new_head_x, new_head_y) in self.snake[:-1]:
            self.game_over()
            return

        # Check if the snake is about to eat the apple
        next_head_x, next_head_y = new_head_x, new_head_y


        if (next_head_x, next_head_y) == (self.apple_x, self.apple_y):
            self.spawn_apple()  # Spawn a new apple and keep the tail (snake grows)
            apple_eaten = True
        else:
            apple_eaten = False

        # [rest of the move_snake code...]

        if not apple_eaten:
            # Remove the last segment of the snake if not growing
            self.snake.pop(0)

        # Check for apple collision with any part of the snake other than the head
        for segment in self.snake[:-1]:
            if segment == (self.apple_x, self.apple_y):
                self.spawn_apple()  # Spawn a new apple if collided with body

        self.draw_snake()

    def update(self):
        """Main game loop update"""
        if self.running:
            self.move_snake()  # Or any other actions needed for updating the game
            self.draw_snake()  # Redraw the snake
            # Schedule the next update only if the game is still running
            self.update_id = self.game_window.after(100, self.update)

    def draw_snake(self):
        """Draw the snake on the canvas"""
        self.canvas.delete("snake")  # Clear previous snake
        for segment in self.snake:
            x, y = segment
            # Draw each segment of the snake
            self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="blue", tags="snake")

    def spawn_apple(self):
        """Spawn an apple in a random location not occupied by the snake."""
        self.canvas.delete("apple")  # Remove the old apple from the canvas

        apple_placed = False
        while not apple_placed:
            # Generate random coordinates for the apple
            temp_x = random.randint(0, self.grid_size - 1) * self.cell_size
            temp_y = random.randint(0, self.grid_size - 1) * self.cell_size

            # Check if the generated coordinates overlap with any part of the snake
            if not any((temp_x, temp_y) == segment for segment in self.snake):
                apple_placed = True

        # Set the apple coordinates to the generated position
        self.apple_x, self.apple_y = temp_x, temp_y

        # Draw a new apple
        self.apple = self.canvas.create_oval(self.apple_x, self.apple_y,
                                             self.apple_x + self.cell_size,
                                             self.apple_y + self.cell_size, fill="red", tags="apple")

    def game_over(self):
        # If game is already over, don't do anything (to avoid multiple pop-ups)
        if self.is_game_over:
            return

        # Set the game over flag to True
        self.is_game_over = True

        """Handle game over situation"""
        # Stop the game loop
        if self.update_id:
            self.game_window.after_cancel(self.update_id)

        # Unbind key events to prevent further movement
        self.game_window.unbind("<Up>")
        self.game_window.unbind("<Down>")
        self.game_window.unbind("<Left>")
        self.game_window.unbind("<Right>")

        # Create a pop-up window for game over
        self.game_over_popup = tk.Toplevel(self.game_window)
        self.game_over_popup.title("Game Over")
        self.game_over_popup.geometry("200x100")  # Adjust size as necessary
        self.game_over_popup.transient(self.game_window)  # Make the pop-up appear above the game window

        # Center the pop-up over the game window
        x = self.game_window.winfo_x() + self.window_size / 2 - 100
        y = self.game_window.winfo_y() + self.window_size / 2 - 50
        self.game_over_popup.geometry("+%d+%d" % (x, y))

        # "Game Over" label
        label = tk.Label(self.game_over_popup, text="GAME OVER", font=("Comic Sans MS", 16, "bold"))
        label.pack(pady=10)

        # Use Comic Sans font for the buttons
        button_font = ("Comic Sans MS", 12, "bold")

        restart_button = tk.Button(self.game_over_popup, text="Restart", font=button_font, command=self.restart_game)
        restart_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        menu_button = tk.Button(self.game_over_popup, text="Menu", font=button_font, command=self.return_to_menu)
        menu_button.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    def return_to_menu(self):
        """Handle the event when the user clicks the 'Menu' button"""
        # Implement what happens when the user goes back to the menu
        # Close game windows or hide them, show the main menu, etc.
        self.game_over_popup.destroy()
        self.game_window.destroy()  # Example of closing the game window
        # Reopen the parent window
        self.parent_window.deiconify()

    def restart_game(self):
        """Restart the game from the beginning and pause it."""
        # Close the game over pop-up
        self.game_over_popup.destroy()

        # Cancel any existing game loops
        if self.update_id:
            self.game_window.after_cancel(self.update_id)

        # Clear the canvas
        self.canvas.delete("all")

        # Reset game variables
        self.direction = 'Right'
        middle_y = self.window_size // 2
        segment_length = 4
        self.snake = [(i * self.cell_size, middle_y) for i in range(segment_length)]
        self.is_game_over = False  # Reset the game over flag

        # Reinitialize game elements
        self.draw_grid()
        self.draw_snake()
        self.spawn_apple()

        # Rebind keys for movement
        self.game_window.bind("<Up>", self.change_direction)
        self.game_window.bind("<Down>", self.change_direction)
        self.game_window.bind("<Left>", self.change_direction)
        self.game_window.bind("<Right>", self.change_direction)

        # Reset the running state to False and do not start the game loop
        self.running = False


def start_game(parent_window):
    parent_window.withdraw()  # Hide the main window  # Close the menu window
    game = SnakeGame(parent_window)  # Start a new game in a new window

