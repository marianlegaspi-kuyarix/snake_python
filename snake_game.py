#starting the modification of the program
import tkinter 
from PIL import Image, ImageTk
from tkinter import font
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT =  TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window 
game_window = tkinter.Tk()
game_window.title("SNAKE_OP")
game_window.resizable(False, False)

game_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

snake_stage = tkinter.Canvas(game_window, bg = "#58d68d", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)

#game font
game_font_title = font.Font(family= "Daydream", size=30, weight="bold")
game_font_large = font.Font(family= "Pixelify Sans SemiBold", size=40)
game_font_medium = font.Font(family= "Pixelify Sans", size=20, weight="bold")
game_font_small = font.Font(family="Pixelify Sans Medium", size=15, weight="bold")

#center the game window
def center_window():
    window_width = game_window.winfo_width()
    window_height = game_window.winfo_height()
    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()

    window_x = int((screen_width/2) - (window_width/2))
    window_y = int((screen_height/2) - (window_height/2))

    #format "(w)x(h)+h+x+y"t
    game_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize the game
snake = Tile(5* TILE_SIZE, 5*TILE_SIZE) #single tile for the snake's head
snake_food =Tile(10* TILE_SIZE, 10*TILE_SIZE) 
snake_body = [] #multiple snake tiles
snake_vel_x = 0
snake_vel_y = 0
game_over = False
game_score = 0

#game paused feature
game_paused = False

#game menu 
game_img = Image.open("C:\\Users\\Ian\\snake\\game_menu.png")
game_img = game_img.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
game_menu_bg = ImageTk.PhotoImage(game_img)

game_menu = tkinter.Canvas(game_window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
game_menu.create_image(0, 0, anchor="nw", image=game_menu_bg)

game_menu.create_text(WINDOW_WIDTH / 2, 100, text="SNAKE GAME", font=game_font_title, fill="#ffffff", anchor="center")
game_menu.create_text(WINDOW_WIDTH / 2, 150, text="ON", font=game_font_title, fill="#ffffff", anchor="center")
game_menu.create_text(WINDOW_WIDTH / 2, 200, text="PYTHON", font=game_font_title, fill="#ffffff", anchor="center")

button_pos = tkinter.Frame(game_menu)
button_pos.place(relx=0.5, rely=0.5, anchor="center")

def game_start():
    global game_over, game_paused, game_score, snake, snake_food, snake_body, snake_vel_x, snake_vel_y
    snake = Tile(5* TILE_SIZE, 5*TILE_SIZE) #single tile for the snake's head
    snake_food =Tile(10* TILE_SIZE, 10*TILE_SIZE) 
    snake_body = [] 
    snake_vel_x = 0
    snake_vel_y = 0
    game_over = False
    game_score = 0
    game_paused = False

    game_menu.pack_forget()
    snake_stage.pack(fill="both", expand=True)
    
    game_window.update()
    center_window()
    
    draw()

def game_quit():
    game_window.quit()

#game menu buttons
def on_enter_play(button):
    button.config(bg="#abebc6")#lighter

def on_leave_play(button):
    button.config(bg="#58d68d")

def on_enter_quit(button):
    button.config(bg="#f1948a")#lighter

def on_leave_quit(button):
    button.config(bg="#e74c3c")

play_button = tkinter.Button(button_pos, text="Play", font=game_font_medium, bg="#58d68d", fg="white", command=game_start,  padx=30, pady=10)
play_button.bind("<Enter>", lambda e: on_enter_play(play_button))
play_button.bind("<Leave>", lambda e: on_leave_play(play_button))
play_button.pack()

quit_button = tkinter.Button(button_pos, text="Quit", font=game_font_medium, bg="#e74c3c", fg="white", command=game_quit, padx=30, pady=10)
quit_button.bind("<Enter>", lambda e: on_enter_quit(quit_button))
quit_button.bind("<Leave>", lambda e: on_leave_quit(quit_button))
quit_button.pack()

game_menu.pack(fill="both", expand=True)
game_window.update()
center_window()

def pause_toggle(e):
    global game_paused
    game_paused = not game_paused

def spacebar_press(e):
    global game_over
    if game_over:
        show_game_menu()

#control binds
def change_direction(e): #e = event
    #print(e)
    #print(e.keysym)    
    global snake_vel_x, snake_vel_y, game_over
    if (game_over):
        return

    if (e.keysym == "Up" and snake_vel_y != 1):
        snake_vel_x = 0
        snake_vel_y = -1
    elif (e.keysym == "Down" and snake_vel_y != -1):
        snake_vel_x = 0
        snake_vel_y = 1
    elif (e.keysym == "Left" and snake_vel_x != 1):
        snake_vel_x = -1
        snake_vel_y = 0
    elif (e.keysym == "Right"  and snake_vel_x != -1):
        snake_vel_x = 1
        snake_vel_y = 0
            
def move():
    global snake, snake_food, snake_body, game_over, game_score
    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
            
    #collision of the snake and the food
    if (snake.x == snake_food.x and snake.y == snake_food.y):
        snake_body.append(Tile(snake_food.x, snake_food.y))
        snake_food.x = random.randint(0, COLS-1) * TILE_SIZE
        snake_food.y = random.randint(0, ROWS-1) * TILE_SIZE
        game_score += 1

    #update the snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += snake_vel_x * TILE_SIZE
    snake.y += snake_vel_y * TILE_SIZE

draw_after_id = None

def draw():
    global snake, snake_food, snake_body, game_over, game_score, draw_after_id
    
    if game_paused:
        snake_stage.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = game_font_large, text = "PAUSED", fill = "black")

        if draw_after_id:
            game_window.after_cancel(draw_after_id) 
        draw_after_id = game_window.after(100, draw)
        return
    
    if game_over:

        snake_stage.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = game_font_large, text = f"GAME OVER: {game_score}", fill = "black" )
        snake_stage.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 60, font =game_font_small, text = "Press Space to retutn to the menu", fill = "black")

        spacebar_w = 200
        spacebar_h = 40
        spacebar_x1 = (WINDOW_WIDTH / 2) - (spacebar_w / 2) 
        spacebar_y1 = (WINDOW_HEIGHT / 2) + 80 
        spacebar_x2 = spacebar_x1 + spacebar_w
        spacebar_y2 = spacebar_y1 + spacebar_h
        
        snake_stage.create_rectangle(spacebar_x1, spacebar_y1, spacebar_x2, spacebar_y2, fill="#D3D3D3", outline="black")
        snake_stage.create_text(WINDOW_WIDTH / 2, spacebar_y1 + (spacebar_h / 2), font=game_font_medium, text="SPACE", fill="black") 

        if draw_after_id:
            game_window.after_cancel(draw_after_id) 
        draw_after_id = game_window.after(100, draw)
        return 
    
    move()

    snake_stage.delete("all")

    #draw the snake's food
    snake_stage.create_rectangle(snake_food.x, snake_food.y, snake_food.x + TILE_SIZE, snake_food.y + TILE_SIZE, fill = "#ec7063")

    #draw the snake
    snake_stage.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "cyan")

    for tile in snake_body:
        snake_stage.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "#3498db")

    snake_stage.create_text(45, 20, font=game_font_small, text=f"Score: {game_score}", fill="black")

    if draw_after_id:
        game_window.after_cancel(draw_after_id)
    draw_after_id = game_window.after(100, draw)
    return

def show_game_menu():
    snake_stage.pack_forget()
    game_menu.pack()
    game_window.update()
    center_window()

game_window.bind("<KeyRelease>", change_direction)
game_window.bind("<p>",pause_toggle)
game_window.bind("<space>",spacebar_press)
game_window.mainloop()