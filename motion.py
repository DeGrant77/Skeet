import random
class Point:
    """
    This class is responsible for setting the ball at  location
    """

    def __init__(self):
        self.x = 0
        self.y = 0


class Velocity:
    """
    This class is responsible for setting a random location
    """

    def __init__(self):
        self.dx = random.uniform(1, 2)
        self.dy = random.uniform(1, 2)


class Flying:
    """"
    This is a base class for the Target and Bullet classes
    """

    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True

    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def is_off_screen(self, screen_width, screen_height):
        if self.center.x > screen_width or self.center.y > screen_height:
            return True