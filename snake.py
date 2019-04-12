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

        title = t.Label(upper, text="Snake - Use arrow keys or WASD")
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
        self.gamewin.bind("w", self.slither)
        self.gamewin.bind("a", self.slither)
        self.gamewin.bind("s", self.slither)
        self.gamewin.bind("d", self.slither)

        self.snake = self.gamewin.create_rectangle(172, 172, 192, 192, tags="hiss", fill="blue")

        self.dot = self.gamewin.create_rectangle(177, 177, 187, 187, fill="red")
        self.bb = self.gamewin.bbox(self.dot)

    def slither(self, event):
        dir = str(event.keysym)
        dx = 0
        dy = 0
        if dir == "Left" or "a":
            dx = -20
        elif dir == "Right" or "d":
            dx = 20
        elif dir == "Up" or "w":
            dy = -20
        elif dir == "Down" or "s":
            dy = 20
        self.gamewin.move(self.snake, dx, dy)
        if self.gamewin.find_overlapping(self.bb[0], self.bb[1], self.bb[2], self.bb[3]) == (1, 2):
            self.scatter()
            self.score = self.score + 1
            self.scr_lab["text"] = "Score: " + str(self.score)

    def scatter(self):
        loc = self.gamewin.coords(self.dot)
        newx = r.randint(10, 340)
        newy = r.randint(10, 340)
        self.gamewin.move(self.dot)
        print(self.gamewin.coords(self.dot))

main()
