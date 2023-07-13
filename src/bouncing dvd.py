from __future__ import annotations
from typing import Union
from math import cos, radians, pi
import pygame


DVD_LOGO_PATH = "..\\images\\DVD logo.png"


class Point:
    x: Union[int, float]
    y: Union[int, float]

    def __init__(self, x: Union[int, float] = 0,
                 y: Union[int, float] = 0) -> None:
        self.position = (x, y)
        self.x = self.position[0]
        self.y = self.position[1]

    def __str__(self) -> str:
        """Return a string in classic constructor style."""
        return f"Point({self.position[0]}, {self.position[1]})"

    def to_tuple(self) -> tuple:
        return (self.x, self.y)

    def move(self, direction: Point) -> None:
        """Set the current point as the addition of two points in 2D vector style."""
        self.__init__(self.x + direction.x, self.y + direction.y)

    def collision(self, obj: Union[Point, Rectangle, Circle]) -> bool:
        if isinstance(obj, Point):
            return self.x == obj.x and self.y == obj.y

        elif isinstance(obj, Rectangle):
            return obj.collision(self)

        elif isinstance(obj, Circle):
            return obj.collision(self)

        else:
            raise NotImplementedError


class Rectangle:
    position: Point
    width: Union[int, float]
    height: Union[int, float]

    def __init__(self, position: Point = 0, width: Union[int, float] = 0,
                 height: Union[int, float] = 0) -> None:
        """ Initialize rectangle at position, with width w, height h."""
        self.position = position
        self.width = width
        self.height = height

    def __str__(self) -> str:
        """Return a string in classic constructor style."""
        return f"Rectangle({self.position}, {self.width}, {self.height})"

    def change_pos(self, position: Point) -> None:
        self.position.x = position.x
        self.position.y = position.y

    def move(self, direction: Point) -> None:
        """Set position as the sum of two points in 2D vector style"""
        self.position.x += direction.x
        self.position.y += direction.y

    def collision(self, obj: Union[Point, Rectangle, Circle]) -> bool:
        """Handle all collisions with all shapes."""
        if isinstance(obj, Point):
            """Points inside or intersecting borders count as colliding."""
            return self.position.x <= obj.x <= self.position.x + self.width and \
                   self.position.y <= obj.y <= self.position.y + self.height

        elif isinstance(obj, Rectangle):
            """Handle via collision with points. TODO: currently does not handle rotations."""
            rect1vertices = [self.position, Point(self.position.x + self.width,
                                                  self.position.y),
                             Point(self.position.x,
                                   self.position.y + self.height),
                             Point(self.position.x + self.width,
                                   self.position.y + self.height)]
            rect2vertices = [obj.position,
                             Point(obj.position.x + obj.width, obj.position.y),
                             Point(obj.position.x, obj.position.y + obj.height),
                             Point(obj.position.x + obj.width,
                                   obj.position.y + obj.height)]
            return any(
                [self.collision(vertice) for vertice in rect1vertices]) or \
                   any([obj.collision(vertice) for vertice in rect2vertices])

        elif isinstance(obj, Circle):
            """Handle collision via cases."""
            #  calculate the distances from rect center to circle center.
            circle_dist_x = abs(
                obj.position.x - (self.position.x + self.width / 2))
            circle_dist_y = abs(
                obj.position.y - (self.position.y + self.height / 2))

            # Check if circle center is easily outside the rectangle.
            if circle_dist_x > (
                    self.width / 2 + obj.radius) or circle_dist_y > (
                    self.height / 2 + obj.radius):
                return False

            # Check if the circle is easily inside the rectangle.
            elif (
                    circle_dist_x <= self.width / 2 + obj.radius) and circle_dist_y <= self.height / 2:  # The last
                # condition ensures that we don't handle the corners.
                return True
            elif (
                    circle_dist_y <= self.height / 2 + obj.radius) and circle_dist_x <= self.width / 2:
                return True

            # Check from the rect corners to the circle.
            vertices = [self.position,
                        Point(self.position.x + self.width, self.position.y),
                        Point(self.position.x, self.position.y + self.height),
                        Point(self.position.x + self.width,
                              self.position.y + self.height)]
            return any([obj.collision(vertice) for vertice in vertices])

        else:
            raise NotImplementedError


class Circle:
    def __init__(self, position: Point, radius: Union[int, float] = 0) -> None:
        self.position = position  # The center and anchor of the circle.
        self.radius = radius

    def __str__(self) -> str:
        """Return a string in classic constructor style."""
        return f"Circle({self.position}, {self.radius})"

    def change_pos(self, position: Point) -> None:
        self.position.x = position.x
        self.position.y = position.y

    def move(self, direction: Point) -> None:
        """Set the current point as the addition of two points in 2D vector style."""
        self.position.x += direction.x
        self.position.y += direction.y

    def collision(self, obj: Union[Point, Rectangle, Circle]) -> bool:
        """Handle collision between objects."""
        if isinstance(obj, Point):
            """Handle in cases; case-by-case speeds things up for common results."""
            """Check if the point is obviously out of the circle."""
            dist_center_point_x = obj.x - self.position.x
            dist_center_point_y = obj.y - self.position.y
            if abs(dist_center_point_x) > self.radius or abs(
                    dist_center_point_y) > self.radius:
                return False
            """Rigorously check otherwise."""
            dist_center_to_point = ((dist_center_point_x ** 2) + (
                    dist_center_point_y ** 2)) ** 0.5
            return dist_center_to_point <= self.radius

        elif isinstance(obj, Circle):
            """I opt for method 1 below. Method 2 is to calculate one center-point with another circle of radius + 
            radius"""
            dist_center_to_center = ((self.position.x - obj.position.x) ** 2 +
                                     (
                                             self.position.y - obj.position.y) ** 2) ** 0.5
            return dist_center_to_center <= self.radius + obj.radius

        elif isinstance(obj, Rectangle):
            """Let my previous work do the carrying. LOL"""
            return obj.collision(self)

        else:
            raise NotImplementedError


class Logo:
    def __init__(self, image: str, position: Point):
        self.sprite = pygame.image.load(image)
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.position = position
        self.hitbox = Rectangle(self.position, self.width, self.height)
        self.speed = 0.5
        self.direction_x = 1
        self.direction_y = 1

    def is_colliding(self, all_sprites: list) -> list:
        result = []
        for sprite in all_sprites:
            if self.hitbox.collision(sprite):
                result.append(sprite)
        return result

    def update(self):
        self.position.move(
            Point(self.direction_x * self.speed, self.direction_y * self.speed))
        self.hitbox.position = self.position


def get_rgb_list():
    return [(
        int(max(255 / 3 * (cos(3 * radians(degree) + 0 * pi / 3) + 1.5), 0)),
        int(max(255 / 3 * (cos(3 * radians(degree) + 2 * pi / 3) + 1.5), 0)),
        int(max(255 / 3 * (cos(3 * radians(degree) + 4 * pi / 3) + 1.5), 0))
    ) for degree in range(360)]  # Each entry has an RGB value to cycle through.


def main():
    pygame.init()

    RGB_LIST = get_rgb_list()

    curr_rgb = 0  # 0 <= curr_rgb < 360

    display_info = pygame.display.Info()
    surface_x = display_info.current_w
    surface_y = display_info.current_h
    main_surface = pygame.display.set_mode((surface_x, surface_y))

    dvd_icon = Logo(DVD_LOGO_PATH, Point(0, 0))
    dvd_bound_x = surface_x - dvd_icon.width
    dvd_bound_y = surface_y - dvd_icon.height
    screen = Rectangle(Point(0, 0), surface_x, surface_y)
    all_sprites = [screen]

    mode = "Screensaver"

    while mode in {"Main Menu", "Screensaver"}:
        if mode == "Main Menu":
            pass

        elif mode == "Screensaver":
            # Logic
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                mode = "Quit"

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_ESCAPE]:
                mode = "Quit"

            dvd_icon.update()
            curr_rgb += 1 / 20
            if curr_rgb >= 360:
                curr_rgb = 0

            if dvd_icon.position.x <= 0 or dvd_icon.position.x >= dvd_bound_x:
                dvd_icon.direction_x *= -1
            if dvd_icon.position.y <= 0 or dvd_icon.position.y >= dvd_bound_y:
                dvd_icon.direction_y *= -1

            dvd_icon.update()

            # Drawing to screen
            main_surface.fill(RGB_LIST[int(curr_rgb)])
            main_surface.blit(dvd_icon.sprite, (dvd_icon.position.to_tuple()))

            pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()
