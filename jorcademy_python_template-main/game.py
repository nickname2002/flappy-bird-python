from jorcademy import *
from game_object import *

# === CONSTANTS === #
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 512


# === GAME OBJECTS === #
# Bird
bird: Bird = GameObject(400, 200, 34, 24, "sprites/bluebird-upflap.png")

# Backdrops
backdrops: list = [Backdrop(144, 256, 288, 512, "sprites/background-night.png"),
                   Backdrop(288, 256, 288, 512, "sprites/background-night.png"),
                   Backdrop(432, 256, 288, 512, "sprites/background-night.png"),
                   Backdrop(576, 256, 288, 512, "sprites/background-night.png"),
                   Backdrop(720, 256, 288, 512, "sprites/background-night.png"),
                   Backdrop(864, 256, 288, 512, "sprites/background-night.png"),
                   Backdrop(1008, 256, 288, 512, "sprites/background-night.png")] 

# Pipes
pipes: list = [Pipe(600, 360, 52, 320, "sprites/pipe-green.png"), 
               Pipe(600, -90, 52, 320, "sprites/pipe-green-rotated.png"),
               Pipe(300, 360, 52, 320, "sprites/pipe-green.png"), 
               Pipe(300, -90, 52, 320, "sprites/pipe-green-rotated.png"),
               Pipe(0, 360, 52, 320, "sprites/pipe-green.png"), 
               Pipe(0, -90, 52, 320, "sprites/pipe-green-rotated.png")]


# Game setup
def setup() -> None:
    screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    backdrop((255, 255, 255))
    title("Flappy Bird")


# Game update
def draw() -> None:
    # Update objects
    for bd in backdrops:
        bd.update()
    
    for pipe in pipes:
        pipe.update()

    # Draw objects
    for bd in backdrops:
        bd.draw()

    for pipe in pipes:
        pipe.draw()

    bird.draw()
    
# TODO: Pipe pairing and proper movement
# TODO: Wrapping draws and updates inside separate functions for clarity