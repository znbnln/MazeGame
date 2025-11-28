import turtle
import random


CELL = 30
SIZE = 15

screen = turtle.Screen()
screen.setup(700, 700)
screen.bgcolor("black")
screen.title(" Maze Game")


wall = turtle.Turtle()
wall.hideturtle()
wall.shape("square")
wall.color("white")
wall.penup()
wall.speed(0)

goal = turtle.Turtle()
goal.hideturtle()
goal.shape("square")
goal.color("green")
goal.penup()

player = turtle.Turtle()
player.shape("circle")
player.color("yellow")
player.penup()
player.speed(0)

msg = turtle.Turtle()
msg.hideturtle()
msg.color("yellow")
msg.penup()
msg.goto(0, -320)  


class Button(turtle.Turtle):
    def __init__(self, text, x, y, color, callback):
        super().__init__()
        self.hideturtle()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=2, stretch_len=6)
        self.penup()
        self.goto(x, y)
        self.showturtle()
        self.onclick(lambda x, y: callback())
       
        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.penup()
        self.label.color("white")
        self.label.goto(x, y-10)
        self.label.write(text, align="center", font=("Arial", 14, "bold"))


def generate_maze():
    maze = [[1 for _ in range(SIZE)] for _ in range(SIZE)]
    stack = [(1,1)]
    maze[1][1] = 0

    while stack:
        x, y = stack[-1]
        directions = [(x+2,y),(x-2,y),(x,y+2),(x,y-2)]
        random.shuffle(directions)
        moved = False
        for nx, ny in directions:
            if 1 <= nx < SIZE-1 and 1 <= ny < SIZE-1 and maze[ny][nx] == 1:
                maze[ny][nx] = 0
                maze[(y+ny)//2][(x+nx)//2] = 0
                stack.append((nx, ny))
                moved = True
                break
        if not moved:
            stack.pop()
            maze[SIZE-2][SIZE-2] = 0
    return maze


def draw_maze(m):
    wall.clear()
    goal.clear()
    for y in range(SIZE):
        for x in range(SIZE):
            if m[y][x] == 1:
                wall.goto(coord(x,y))
                wall.stamp()
    goal.goto(coord(SIZE-2,SIZE-2))
    goal.stamp()

def coord(x, y):
    return (x*CELL - 220, 220 - y*CELL)


maze = []
px, py = 1,1

def start_game():
    global maze, px, py
    msg.clear()
    maze = generate_maze()
    draw_maze(maze)
    px, py = 1,1
    player.goto(coord(px, py))

def move(dx, dy):
    global px, py
    nx, ny = px+dx, py+dy
    if 0 <= nx < SIZE and 0 <= ny < SIZE:
        if maze[ny][nx] == 0:
            px, py = nx, ny
            player.goto(coord(px, py))
    if px == SIZE-2 and py == SIZE-2:
        msg.clear()
        msg.write("🎉 You Win! Press Restart or Exit", align="center", font=("Arial", 16, "bold"))


def restart_game():
    start_game()
    msg.clear()

def exit_game():
    turtle.bye()


Button("Restart", -200, 300, "#0055ff", restart_game)
Button("Exit", 200, 300, "#aa0000", exit_game)


screen.listen()
screen.onkey(lambda: move(1,0),"Right")
screen.onkey(lambda: move(-1,0),"Left")
screen.onkey(lambda: move(0,-1),"Up")
screen.onkey(lambda: move(0,1),"Down")


start_game()
turtle.mainloop()
