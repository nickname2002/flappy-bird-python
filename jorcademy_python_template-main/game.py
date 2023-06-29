from jorcademy import *
from game_object import *

# === CONSTANTS === #
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 512


# === GAME OBJECTS === #
# Bird
bird: Bird = Bird(400, 200, 34, 24, "sprites/bluebird-upflap.png")

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


# Make pipe reset position when out of frame
def reset_pipe_positions():
    space_between_pipes: int = 440

    for i in range(3):
       # Fetch pair of pipes
       pipe1 = pipes[i * 2]
       pipe2 = pipes[i * 2 + 1]

       # Update pipe positions when out of frame
       if pipe1.out_of_frame():
           # Generate random y position
           pipe1.reset_pipe_position()
           pipe2.y = pipe1.y - space_between_pipes

           # Place pipes at the right side of frame
           pipe1.place_right_of_frame()
           pipe2.place_right_of_frame()


# Handle user input
def user_input():
    if key_space_down:
        bird.flap()
    else:
        bird.fall()


# Update objects
def update_game_objects():
    # Update pipes
    for bd in backdrops:
        bd.update()
    
    # Update pipes
    for pipe in pipes:
        pipe.update()
    reset_pipe_positions()

    # Update bird
    bird.update()
    

# Draw objects
def draw_game_objects():
    # Draw backdrops
    for bd in backdrops:
        bd.draw()

    # Draw pipes
    for pipe in pipes:
        pipe.draw()

    # Draw bird
    bird.draw()


# Game setup
def setup() -> None:
    screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    backdrop((255, 255, 255))
    title("Flappy Bird")


# Game update
def draw() -> None:
    user_input()
    update_game_objects()
    draw_game_objects()

