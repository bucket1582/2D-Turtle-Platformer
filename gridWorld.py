from sources import *
import turtle as t

# settings
fps = 60

creator = t.Turtle()
screen = t.Screen()

level = 1

char = None
collide = 6
speed = 4

lv_data = None
origin = [0, 0]


def load(fname):
    global origin, lv_data
    f = open(fname).read()
    data = f.split('\n')
    origin = list(map(lambda x: float(x), data[0].split(' ')))
    lv_data = list(map(lambda x: eval(x), data[1:-1]))


def init():
    global creator, screen, fps, char, collide, origin

    screen.setup(960, 640, 100, 100)
    screen.setworldcoordinates(0, 640, 960, 0)
    screen.tracer(0, 0)
    screen.title("Platformer")

    screen.onkeypress(press_A, 'a')
    screen.onkeypress(press_D, 'd')
    screen.onkeypress(stuck, 'r')

    screen.bgcolor('gray')

    char = Character(origin, collide)
    char.accel[1] = gravity

    creator.ht()
    creator.pu()
    creator.color('#99FFFF', '#FFFFFF')
    creator.speed(0)

    screen.listen()
    update()


def update():
    global char, lv_data, creator, screen

    char.physics()
    if not char.is_alive():
        char.respawn()

    if char.status == 'G':
        print("Goal!")
        screen.bye()

    creator.clear()

    # Main Character
    creator.color('#FFFF00', '#FFFF00')
    creator.goto(char.x, char.y - collide)
    creator.begin_fill()
    creator.circle(collide)
    creator.end_fill()

    # Blocks
    for data in lv_data:
        if data[1] == 'B':
            creator.color('#66FFFF', '#FFFFFF')
            creator.goto(grid * data[0].x, grid * data[0].y)
            creator.pd()
            creator.begin_fill()
            creator.goto(grid * data[0].x, grid * (data[0].y + 1))
            creator.goto(grid * (data[0].x + 1), grid * (data[0].y + 1))
            creator.goto(grid * (data[0].x + 1), grid * data[0].y)
            creator.goto(grid * data[0].x, grid * data[0].y)
            creator.end_fill()
            creator.pu()
        if data[1] == 'G':
            creator.color('#66FF00', '#66FF00')
            creator.goto(grid * data[0].x + grid / 2, grid * data[0].y)
            creator.begin_fill()
            creator.circle(grid / 2)
            creator.end_fill()

    screen.update()
    screen.ontimer(update, 1000 // fps)


def press_A():
    global speed, screen, char
    char.velocity[0] -= speed
    screen.onkeypress(None, 'a')  # going left and right at the same time is an invalid move.
    screen.onkeypress(None, 'd')
    screen.onkeyrelease(release_A, 'a')


def release_A():
    global char, screen
    char.velocity[0] = 0
    screen.onkeypress(press_A, 'a')
    screen.onkeypress(press_D, 'd')


def press_D():
    global speed, char, screen
    char.velocity[0] += speed
    screen.onkeypress(None, 'a')  # going left and right at the same time is an invalid move.
    screen.onkeypress(None, 'd')
    screen.onkeyrelease(release_D, 'd')


def release_D():
    global char, screen
    char.velocity[0] = 0
    screen.onkeypress(press_A, 'a')
    screen.onkeypress(press_D, 'd')


def stuck():
    char.respawn()


if __name__ == "__main__":
    load("tutorial.lvdata")
    init()
    screen.mainloop()
