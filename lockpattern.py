import pygame


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900

colors = {
    'unselected': (0, 0, 0),
    'selected': (150, 75, 0),
    'line': (0, 0, 255)
}


class Window:
    def __init__(self):
        # setup window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        # fps for clean lock patterning
        self.FPS = 60

        # TODO: handle user input
        square_length = 3
        self.lock_pattern = LockPattern(square_length)

        # run the program!
        self.running = True

    def main_loop(self):
        # main window loop
        while self.running:
            self.get_events()
            self.update()
            self.render()

        # quit pygame once loop is over
        pygame.quit()

    def get_events(self):
        # get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # check if mouse button is held
            mouse_buttons = pygame.mouse.get_pressed()
            # lets any mouse button be held
            if any(mouse_buttons):
                # selected is either a dot or None
                selected = self.lock_pattern.check_selection(
                    pygame.mouse.get_pos()
                )

                # if a dot and not in stack, add to stack
                self.lock_pattern.add_to_selection(selected)

            # clear once lifted
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.lock_pattern.clear_selection()

    def update(self):
        # tick tock
        self.clock.tick(self.FPS)

    def render(self):
        # simple window
        self.screen.fill('white')
        self.lock_pattern.render(self.screen)
        pygame.display.flip()


class LockPattern:
    def __init__(self, square_length: int):
        # length of lockpattern square
        self.square_length = square_length
        # size of dot
        self.dot_radius = 50
        # gap between dots
        self.gap = (7 / 6 * SCREEN_WIDTH) // self.square_length
        # arbitrary thickness
        self.thickness = 10
        # currently set to a radius length, tweak as you'd like
        self.error = self.dot_radius

        # init dots
        self.dots = []
        # square the range
        for i in range(square_length**2):
            self.dots.append(
                Dot(
                    # all start as black
                    colors['unselected'],
                    # evenly spaced
                    pygame.math.Vector2(
                        SCREEN_WIDTH // 9 + self.gap * \
                        (i % self.square_length),
                        SCREEN_HEIGHT // 9 + self.gap * \
                        (i // self.square_length)
                    ),
                    # preset dot radius
                    self.dot_radius
                )
            )

        # add dots that are currently in the lock pattern
        self.selected_stack = []

    # TODO: add return type for Dot
    def check_selection(self, mouse_pos: tuple):
        # check if mouse_pos is close enough to dot,
        # uses self.error bc we love a user-friendly experience <3
        for dot in self.dots:
            distance = pygame.math.Vector2(mouse_pos).distance_to(dot.position)
            if distance < self.dot_radius + self.error:
                dot.selected = True
                return dot
        return None

    def add_to_selection(self, dot):
        # if a dot, add it to the stack of selected
        if dot and dot not in self.selected_stack:
            self.selected_stack.append(dot)
            dot.update_color(colors['selected'])

    def clear_selection(self):
        # when mouse is lifted, reset everthing back to normal
        for dot in self.dots:
            dot.selected = False
            dot.update_color(colors['unselected'])
        self.selected_stack = []

    def render(self, screen):
        # once the stack has something, track mouse movement
        if len(self.selected_stack) > 0:
            last = self.selected_stack[-1]
            for i in range(len(self.selected_stack)):
                # last is the one following the mouse
                if self.selected_stack[i] == last:
                    pygame.draw.line(screen, colors['line'],
                                     self.selected_stack[i].position,
                                     pygame.mouse.get_pos(),
                                     self.thickness)
                    break
                pygame.draw.line(screen, colors['line'],
                                 self.selected_stack[i].position,
                                 self.selected_stack[i + 1].position,
                                 self.thickness)
        for dot in self.dots:
            dot.draw(screen)


class Dot:
    def __init__(self, color, position, radius):
        self.selected = False
        self.color = color
        self.position = position
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def update_color(self, color):
        self.color = color
