class Bird:
    def __init__(self, x: int, y: int, jump_force: int) -> None:
        self.x = x
        self.y = y
        self.jump_force = jump_force  # negative
        self.jumped = False
        self.velocity = 0

    def move(self, g: int,) -> None:
        self.velocity = self.jump_force if self.jumped else self.velocity + g
        self.y += self.velocity
        self.jumped = False


class Bar:
    def __init__(self, x: int, top_height: int) -> None:
        self.x = x
        self.top_height = top_height

    def move(self, del_x):
        self.x -= del_x
