import tkinter 
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT =  TILE_SIZE * ROWS

#game window 
game_window = tkinter.Tk()
game_window.title("Snake")
game_window.resizable(False, False)

canvas = tkinter.Canvas(game_window, bg = "magenta", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
game_window.update

game_window.mainloop()


