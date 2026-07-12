#Note: Always comment out all the programs here before continuing to the other program.
#Starting Graphics Window
import turtle
win = turtle.Screen()
win.setup(400, 400)
pt = turtle.Turtle()
pt.penup()
pt.goto(100, -50)
pt.pendown()
pt.dot(10)
win.exitonclick()

#Line() Function
#Line(Point (x, y), Point (x, y))
import turtle
window1 = turtle.Screen()
window1.setup(400, 300)  # Set window size
window1.title("Line Drawing")
line_turtle = turtle.Turtle(visible=False)
line_turtle.penup()
line_turtle.goto(50, -100)
line_turtle.pendown()
line_turtle.goto(200, -100)
window1.exitonclick()

#Circle() Function
#Circle(Point (x, y), val)
import turtle
window2 = turtle.Screen()
window2.setup(400, 300)
cir_turtle = turtle.Turtle(visible=False)
cir_turtle.speed(0)
cir_turtle.penup()
cir_turtle.goto(50, -100)
cir_turtle.pendown()
cir_turtle.circle(50)
window2.exitonclick()

#Rectangle() Function
#Rectangle(Point (x, y), Point (x, y)
import turtle
window3 = turtle.Screen()
window3.setup(400, 300)
rect_turtle = turtle.Turtle(visible=False)
rect_turtle.speed(0)
rect_turtle.penup()
rect_turtle.goto(50, -40)
rect_turtle.pendown()
rect_turtle.goto(100, -40)
rect_turtle.goto(100, -150)
rect_turtle.goto(50, -150)
rect_turtle.goto(50, -40)
window3.exitonclick()

#Polygon() Function
#Polygon(Point(30, 40), Point(60, 70), Point(80, 90))
import turtle
window4 = turtle.Screen()
window4.setup(400, 300)
poly_turtle = turtle.Turtle(visible=False)
poly_turtle.speed(0)
poly_turtle.penup()
poly_turtle.goto(50, -40)
poly_turtle.pendown()
poly_turtle.goto(100, -150)
poly_turtle.goto(200, -90)
poly_turtle.goto(50, -40)
window4.exitonclick()

#Text() Function
#Text(Point (x, y), "text_string")
import turtle
window5 = turtle.Screen()
window5.setup(400, 300)
text_turtle = turtle.Turtle(visible=False)
text_turtle.speed(0)
text_turtle.penup()
text_turtle.goto(100, -150)
text_turtle.write("Hello World", font=("Arial", 16, "normal"))
window5.exitonclick()

#setFill() Function
#setFill("colourname")
import turtle
window6 = turtle.Screen()
window6.setup(400, 300)
oval_turtle = turtle.Turtle(visible=False)
oval_turtle.speed(0)
oval_turtle.color("red")
oval_turtle.penup()
oval_turtle.goto(100, -130)
oval_turtle.pendown()
oval_turtle.begin_fill()
oval_turtle.circle(50, 180)
oval_turtle.goto(100, -130)
oval_turtle.end_fill()
window6.exitonclick()

#setOutline() Function
import turtle
window7 = turtle.Screen()
window7.setup(400, 300)
sq_turtle = turtle.Turtle(visible=False)
sq_turtle.speed(0)
sq_turtle.pencolor("teal")
sq_turtle.fillcolor("red")
sq_turtle.penup()
sq_turtle.goto(50, -100)
sq_turtle.pendown()
sq_turtle.begin_fill()
sq_turtle.goto(100, -100)
sq_turtle.goto(100, -150)
sq_turtle.goto(50, -150)
sq_turtle.goto(50, -100)
sq_turtle.end_fill()
window7.exitonclick()