# Sources for level.

screen = [960, 640]
gravity = 0.3
grid = 32

addition = 2


class Block:
    data = []

    def __init__(self, x, y):
        self.type = type
        self.x = x
        self.y = y
        Block.data.append(self)

    def __repr__(self):
        return f"Block({self.x}, {self.y})"

    def collide(self, other):
        if grid * self.x - other.x <= other.col and grid * self.x - other.x > 0:
            other.velocity[0] *= -1
        elif other.x - grid * (self.x + 1) <= other.col and other.x - grid * (self.x + 1) > 0:
            other.velocity[0] *= -1
        elif grid * self.y - other.y <= other.col and grid * self.y - other.y > 0:
            other.velocity[1] = -7
        elif other.y - grid * (self.y + 1) <= other.col and other.y - grid * (self.y + 1) > 0:
            other.velocity[1] *= -1

    def pushoff(self, other):
        inblockx = other.x - grid * self.x
        inblocky = other.y - grid * self.y
        antix = grid - inblockx
        antiy = grid - inblocky
        distances = [inblockx, inblocky, antix, antiy]

        if min(distances) == inblocky:
            other.y -= inblocky + other.col
        elif min(distances) == antiy:
            other.y += antiy + other.col
        elif min(distances) == inblockx:
            other.x -= inblockx + other.col
        else:
            other.x += antix + other.col


class Entity:
    def __init__(self, spawn, collision_circle):
        self.spawn = spawn
        self.x = spawn[0]
        self.y = spawn[1]
        self.velocity = [0, 0]
        self.accel = [0, 0]
        self.col = collision_circle
        self.status = 'P'


class Character(Entity):
    def physics(self):
        self.block_collision()
        self.velocity[0] += self.accel[0]
        self.velocity[1] += self.accel[1]
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def block_collision(self):
        for block in Block.data:
            if grid * block.x - self.col <= self.x and grid * (block.x + 1) + self.col >= self.x \
                    and grid * block.y - self.col <= self.y and grid * (block.y + 1) + self.col >= self.y:
                block.pushoff(self)
            if grid * block.x - self.col <= self.x and grid * (block.x + 1) + self.col >= self.x \
                    and grid * block.y - self.col <= self.y and grid * (block.y + 1) + self.col >= self.y:
                block.collide(self)

    def respawn(self):
        self.x = self.spawn[0]
        self.y = self.spawn[1]
        self.velocity = [0, 0]
        self.accel = [0, gravity]

    def is_alive(self):
        if self.y >= 640:
            return False
        else:
            return True

    def goal(self):
        self.status = 'G'


class Goal(Block):
    def __repr__(self):
        return f"Goal({self.x}, {self.y})"

    def collide(self, other):
        pass

    def pushoff(self, other):
        other.goal()
