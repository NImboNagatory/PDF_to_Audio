from tkinter import Tk
from func import Screen

gui = Tk()

gui.title("")

gui.resizable(False, False)

gui.geometry("200x100")

screen = Screen(gui)

screen.grid()

loop_on = True

while loop_on:
    gui.update()
