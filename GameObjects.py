import arcade
import math
import random
from motion import Flying, Point, Velocity

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15
class Bullet(Flying):

    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.velocity.dx = BULLET_SPEED
        self.velocity.dy = BULLET_SPEED
        self.bullet_color = BULLET_COLOR

    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.bullet_color)

    def fire(self, angle):
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED


class Target(Flying):
    """
    A base class for all target types
    """

    def __init__(self):
        super().__init__()
        self.center.x = random.uniform(100, 200)
        self.center.y = random.uniform(260, 400)
        self.velocity.dx = random.uniform(1, 5)
        self.velocity.dy = random.uniform(-2, 5)
        self.radius = TARGET_RADIUS
        self.num_hit = 1

    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, TARGET_COLOR)

    def hit(self):
        self.alive = False
        return self.num_hit

    def strong_hit(self):
        self.alive = False
        return self.num_hit * 2


class StrongTarget(Target):
    """"
    This is a class for a strong target rendered as a circle with a number inside it. Its a sub-class for
    Target().
    """

    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(1, 3)
        self.velocity.dy = random.uniform(-2, 1)
        self.num_hit = 3
        self.text = "3"
        self.target_color = TARGET_COLOR

    def draw(self):
        arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, self.target_color, 3)
        arcade.draw_text(self.text, self.center.x - self.radius / 2, self.center.y - self.radius / 2, self.target_color,
                         20)

    def hit(self):  # This method has been modified to decrease the number inside the circle when hit with
        self.num_hit -= 1  # a Bullet and change target color
        if self.num_hit == 2:
            self.target_color = arcade.color.RED
            self.text = "2"
        elif self.num_hit == 1:
            self.text = "1"
        elif self.num_hit < 1:
            self.alive = False
            return 5
        return 1

    def strong_hit(self):  # Additional method to check if target has been hit with a Strong Bullet
        self.alive = False
        return 6


class SafeTarget(Target):
    """
    This is a class for a safe target rendered as a rectangle. It also inherits from the Target class
    """

    def __init__(self):
        super().__init__()
        self.radius = TARGET_SAFE_RADIUS
        self.num_hit = -10

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, self.radius * 2, self.radius * 2, TARGET_SAFE_COLOR)

    def hit(self):
        self.alive = False
        return self.num_hit

    def strong_hit(self):  # Checks to see if target has been hit by a strong bullet
        self.alive = False
        return self.num_hit


class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """

    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)



class StrongBullet(Bullet):
    """
    This is a sub class for Bullet class.
    """

    def __init__(self):
        super().__init__()
        self.bullet_color = arcade.color.RED_DEVIL


class Field:
    """
    This class helps improve game design and visuals
    """

    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

    def draw_sky(self):
        arcade.draw_lrtb_rectangle_filled(0, self.width, self.height, self.height / 3, arcade.color.SKY_BLUE)

    def draw_field(self):
        arcade.draw_lrtb_rectangle_filled(0, self.width, self.height / 3, 0, arcade.color.GREEN_YELLOW)

    def draw_tree(self):
        arcade.draw_lrtb_rectangle_filled(40, 50, 100, 50, arcade.color.DARK_BROWN)
        arcade.draw_triangle_filled(20, 100, 70, 100, 45, 200, arcade.color.GREEN)
        arcade.draw_lrtb_rectangle_filled(self.width / 2, 310, self.height / 3, 100, arcade.color.DARK_BROWN)
        arcade.draw_triangle_filled(270, 150, 340, 150, 305, 250, arcade.color.GREEN)
        arcade.draw_lrtb_rectangle_filled(540, 550, 100, 50, arcade.color.DARK_BROWN)
        arcade.draw_triangle_filled(520, 100, 570, 100, 545, 200, arcade.color.GREEN)

    def draw_sun(self):
        arcade.draw_circle_filled(540, 400, 50, arcade.color.YELLOW)