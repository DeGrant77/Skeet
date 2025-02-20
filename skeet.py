"""
Original Author: Mr. Burton
Completed by Deli DeGrant
This program implements an awesome version of skeet
"""
import arcade
import math
import random
from GameObjects import Rifle, Field, Target, StrongTarget, SafeTarget, Bullet, StrongBullet

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
TITLE = "Classic Skeet Game"

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Points
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height, title):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height, title)

        self.rifle = Rifle()
        self.score = 0
        self.field = Field()  # A Field instance
        self.bullets = []
        self.targets = []
        self.strong_bullets = []  # A separate list for strong bullets
        self.num_of_bullets = 10  # Sets the number of strong bullets

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.field.draw_sky()
        self.field.draw_field()
        self.field.draw_tree()
        self.field.draw_sun()
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        for strong in self.strong_bullets:  # Iterate through strong bullets and draws them
            strong.draw()

        for target in self.targets:
            target.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        for strong in self.strong_bullets:  # Iterate through strong bullets and advance them
            strong.advance()

        for target in self.targets:
            target.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """

        # All three types of targets created and appended here
        tar = Target()
        strong_tar = StrongTarget()
        safe_tar = SafeTarget()
        self.targets.append(tar)
        self.targets.append(strong_tar)
        self.targets.append(safe_tar)

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                            abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False

                        self.score += target.hit()
        for strong in self.strong_bullets:
            for target in self.targets:
                if strong.alive and target.alive:
                    too_close = strong.radius + target.radius

                    if (abs(strong.center.x - target.center.x) < too_close and
                            abs(strong.center.y - target.center.y) < too_close):
                        # its a hit!
                        strong.alive = False
                        self.score += target.strong_hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for strong in self.strong_bullets:
            if not strong.alive:
                self.strong_bullets.remove(strong)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for strong in self.strong_bullets:
            if strong.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.strong_bullets.remove(strong)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

        if button == arcade.MOUSE_BUTTON_RIGHT:  # If player presses the  right mouse button, strong bullet is fired!
            strong_bullet = StrongBullet()
            strong_bullet.fire(angle)
            self.strong_bullets.append(strong_bullet)
            self.num_of_bullets -= 1

        if self.num_of_bullets < 0:  # Checks to see if the number of bullets is zero and create an empty list
            self.strong_bullets = []  # for strong bullets and fires "normal" bullets instead.

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
arcade.run()
