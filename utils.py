from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import Clock, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.label import CoreLabel
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp  
from math import ceil
from requestAPI import *

import os
import pickle


class ImageButton(ButtonBehavior, AsyncImage):
    pass