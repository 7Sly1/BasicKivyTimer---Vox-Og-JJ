from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.graphics import Color, Line, InstructionGroup
from kivy.clock import Clock
import math
from random import randint
from time import sleep
from os import remove


class WindowManager(ScreenManager):
    pass


class MainMenu(Screen):
    startTime = 5
    timerText = StringProperty("Time: " + str(startTime))
    running = False
    expired = False
    timeLeft = startTime
    rounds = 1
    roundText = StringProperty("Rounds: " + str(rounds))

    # Skifter running til modsatte boolske vaerdi
    def toggle(self):
        if self.expired and not self.running:
            self.timeLeft = self.startTime
            self.expired = False
        else:
            self.running = not self.running

    def updateTimer(self, dt):
        self.timerText = "Time: " + str(math.ceil(self.timeLeft))

    def updateRounds(self, dt):
        self.roundText = "Rounds: " + str(math.ceil(self.rounds))

    def timeControl(self, amount):
        self.timeLeft += amount
        if self.timeLeft < 1:
            self.timeLeft += 1
        self.updateTimer(1.0 / 30.0)
        gameManager.timer = self.timeLeft

    def roundControl(self, amount):
        self.rounds += amount
        if self.rounds < 1:
            self.rounds += 1
        self.updateRounds(1.0 / 30.0)
        gameManager.rounds = self.rounds


class gameManager():
    timer = MainMenu.timeLeft
    rounds = MainMenu.rounds
    objective = ""


class PlayingScreen(Screen):
    # TODO: Game logic goes here
    gameTimer = 0
    gameTimerText = StringProperty(str(gameTimer))
    running = False
    expired = False
    objectiveText = StringProperty("")
    toRemove = []
    objects = []
    drawing = False

    def getObjective(self):
        possible = ['Monkey', 'Cat', 'Bike', 'Car', 'Dog', 'House', 'Lightbulb']
        objID = randint(0, len(possible) - 1)
        gameManager.objective = possible[objID]
        return possible[objID]

    def updateValues(self):
        gameManager.rounds -= 1
        self.gameTimer = gameManager.timer
        self.objectiveText = self.getObjective()

    def update(self, dt):
        if self.running:
            self.gameTimer = self.gameTimer - dt
        if self.gameTimer <= 0 and self.running:
            self.running = False
            self.expired = True
            Clock.unschedule(self.update)
            self.removeLines()
            self.manager.current = "end"

        self.gameTimerText = str(math.ceil(self.gameTimer))

    def gameLoop(self):
        self.running = True
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_touch_up(self, touch):
        self.drawing = False

    def on_touch_move(self, touch):
        if self.drawing:
            self.points.append(touch.pos)
            self.obj.children[-1].points = self.points
        else:
            self.drawing = True
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
        # Loops through all of our instructions
        self.export_to_png("Drawing.png")
        for i in range(0, len(self.objects)):
            item = self.objects.pop(-1)
            self.toRemove.append(item)
            # We remove the instruction from the canvas to clear it without removing all of our layout.
            self.canvas.remove(item)


class EndScreen(Screen):
    # Handles logic for the end screen

    endButtonText = StringProperty("")
    objectiveText = StringProperty("")

    def updateText(self):
        self.ids.imageView.reload()
        self.objectiveText = gameManager.objective

    def nextScreen(self):
        sleep(5)
        if gameManager.rounds > 0:
            self.manager.current = "playing"
        else:
            remove('Drawing.png')
            exit()


class SpeedDrawApp(App):
    def build(self):
        return


if __name__ in ('__main__', '__android__'):
    SpeedDrawApp().run()
