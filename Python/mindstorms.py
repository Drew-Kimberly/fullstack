import turtle



def initCanvas():

    #Create Screen
    window = turtle.Screen()
    window.bgcolor("red")
    return window


def initTurtles():

    #Create brad
    brad = turtle.Turtle()
    brad.shape("turtle")
    brad.color("yellow")
    brad.speed(20)

    #Create stanley
    stanley = turtle.Turtle()
    stanley.shape("classic")
    stanley.color("blue")

    #Create jeff
    jeff = turtle.Turtle()
    jeff.shape("triangle")
    jeff.color("green")

    return [brad, stanley, jeff]


def drawSq(turtleObj, sideLength):

    #draw square
    for i in range(4):
        turtleObj.forward(sideLength)
        turtleObj._rotate(90)


def drawCircle(turtleObj, radius):

    #draw circle
    turtleObj.circle(radius)


def drawTriangle(turtleObj, sideLength):

    #draw triangle
    for i in range(3):
        turtleObj.forward(sideLength)
        turtleObj._rotate(120)




canvas = initCanvas()
[brad, stanley, jeff] = initTurtles()
for i in range(360):
    drawSq(brad, 100)
    brad._rotate(271)
# drawCircle(turtles[1], 100)
# drawTriangle(turtles[2], 100)

#Exit window
canvas.exitonclick()


