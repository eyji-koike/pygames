# Pong game made by @eyji-koike under apache 2.0 licensing
# simple pong game made with python by eyji

import sys
import turtle
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("..")

    return os.path.join(base_path, relative_path)


# check which system we are on and define the right sound play
def play_sound(path):
    if sys.platform.startswith('win'):
        import winsound
        winsound.PlaySound("{}".format(path), winsound.SND_ASYNC)
    elif sys.platform.startswith('linux'):
        os.system("aplay {}&".format(path))
    elif sys.platform.startswith('darwin'):
        os.system("afplay {}&".format(path))


# Set up our window
window_width = 800
window_height = 600
window = turtle.Screen()
window.title('Pong by @eyji-koike')
window.bgcolor('black')
window.setup(window_width, window_height)
window.tracer(0)


# A Class to make Paddles
class Paddle:
    # here we state our paddle object and its properties
    def __init__(self):
        self.paddle = turtle.Turtle()
        self.paddle.speed(0)
        self.paddle.shape('square')
        self.paddle.shapesize(stretch_wid=5, stretch_len=1)
        self.paddle.color('white')
        self.paddle.penup()

    # here we define the moving proprieties
    def paddle_up(self):
        y = self.paddle.ycor()
        y += 20
        self.paddle.sety(y)

    def paddle_down(self):
        y = self.paddle.ycor()
        y -= 20
        self.paddle.sety(y)


# a class to make balls
class Ball:
    def __init__(self):
        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.shape('circle')
        self.ball.shapesize(stretch_wid=1, stretch_len=1)
        self.ball.color('white')
        self.ball.penup()


# a class to make pens
class Pen:
    def __init__(self):
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.color('white')
        self.pen.penup()
        self.pen.hideturtle()


# paddle left
paddle_left = Paddle()
paddle_left.paddle.goto(-350, 0)

# paddle left
paddle_right = Paddle()
paddle_right.paddle.goto(350, 0)

# ball
ball = Ball()
ball.ball.goto(0, 0)
ball.ball.dx = 2
ball.ball.dy = 2

# Pen
pen = Pen()
pen.pen.goto(0, ((window_height / 2) * 0.90))

# score
score_left = 0
score_right = 0

wall_bounce_url = resource_path('sound_effects/wall_bounce.wav')
paddle_bounce_url = resource_path('sound_effects/paddle_bounce.wav')
point_bounce_url = resource_path('sound_effects/point.wav')
# main loop
while True:
    window.update()
    window.listen()
    pen.pen.clear()
    pen.pen.write("Player A: {} | Player B: {}".format(score_left, score_right),
                  align="center",
                  font=("Courier", 24, "normal"))
    # key bindings
    window.onkeypress(paddle_left.paddle_up, 'w')
    window.onkeypress(paddle_left.paddle_down, 's')
    window.onkeypress(paddle_right.paddle_up, 'i')
    window.onkeypress(paddle_right.paddle_down, 'k')
    # start the ball
    ball.ball.setx(ball.ball.xcor() + ball.ball.dx)
    ball.ball.sety(ball.ball.ycor() + ball.ball.dy)

    # border checks
    # bounce in the walls
    if ball.ball.ycor() > ((window_height / 2) - 10):
        ball.ball.sety(((window_height / 2) - 10))
        ball.ball.dy *= -1
        play_sound(wall_bounce_url)
    if ball.ball.ycor() < (-(window_height / 2) + 20):
        ball.ball.sety(-(window_height / 2) + 20)
        ball.ball.dy *= -1
        play_sound(wall_bounce_url)
    # restart if it goes past the paddle
    if ball.ball.xcor() > ((window_width / 2) - 10):
        ball.ball.goto(0, 0)
        ball.ball.dx *= -1
        score_left += 1
        play_sound(point_bounce_url)
    if ball.ball.xcor() < (-(window_width / 2)):
        ball.ball.goto(0, 0)
        ball.ball.dx *= -1
        score_right += 1
        play_sound(point_bounce_url)

    # paddle checks
    if ball.ball.xcor() > ((window_height / 2) + 30) and (
            paddle_right.paddle.ycor() + 40 > ball.ball.ycor() > paddle_right.paddle.ycor() - 40):
        ball.ball.setx((window_height / 2) + 30)
        ball.ball.dx *= -1
        play_sound(paddle_bounce_url)
    if ball.ball.xcor() < (-(window_height / 2) - 30) and (
            paddle_left.paddle.ycor() + 40 > ball.ball.ycor() > paddle_left.paddle.ycor() - 40):
        ball.ball.setx(-(window_height / 2) - 30)
        ball.ball.dx *= -1
        play_sound(paddle_bounce_url)
