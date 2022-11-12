from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Grafiske komponenter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# Properties til interaktion mellem python og kv
from kivy.properties import StringProperty
from kivy.clock import Clock
import math


class WindowManager(ScreenManager):
    pass


class MainMenu(Screen):
    startTime = 5
    timerText = StringProperty(str(startTime))
    running = False
    expired = False
    timeLeft = startTime

    # Skifter running til modsatte boolske vaerdi
    def toggle(self):
        if self.expired and not self.running:
            self.timeLeft = self.startTime
            self.expired = False
        else:
            self.running = not self.running

    def update(self, dt):
        if self.running:
            self.timeLeft = self.timeLeft - dt
        if self.timeLeft <= 0 and self.running:
            self.toggle()
            self.expired = True

        self.timerText = str(math.ceil(self.timeLeft))

    def timeControl(self, amount):
        self.timeLeft += amount
        if self.timeLeft < 0:
            self.timeLeft += 1
        self.update(1.0 / 30.0)
        return self.timeLeft

    # TODO: Figure out how to transfer timeLeft from this class to another
    # TODO: Seems like it takes the "default" value instead of the changed..


class PlayingScreen(Screen):
    # TODO: Game logic goes here
    gameTimerText = MainMenu.timerText
    gameTimer = MainMenu.timeLeft
    running = False
    expired = False

    def update(self, dt):
        if self.running:
            self.gameTimer = self.gameTimer - dt
        if self.gameTimer <= 0 and self.running:
            print("UH OH YOU DONE!") # TODO: Change to end screen
            self.running = False
            self.expired = True

        self.gameTimerText = str(math.ceil(self.gameTimer))

    def gameLoop(self):
        self.running = True
        Clock.schedule_interval(self.update, 1.0/30.0)
        return self


class EndScreen(Screen):
    # TODO: End screen logic goes here
    pass


class AmongUsApp(App):
    def build(self):
        return


if __name__ in ('__main__', '__android__'):
    AmongUsApp().run()