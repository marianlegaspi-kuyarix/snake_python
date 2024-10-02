import tkinter 
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
game_window.title("Snake")
game_window.resizable(False, False)

canvas = tkinter.Canvas(game_window, bg = "magenta", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
game_window.update()

#center the game window
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

#control binds
def change_direction(e): #e = event
    #print(e)
    #print(e.keysym)
    global snake_vel_x, snake_vel_y

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
    global snake

    #collision of the snake and the food
    if (snake.x == snake_food.x and snake.y == snake_food.y):
        snake_body.append(Tile(snake_food.x, snake_food.y))
        snake_food.x = random.randint(0, COLS-1) * TILE_SIZE
        snake_food.y = random.randint(0, ROWS-1) * TILE_SIZE

    #update the snake body
    for i in range(len(snake_body)-1, -1):
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

def draw():
    global snake
    move()

    canvas.delete("all")

    #draw the snake's food
    canvas.create_rectangle(snake_food.x, snake_food.y, snake_food.x + TILE_SIZE, snake_food.y + TILE_SIZE, fill = "yellow")

    #draw the snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "cyan")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "cyan")

    game_window.after(100, draw) #100ms = 1/10 second, 10 frames/second

draw()    

game_window.bind("<KeyRelease>", change_direction)
game_window.mainloop()


