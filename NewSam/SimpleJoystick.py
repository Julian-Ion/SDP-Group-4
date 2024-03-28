import pygame


class SimpleJoystick:

    def __init__(self) -> None:

        pygame.init()

        pygame.joystick.init()

        self.num_controllers: int = pygame.joystick.get_count()
        print(f"{self.num_controllers} controllers available")

        self.joystick = pygame.joystick.Joystick(0) # Get the controller
        self.joystick.init()

    def getValues(self) -> dict:

        """
        x_axis: -1 is left 1 is right
        y_axis: 1 is up -1 is down
        """

        for event in pygame.event.get(): # Process all events
            pass

        x_axis = self.joystick.get_axis(0)
        y_axis = self.joystick.get_axis(1)*-1 # Flipping it to make a bit more sense

        square = self.joystick.get_button(3)
        cross = self.joystick.get_button(0)
        circle = self.joystick.get_button(1)
        triangle = self.joystick.get_button(2)

        return {"x": round(x_axis, 2), "y": round(y_axis, 2), "square": square, "cross": cross, "circle": circle, "triangle": triangle}


def main() -> None:

    return None

    joystick = SimpleJoystick()

    while True:
        print(joystick.getValues())


if __name__ == "__main__":
    main()
