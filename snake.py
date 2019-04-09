import tkinter as t
import time
import random as r

def main():
    root = t.Tk()
    sgame = Game(root)
    root.mainloop()
class Game:
    def __init__(self, parent):
        upper = t.Frame(parent)
        upper_btn = t.Frame(parent)
        upper_scr = t.Frame(parent)
        lower = t.Frame(parent)
        upper.pack()
        upper_btn.pack()
        upper_scr.pack()
        lower.pack()

        title = t.Label(upper, text="Snake")
        title.pack()

        


main()
