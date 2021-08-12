from sources import *
import turtle as t

# settings
fps = 40

creator = t.Turtle()
check = t.Turtle()
screen = t.Screen()
canvas = screen.getcanvas()

level = 1

lv_data = [(Block(0, 0), 'B'), (Goal(1, 0), 'G')]
items = len(lv_data)
origin = [0, 0]


def init():
    global creator, screen, fps

    screen.setup(960, 672, 100, 100)
    screen.setworldcoordinates(0, 672, 960, 0)
    screen.tracer(0, 0)
    screen.title("Editor")
    screen.ontimer(update, 1000 // fps)

    screen.onclick(editor)
    screen.onclick(remover, btn=3)
    screen.onkeyrelease(command, '/')

    screen.bgcolor('#DDDDDD')

    creator.ht()
    creator.pu()
    creator.speed(0)
    check.turtlesize(3)
    check.pu()
    check.color('red')
    check.lt(90)
    check.ht()
    check.goto(grid / 2, grid / 2)

    xygrid()

    screen.listen()


def xygrid():
    creator.pencolor('black')
    for ypos in range(32, 641, 16):
        creator.pu()
        creator.goto(0, ypos)
        creator.pd()
        creator.goto(960, ypos)

    for xpos in range(0, 961, 16):
        creator.pu()
        creator.goto(xpos, 32)
        creator.pd()
        creator.goto(xpos, 640)
    creator.pu()


def update():
    global char, lv_data, creator, screen, check

    creator.clear()

    xygrid()
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


selection = 0


def editor(x, y):
    global selection
    if 0 <= x and x <= grid and 0 <= y and y <= grid:
        selection = 1
        check.goto(grid / 2, grid / 2)
        check.st()
    elif grid < x and x <= 2 * grid and 0 <= y and y <= grid:
        selection = 2
        check.goto(3 * grid / 2, grid / 2)
        check.st()
    elif selection == 1:
        if x < 0 or y < 32:
            selection = 0
            check.ht()
        xpos = (x // 16) / 2
        ypos = (y // 16) / 2
        new = Block(xpos, ypos)
        lv_data.append((new, 'B'))
    elif selection == 2:
        if x < 0 or y < 32:
            selection = 0
            check.ht()
        xpos = (x // 16) / 2
        ypos = (y // 16) / 2
        new = Goal(xpos, ypos)
        lv_data.append((new, 'G'))


def remover(x, y):
    if x > 0 and y > 32:
        xpos = (x // 16) / 2
        ypos = (y // 16) / 2
        rm = False

        for block in Block.data:
            if block.x == xpos and block.y == ypos:
                rm = block

        if rm != False:
            Block.data.remove(rm)
            for data in lv_data:
                if data[0] == rm:
                    lv_data.remove(data)
            del rm


class CommandError(TypeError):
    pass


def command():
    global lv_data, origin, items
    uinput = screen.textinput("Command Prompt", "Command : ").split(" ")
    screen.listen()
    if uinput[0] == "clear":
        Block.data = [Block.data[0]]
        lv_data = [lv_data[0]]
    elif uinput[0] == "origin":
        if len(uinput) > 3:
            raise CommandError(f"Origin takes 2 positional arguments but {len(uinput) - 1} were given.")
        elif len(uinput) == 1:
            raise CommandError("Origin takes 2 positional arguments but none were given.")
        elif len(uinput) == 2:
            raise CommandError("Origin takes 2 positional arguments but 1 was given.")
        origin = [float(uinput[1]), float(uinput[2])]
        print(f"Origin was set to {origin}")
    elif uinput[0] == 'exit':
        print(' '.join(uinput[1:]))
        screen.bye()
    elif uinput[0] == 'save':
        if len(uinput) > 2:
            raise CommandError(f"Save takes 1 positional argument but {len(uinput) - 1} were given.")
        elif len(uinput) == 1:
            raise CommandError("Save takes 1 positional argument but none were given.")
        with open(uinput[1] + ".lvdata", mode="w") as f:
            f.write(f"{origin[0]} {origin[1]}\n")
            for data in lv_data[items:]:
                f.write(str(data) + "\n")
    else:
        raise CommandError("No such command exists")


if __name__ == "__main__":
    init()
    screen.mainloop()
