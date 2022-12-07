# Imports the needed graphical components from Kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.graphics import Color, Line, InstructionGroup
from kivy.clock import Clock
# Imports math for the timer logic
import math
# Imports randint from random for getting a random objective to draw
from random import randint
# Imports sleep from time to have the program wait on the end screen
from time import sleep
# Imports remove from os so the program can delete the image again.
from os import remove


class WindowManager(ScreenManager):
    # This class just has to be defined for Kivy's ScreenManger logic to work properly.
    pass


class MainMenu(Screen):
    # Initializes needed variables
    startTime = 5
    timerText = StringProperty("Time: " + str(startTime))
    running = False
    expired = False
    timeLeft = startTime
    rounds = 1
    roundText = StringProperty("Rounds: " + str(rounds))

    def updateTimer(self, dt):
        self.timerText = "Time: " + str(math.ceil(self.timeLeft))

    # These two update functions update the text on the screen.

    def updateRounds(self, dt):
        self.roundText = "Rounds: " + str(math.ceil(self.rounds))

    def timeControl(self, amount):
        # Subtracts or adds seconds to the timer and calls the text update.
        self.timeLeft += amount
        if self.timeLeft < 1:
            self.timeLeft += 1
        self.updateTimer(1.0 / 30.0)
        gameManager.timer = self.timeLeft

    def roundControl(self, amount):
        # Subtracts or adds rounds to the timer and calls the text update.
        self.rounds += amount
        if self.rounds < 1:
            self.rounds += 1
        self.updateRounds(1.0 / 30.0)
        gameManager.rounds = self.rounds


class gameManager():
    # This class serves as a "middle man" between functions for variables to stay the same throughout classes
    # This is so that other classes can access variables set by another class.
    timer = MainMenu.timeLeft
    rounds = MainMenu.rounds
    objective = ""


class PlayingScreen(Screen):
    # Initializes needed variables
    gameTimer = 0
    gameTimerText = StringProperty(str(gameTimer))
    running = False
    expired = False
    objectiveText = StringProperty("")
    objects = []
    drawing = False

    def getObjective(self):
        # Gets a random string from the list and returns it so it can be shown on the screen.
        possible = ['Monkey', 'Cat', 'Bike', 'Car', 'Dog', 'House', 'Lightbulb']
        objID = randint(0, len(possible) - 1)
        gameManager.objective = possible[objID]
        return possible[objID]

    def updateValues(self):
        # Updates values and gets a new objective to draw.
        gameManager.rounds -= 1
        self.gameTimer = gameManager.timer
        self.objectiveText = self.getObjective()

    def update(self, dt):
        # Updates the timer if it's running
        if self.running:
            self.gameTimer = self.gameTimer - dt
        if self.gameTimer <= 0 and self.running:
            # If it's not running stop updating, remove all lines on the canvas and change to the end screen.
            self.running = False
            self.expired = True
            Clock.unschedule(self.update)
            self.removeLines()
            self.manager.current = "end"

        # Updates the timer text.
        self.gameTimerText = str(math.ceil(self.gameTimer))

    def gameLoop(self):
        # Function to call to start the update loop.
        self.running = True
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_touch_up(self, touch):
        # Makes sure that the screen is only drawn to when the mouse button is down.
        self.drawing = False

    def on_touch_move(self, touch):
        if self.drawing:
            # Gets the new position of the drawing
            self.points.append(touch.pos)
            # Makes sure the objects position is the new position
            self.obj.children[-1].points = self.points
        else:
            self.drawing = True
            # Gets the position of where there has been drawn.
            self.points = [touch.pos]
            # We create a "group" (Basically just a list but Kivy edition) for our instructions to store them
            self.obj = InstructionGroup()
            # We add the line and color to the group
            self.obj.add(Color(1, 1, 1, 1))
            self.obj.add(Line())
            # We append the instruction to a normal list
            self.objects.append(self.obj)
            # We finally add the instruction to the actual canvas and draw it.
            self.canvas.add(self.obj)

    def removeLines(self):
        # Saves the canvas to an image so it can be shown on the next screen.
        self.export_to_png("Drawing.png")
        # Loops through all of our instructions
        for i in range(0, len(self.objects)):
            item = self.objects.pop(-1)
            # We remove the instruction from the canvas to clear it without removing all of our layout.
            self.canvas.remove(item)


class EndScreen(Screen):
    # Initializes needed variables
    endButtonText = StringProperty("")
    objectiveText = StringProperty("")

    def updateText(self):
        # Updates text and reloads the image with the new image of the canvas
        self.ids.imageView.reload()
        self.objectiveText = gameManager.objective

    def nextScreen(self):
        # Waits 5 seconds so the user has time to look at the image
        sleep(5)
        # Checks if there are more rounds. If there is then it switches back to the playing screen.
        if gameManager.rounds > 0:
            self.manager.current = "playing"
        # If there isn't it removes the image file and exits the program.
        else:
            remove('Drawing.png')
            exit()


class SpeedDrawApp(App):
    # Builds the app within Kivy
    def build(self):
        # Has to return nothing because the layout is dynamic.
        return


# Makes sure the app is run on it's own and not as a module or package.
if __name__ in ('__main__', '__android__'):
    SpeedDrawApp().run()
