from jorcademy import *

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
        if self.x < -self.width / 2: 
            self.x = 800 + self.width / 2

    def update(self):
        pass 

    def draw(self):
        image(self.pathname, self.x, self.y, 1)


class Bird(GameObject):
    def __init__(self, x, y, width, height, pathname):
        super().__init__(x, y, width, pathname)

    def update():
        pass


class Pipe(GameObject):
    def __init__(self, x, y, width, height, pathname):
        super().__init__(x, y, width, height, pathname)
        self.speed = 1.5

    def update(self):
        self.move()


class Backdrop(GameObject):
    def __init__(self, x, y, width, height, pathname):
        super().__init__(x, y, width, height, pathname)
        self.speed = 0.5

    def update(self):
        self.move()