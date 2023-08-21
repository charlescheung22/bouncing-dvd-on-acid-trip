from math import cos, radians, pi
import pygame

# Constants
FPS: int = 144
DVD_LOGO_PATH: str = "../images/DVD logo.png"
# Generate a list of RGB values for background color cycling.
RGB_LIST: list[tuple[int, int, int]] = [(
    int(max(255 / 3 * (cos(3 * radians(degree) + 0 * pi / 3) + 1.5), 0)),
    int(max(255 / 3 * (cos(3 * radians(degree) + 2 * pi / 3) + 1.5), 0)),
    int(max(255 / 3 * (cos(3 * radians(degree) + 4 * pi / 3) + 1.5), 0))
) for degree in range(360)]  # Each entry has an RGB value to cycle through.


class Logo:
    def __init__(self, image_path: str, position: tuple[int, int]) -> None:
        """
        Logo class constructor.

        :parameter image_path: A string representing the path to the DVD logo from the current directory.
        :parameter position: A tuple pair of coordinates, which will be converted to a vector.
        """
        self.sprite = pygame.image.load(image_path)
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(1, 1)

    def update(self) -> None:
        """Update the current position with the current direction."""
        self.position += self.direction
        # Collision detection will be handled in the main loop

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the DVD logo on a given surface.

        :param surface: Pygame surface to draw the logo on.
        """
        surface.blit(self.sprite, self.position)


def handle_events() -> str:
    """
    Handle Pygame events and determine whether to continue the screensaver or quit.

    :return: Either "Screensaver" to continue or "Quit" to exit.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "Quit"
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            return "Quit"
    return "Screensaver"


def main():
    pygame.init()
    curr_rgb = 0  # RGB index for background color cycling.

    flag_bounced: bool = False

    # Getting screen dimensions
    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h
    main_surface = pygame.display.set_mode((screen_width, screen_height))

    dvd_icon = Logo(DVD_LOGO_PATH, (0, 0))
    dvd_bound_x = screen_width - dvd_icon.width
    dvd_bound_y = screen_height - dvd_icon.height

    mode = "Screensaver"
    while mode == "Screensaver":
        # Handle events
        mode = handle_events()

        dvd_icon.update()
        # Check for collisions with screen boundaries and reverse direction if necessary
        if dvd_icon.position.x <= 0 or dvd_icon.position.x >= dvd_bound_x:
            dvd_icon.direction.x *= -1
            flag_bounced = True
        if dvd_icon.position.y <= 0 or dvd_icon.position.y >= dvd_bound_y:
            dvd_icon.direction.y *= -1
            flag_bounced = True

        # Update position after handling collisions
        if flag_bounced:
            dvd_icon.update()
            flag_bounced = False

        # Render DVD logo and background
        main_surface.fill(RGB_LIST[int(curr_rgb)])
        dvd_icon.draw(main_surface)
        pygame.display.flip()

        curr_rgb += 1 / 20
        curr_rgb %= 360

    pygame.quit()



if __name__ == "__main__":
    main()
