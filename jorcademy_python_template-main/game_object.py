from jorcademy import *
import random

# Constants
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 512
GRAVITY: float = 0.981


class GameObject:
    def __init__(self, x, y, width, height, pathname):
        self.x = x
        self.y = y
        self.pathname = pathname
        self.width = width
        self.height = height
        self.speed = 1

    def move(self):
        self.x -= self.speed

        # Reset position when out of screen
        if self.out_of_frame():
            self.place_right_of_frame()

    def place_right_of_frame(self):
        self.x = 800 + self.width / 2

    def out_of_frame(self):
        return self.x + 1 / 2 * self.width < 0

    def update(self):
        pass

    def draw(self):
        image(self.pathname, self.x, self.y, 1)

    def collision_detected(self, other):
        in_x_range = (self.x + self.width / 2) > (other.x - other.width / 2) and \
                     (self.x - self.width / 2) < (other.x + other.width / 2)
        in_y_range = (self.y + self.height / 2) > (other.y - other.height / 2) and \
                     (self.y - self.height / 2) < (other.y + other.height / 2)
        return in_x_range and in_y_range


class Bird(GameObject):
    def __init__(self, x, y, width, height, pathname, rotation):
        super().__init__(x, y, width, height, pathname)
        self.velocity_y = 0.5
        self.speed = 1
        self.min_velocity_y = -3
        self.max_velocity_y = 4
        self.timer = 0
        self.animation_length = 10
        self.selected_sprite = pathname[0]
        self.rotation = rotation

    # Change position based on velocity
    def move(self):
        self.y += self.velocity_y

    def ground_hit(self):
        ground_y = 450
        return (self.y + self.height / 2) >= ground_y

    def fall(self):
        self.rotation -= 2
        if self.velocity_y < self.max_velocity_y:
            self.velocity_y += GRAVITY * self.speed

    def flap(self):
        self.rotation = 20
        if self.velocity_y > self.min_velocity_y:
            self.velocity_y -= 2 * self.speed

    def handle_animations(self):
        if not self.ground_hit() and self.timer % 10 == 0:
            if self.selected_sprite == self.pathname[0]:
                self.selected_sprite = self.pathname[1]
            elif self.selected_sprite == self.pathname[1]:
                self.selected_sprite = self.pathname[0]

    def draw(self):
        # Handle animations
        if not self.ground_hit():
            self.handle_animations()

        if self.rotation < -35:
            self.rotation = -35

        # Display image
        image(self.selected_sprite, self.x, self.y, 1, self.rotation)

    def update(self):
        self.timer += 1
        if not self.ground_hit():
            self.move()


class Pipe(GameObject):
    def __init__(self, x, y, width, height, pathname):
        super().__init__(x, y, width, height, pathname)
        self.speed = 3.5

    def reset_pipe_position(self):
        min_y = 390
        max_y = 600
        self.y = random.randrange(int(min_y), int(max_y))

    def move(self):
        self.x -= self.speed

    def update(self):
        self.move()


class StaticObject(GameObject):
    def __init__(self, x, y, width, height, speed, pathname):
        super().__init__(x, y, width, height, pathname)
        self.speed = speed

    def update(self):
        self.move()
