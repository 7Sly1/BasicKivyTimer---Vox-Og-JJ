from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.graphics import Color, Line
from kivy.clock import Clock
import math


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

    def roundControl(self, amount): # TODO: Make rounds actually do stuff
        self.rounds += amount
        if self.rounds < 1:
            self.rounds += 1
        self.updateRounds(1.0 / 30.0)
        gameManager.rounds = self.rounds


class gameManager():
    timer = MainMenu.timeLeft
    rounds = MainMenu.rounds

class PlayingScreen(Screen):
    # TODO: Game logic goes here
    gameTimer = 0
    gameTimerText = StringProperty(str(gameTimer))
    running = False
    expired = False
    gameManager.rounds -= 1

    def updateValues(self):
        PlayingScreen.gameTimer = gameManager.timer

    def update(self, dt):
        if self.running:
            self.gameTimer = self.gameTimer - dt
        if self.gameTimer <= 0 and self.running:
            self.running = False
            self.expired = True
            self.manager.current = "end"

        self.gameTimerText = str(math.ceil(self.gameTimer))

    def gameLoop(self):
        self.running = True
        Clock.schedule_interval(self.update, 1.0/30.0)

    def on_touch_down(self, touch):
        # Begynder en linje der hvor man klikker på canvas
        with self.canvas:
            Color(1, 1, 1)
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        # Når man flytter musen trækker den stregen med musen fra klik punktet
        touch.ud['line'].points += [touch.x, touch.y]


class EndScreen(Screen):
    # Handles logic for the end screen
    if gameManager.rounds > 0: # TODO: Fix
        endButtonText = StringProperty("Next Round")
    else:
        endButtonText = StringProperty("Exit")
    # TODO: See if this if logic can be simplified
    def endButton(self):
        if gameManager.rounds > 0:
            self.manager.current = "playing"
        else:
            exit()
            
# TODO: Store time values in manager to carry over for more rounds
# TODO: Clear canvas when calling playing screen again

class AmongUsApp(App):
    def build(self):
        return


if __name__ in ('__main__', '__android__'):
    AmongUsApp().run()