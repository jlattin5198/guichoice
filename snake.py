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

        title = t.Label(upper, text="Snake - Use arrow keys")
        title.pack()

        s_btn = t.Button(upper_btn, text="Start")
        s_btn.pack(side="left")
        r_btn = t.Button(upper_btn, text="Retry", state="disabled")
        r_btn.pack(side="right")

        self.score = 0
        self.scr_lab = t.Label(upper_scr, text="Score: " + str(self.score))
        self.scr_lab.pack()

        self.gamewin = t.Canvas(lower, height="350", width="350", bg="white", borderwidth="7", relief="ridge")
        self.gamewin.pack()
        self.gamewin.focus_force()
        self.gamewin.bind("<Left>", self.slither)
        self.gamewin.bind("<Right>", self.slither)
        self.gamewin.bind("<Up>", self.slither)
        self.gamewin.bind("<Down>", self.slither)

        self.snake = self.gamewin.create_rectangle(172, 172, 192, 192, tags="hiss", fill="blue")

        self.dot = self.gamewin.create_rectangle(177, 177, 187, 187)

    def slither(self, event):
        dir = str(event.keysym)
        dx = 0
        dy = 0
        if dir == "Left":
            dx = -20
        elif dir == "Right":
            dx = 20
        elif dir == "Up":
            dy = -20
        else:
            dy = 20
        self.gamewin.move(self.snake, dx, dy)


main()
