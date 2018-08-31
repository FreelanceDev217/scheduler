# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 11:58:37 2018

@author: Sandman
"""

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.dropdown import DropDown
#from kivy.uix.button import Button
#from kivy.base import runTouchApp

class HCC(GridLayout):
    pass

class StartScreen(Screen):
    pass

class RootScreen(ScreenManager):
    pass

class GameSched(Widget):
    pass

#class CustomDropDown(DropDown):
#    pass
#
#dropdown = CustomDropDown()
#mainbutton = Button(text='Menu', size_hint=(None,None))
#mainbutton.bind(on_release=dropdown.open)
#dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))


class HCCApp(App):
    def build(self):
        self.title = 'Holy City Classic 2019'
        return HCC()

if __name__ == '__main__':
    HCCApp().run()