from jorcademy import *
from game_object import *

# === VARIABLES === #

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 512

# Game flags
game_over = False 
bird_hit_pipe = False

# Game vars
score = 0
pipes_start_position = 1000
diff_x_between_pipes = 300


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


# Sense that the bird has passed a pair of pipes
def update_score():
    global score 
    for pipe in pipes:
        if (pipe.x > SCREEN_WIDTH / 2 - 2) and \
           (pipe.x < SCREEN_WIDTH / 2 + 2):
            score += 1
            break

# Make pipe reset position when out of frame
def reset_pipe_heights():
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


# Initialize pipe positions at game start
def init_pipes():
    for i in range(3):
       # Fetch pair of pipes
       pipe1 = pipes[i * 2]
       pipe2 = pipes[i * 2 + 1]

       # Set start position
       pipe1.x = pipes_start_position + 300 * i
       pipe2.x = pipe1.x


# Check collision of bird with pipes
def observe_collision():
    global bird_hit_pipe

    for pipe in pipes:
        if bird.collision_detected(pipe):
            bird_hit_pipe = True


# Handle user input
def user_control():
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
    reset_pipe_heights()

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


def display_score():
    # Display score
    global score
    digits = [i for i in str(score)]
    images = [f"sprites/{digit}.png" for digit in digits]

    # Get score coordinates
    score_x = SCREEN_WIDTH / 2 + 10 - 10 * len(images)
    score_y = 40
    
    
    for path in images:
        image(path, score_x, score_y, 1)
        score_x += 20


# Game setup
def setup() -> None:
    # Screen settings
    screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    title("Flappy Bird")

    # Setup game
    init_pipes()


# Game update
def draw() -> None:
    # Update game score
    update_score()

    # Check for collision
    observe_collision()

    # Allow bird control until collision
    if not bird_hit_pipe:
        user_control()
    else:
        bird.fall()

    # Update game objects state
    if not bird.ground_hit():
        update_game_objects()      

    # Draw the game objects
    draw_game_objects()
    display_score()  

