import pygame
import random
import ctypes

size = 600
rows = 20


class Cube():
    size = size
    rows = rows

    def __init__(self, start, x=1, y=0, colour=(235, 172, 113)):
        self.pos = start
        self.direction_x = x
        self.direction_y = y
        self.__color = colour  # default color of the body is set within the default variable colour

    def move(self, x, y):
        self.direction_x = x
        self.direction_y = y
        self.pos = (self.pos[0] + self.direction_x, self.pos[1] + self.direction_y)

    def draw(self, window):
        dist = self.size // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(window, self.__color, (i * dist + 1, j * dist + 1, dist - 1, dist - 1))


class Snake():
    body = []
    turns = {}

    def __init__(self, colour, pos):
        self.__colour = colour
        self.__head = Cube(pos, colour=colour)
        self.body.append(self.__head)

        # directions for (x,y)
        self.direction_x = 0
        self.direction_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()  # list of all key values that have been pressed
            for key in keys:
                if keys[pygame.K_LEFT]:
                    # we go left, which means we gotta decrement the x coordinate
                    self.direction_x = -1
                    self.direction_y = 0

                    # we gotta remember where we took a turn
                    self.turns[self.__head.pos[:]] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_RIGHT]:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turns[self.__head.pos[:]] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_UP]:
                    self.direction_x = 0
                    self.direction_y = -1
                    self.turns[self.__head.pos[:]] = [self.direction_x, self.direction_y]
                elif keys[pygame.K_DOWN]:
                    self.direction_x = 0
                    self.direction_y = 1
                    self.turns[self.__head.pos[:]] = [self.direction_x, self.direction_y]

        for index, cube in enumerate(self.body):
            p = cube.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                cube.move(turn[0], turn[1])
                # at the last cube = end of tail, we remove the existence of the turn
                if index == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # taking into consideration the margins of the game when moving
                if cube.direction_x == -1 and cube.pos[0] <= 0:
                    cube.pos = (cube.rows - 1, cube.pos[1])
                elif cube.direction_x == 1 and cube.pos[0] >= cube.rows - 1:
                    cube.pos = (0, cube.pos[1])
                elif cube.direction_y == 1 and cube.pos[1] >= cube.rows - 1:
                    cube.pos = (cube.pos[0], 0)
                elif cube.direction_y == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], cube.rows - 1)
                else:
                    # simply move the cube in case it's not at the edge of the screen
                    cube.move(cube.direction_x, cube.direction_y)

    def draw(self, window):
        for index, cube in enumerate(self.body):
            cube.draw(window)

    def add(self):
        # adding a new cube to the tail after the snake ate the food
        tail = self.body[-1]
        x, y = tail.direction_x, tail.direction_y

        if x == 1 and y == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif x == -1 and y == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif x == 0 and y == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif x == 0 and y == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        # adding the direction to the new cube so it knows where to move next
        self.body[-1].direction_x = x
        self.body[-1].direction_y = y

    def reset(self, pos):
        # resets snake
        self.__head = Cube(pos, colour=self.__colour)
        self.body = []
        self.body.append(self.__head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1


def generateFood(rows, snek):
    position = snek.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda x: x.pos == (x, y), position))) > 0:
            continue
        else:
            break

    return (x, y)


def drawWindow(window, size, rows, snek, food):
    # window.fill((255, 255, 255))
    window.fill((0, 0, 0))

    snek.draw(window)
    food.draw(window)

    pygame.display.update()


def main():
    window = pygame.display.set_mode((size, size))

    snek = Snake((232, 129, 32), (1, 1))  # we also give here the head colour of the snake
    food = Cube(generateFood(rows, snek), colour=(149, 196, 152))

    while True:
        # the lower the delay between steps, the faster it's gonna move
        pygame.time.delay(90)

        snek.move()
        if snek.body[0].pos == food.pos:
            snek.add()
            food = Cube(generateFood(rows, snek), colour=(149, 196, 152))

        for x in range(len(snek.body)):
            if snek.body[x].pos in list(map(lambda z: z.pos, snek.body[x + 1:])):
                message = 'Score: ' + str(len(snek.body))
                ctypes.windll.user32.MessageBoxW(0, message, "Game Over", 1)

                # reset the snake and the food after the game is over
                snek.reset((10, 10))
                food = Cube(generateFood(rows, snek), colour=(149, 196, 152))
                break

        drawWindow(window, size, rows, snek, food)


main()
