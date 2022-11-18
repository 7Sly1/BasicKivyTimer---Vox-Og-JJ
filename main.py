from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
# Grafiske komponenter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# Properties til interaktion mellem python og kv
from kivy.properties import StringProperty

# Kivys interne clock til timing og framerate
from kivy.clock import Clock

# Python standard biblioteker
import math

class WindowManager(ScreenManager):
    pass

class MainMenu(Screen):
    # Tekst paa knappen. Bundet via .kv. Bliver aendret i update.
    timerText = StringProperty('5')
    buttonText = StringProperty('Start timer')
    running = False  # Nedtaellingen koerer hvis sand
    expired = False
    startTime = 5  # Antal sekunder timeren starter på
    timeLeft = startTime  # Antal sekunder tilbage i nedtaellingen
    rounds = 1
    roundText = StringProperty("Rounds: " + str(rounds))

    # Skifter running til modsatte boolske vaerdi
    def toggle(self):
        if self.expired and not self.running:
            self.timeLeft = self.startTime
            self.expired = False
        else:
            self.running = not self.running

    # Taeller ned hvis running. Opdaterer buttonText ved hvert kald
    def update(self, dt):
        if self.running:
            self.timeLeft = self.timeLeft - dt
        if self.timeLeft <= 0 and self.running:
            self.toggle()
            self.expired = True

        self.timerText = str(math.ceil(self.timeLeft))

    def roundUpdate(self,dt):
        self.roundText = str(math.ceil(self.rounds))


    def timeControl(self, amount):
        self.timeLeft += amount
        self.update(1.0 / 30.0)

    def roundCount(self, amount):
        self.rounds += amount
        self.updateRounds(1.0 / 30.0)


class PlayingScreen(Screen):
    pass
class EndScreen(Screen):
    pass



class BasicTimerApp(App):

    def build(self):
        return

if __name__ in ('__main__', '__android__'):
    BasicTimerApp().run()