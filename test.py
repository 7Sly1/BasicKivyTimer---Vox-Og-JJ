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
    timerText = StringProperty('5')
    running = False
    expired = False
    startTime = 5
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
        self.update(1.0 / 30.0)


class PlayingScreen(Screen):
    pass


class EndScreen(Screen):
    pass


class AmongUsApp(App):
    def build(self):
        return


if __name__ in ('__main__', '__android__'):
    AmongUsApp().run()