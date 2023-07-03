from jorcademy import *
from game_object import *

# === VARIABLES === #

# Constants
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 512

# Game flags
game_over: bool = True
bird_hit_pipe: bool = False

# Game vars
score: int = 0
pipes_start_position: int = 1000
diff_x_between_pipes: int = 300
animation_speed: int = 10

# Audio
flap_sound = load_sound("assets/audio/wing.wav")
score_sound = load_sound("assets/audio/point.wav")
hit_sound = load_sound("assets/audio/hit.wav")
die_sound = load_sound("assets/audio/die.wav")

# === GAME OBJECTS === #

# Bird
bird: Bird = Bird(400, 200, 34, 24,
                  ["sprites/bluebird-upflap.png", "sprites/bluebird-downflap.png"], 15)

# Backdrops
backdrops: list = [StaticObject(144, 256, 288, 512, 0.5, "sprites/background-night.png"),
                   StaticObject(288, 256, 288, 512, 0.5, "sprites/background-night.png"),
                   StaticObject(432, 256, 288, 512, 0.5, "sprites/background-night.png"),
                   StaticObject(576, 256, 288, 512, 0.5, "sprites/background-night.png"),
                   StaticObject(720, 256, 288, 512, 0.5, "sprites/background-night.png"),
                   StaticObject(864, 256, 288, 512, 0.5, "sprites/background-night.png"),
                   StaticObject(1008, 256, 288, 512, 0.5, "sprites/background-night.png")]

# Grounds
grounds: list = [StaticObject(0, 500, 337, 512, 3.5, "sprites/base.png"),
                 StaticObject(333, 500, 337, 512, 3.5, "sprites/base.png"),
                 StaticObject(333 * 2, 500, 337, 512, 3.5, "sprites/base.png"),
                 StaticObject(333 * 3, 500, 337, 512, 3.5, "sprites/base.png")]

# Pipes
pipes: list = [Pipe(600, 360, 52, 320, "sprites/pipe-green.png"),
               Pipe(600, -90, 52, 320, "sprites/pipe-green-rotated.png"),
               Pipe(300, 360, 52, 320, "sprites/pipe-green.png"),
               Pipe(300, -90, 52, 320, "sprites/pipe-green-rotated.png"),
               Pipe(0, 360, 52, 320, "sprites/pipe-green.png"),
               Pipe(0, -90, 52, 320, "sprites/pipe-green-rotated.png")]


# Sense that the bird has passed a pair of pipes
def update_score() -> None:
    global score
    global bird_hit_pipe

    for pipe in pipes:
        if (pipe.x > SCREEN_WIDTH / 2 - 2) and \
                (pipe.x < SCREEN_WIDTH / 2 + 2) and \
                not bird_hit_pipe:
            score += 1
            play_sound(score_sound, 1)
            break


# Make pipe reset position when out of frame
def reset_pipe_heights() -> None:
    space_between_pipes: int = 440

    for i in range(3):
        # Fetch a pair of pipes
        pipe1 = pipes[i * 2]
        pipe2 = pipes[i * 2 + 1]

        # Update pipe positions when out of frame
        if pipe1.out_of_frame():
            # Generate random y position
            pipe1.reset_pipe_position()
            pipe2.y = pipe1.y - space_between_pipes

            # Place pipes on the right side of frame
            pipe1.place_right_of_frame()
            pipe2.place_right_of_frame()


# Initialize pipe positions at game start
def init_pipes() -> None:
    for i in range(3):
        # Fetch a pair of pipes
        pipe1 = pipes[i * 2]
        pipe2 = pipes[i * 2 + 1]

        # Set start position
        pipe1.x = pipes_start_position + 300 * i
        pipe2.x = pipe1.x


# Check collision of bird with pipes
def observe_collision() -> None:
    global bird_hit_pipe

    for pipe in pipes:
        if bird.collision_detected(pipe) \
                and not bird_hit_pipe:
            play_sound(hit_sound, 2)
            play_sound(die_sound, 3)
            bird_hit_pipe = True


# Handle user input
def user_control() -> None:
    if key_space_down:
        bird.flap()
        play_sound(flap_sound, 0)
    else:
        bird.fall()


# Update objects
def update_game_objects() -> None:
    # Update pipes
    for bd in backdrops:
        bd.update()

    # Update pipes
    for pipe in pipes:
        pipe.update()
    reset_pipe_heights()

    # Update grounds
    for ground in grounds:
        ground.update()

    # Update bird
    bird.update()


# Draw objects
def draw_game_objects() -> None:
    # Draw backdrops
    for bd in backdrops:
        bd.draw()

    # Draw pipes
    for pipe in pipes:
        pipe.draw()

    # Draw grounds
    for ground in grounds:
        ground.draw()

    # Draw bird
    bird.draw()


# Display UI of in-game state
def display_game_ui() -> None:
    global game_over

    # Display score
    display_score()

    # Switch to menu when game over
    if not game_over and bird.ground_hit():
        if key_up_down:
            game_over = True
        else:
            image("sprites/gameover.png", 
                  SCREEN_WIDTH / 2, 
                  SCREEN_HEIGHT / 2 - 50, 
                  2)
            text("PRESS UP TO CONTINUE", 
                 52,
                 (255, 255, 255),
                 SCREEN_WIDTH / 2,
                 SCREEN_HEIGHT / 2 + 30,
                 "fonts/flappy_bird_font.ttf")


# Display game menu
def display_menu() -> None:
    # Draw backdrops
    for bd in backdrops:
        bd.draw()

    # Draw grounds
    for ground in grounds:
        ground.draw()

    # Display menu message
    image("sprites/message.png", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30, 1)
    text("PRESS SPACE TO START", 
         50, 
         (255, 255, 255), 
         SCREEN_WIDTH / 2, 
         SCREEN_HEIGHT / 4 * 3 + 30, 
         "fonts/flappy_bird_font.ttf")

    # Display JorCademy icon
    image("icons/jc_icon.png", 50, 50, 0.1)


# Display the score of the game
def display_score() -> None:
    # Display score
    global score
    digits = [i for i in str(score)]
    images = [f"sprites/{digit}.png" for digit in digits]

    # Get score coordinates
    score_x = SCREEN_WIDTH / 2 + 10 - 10 * len(images)
    score_y = 40

    # Display score images
    for path in images:
        image(path, score_x, score_y, 1)
        score_x += 20


# Create starting state of the game
def init_game() -> None:
    global bird_hit_pipe
    global score

    # Reset bird
    bird.x = 400
    bird.y = 150

    # Reset vars
    score = 0
    bird_hit_pipe = False

    # Reset pipes
    init_pipes()


# Run the game
def play_game() -> None:
    # Update game score
    update_score()

    # Check for collision
    observe_collision()

    # Allow bird control until collision
    if not bird_hit_pipe and not bird.ground_hit():
        user_control()
    else:
        bird.fall()

    # Update game objects state
    if not bird.ground_hit():
        update_game_objects()

        # Draw the game objects
    draw_game_objects()
    display_game_ui()


# Game setup
def setup() -> None:
    # Screen settings
    screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    title("Flappy Bird | JorCademy Engine")

    # Setup game
    init_game()


# Game update
def update() -> None:
    global game_over

    # Determine game state
    if game_over:
        display_menu()

        if key_space_down:
            init_game()
            game_over = False
    else:
        play_game()
