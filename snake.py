import tkinter as t
import random as r
import time
import threading as thr


def main():
    root = t.Tk()
    sgame = Game(root)
    root.mainloop()


class Game:
    def __init__(self, parent):
        """creates snake window and components"""
        self.parent = parent

        upper = t.Frame(parent)
        upper_btn = t.Frame(parent)
        upper_scr = t.Frame(parent)
        lower = t.Frame(parent)
        lower_set = t.Frame(parent)
        upper.pack()
        upper_btn.pack()
        upper_scr.pack()
        lower.pack()
        lower_set.pack()

        self.title = t.Label(upper, text="Snake - Use wasd to control")
        self.title.pack()

        self.s_btn = t.Button(upper_btn, text="Start")
        self.s_btn.pack(side="left")
        self.s_btn.bind("<ButtonRelease-1>", self.start)
        self.r_btn = t.Button(upper_btn, text="Retry", state="disabled")
        self.r_btn.pack(side="right")
        self.r_btn.bind("<ButtonRelease-1>", self.retry)

        self.score = 0
        self.scr_lab = t.Label(upper_scr, text="Score: " + str(self.score))
        self.scr_lab.pack(fill="x")

        self.time_lab = t.Label(upper_scr, text="Time left: 0", state="disabled")
        self.time_lab.pack(fill="x")
        self.timed = False

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
        self.gamewin.bind("i", self.slither)
        self.gamewin.bind("j", self.slither)
        self.gamewin.bind("k", self.slither)
        self.gamewin.bind("l", self.slither)
        self.status = False

        self.snake = self.gamewin.create_rectangle(172, 172, 192, 192, tags="hiss", fill="blue")

        self.dot = self.gamewin.create_rectangle(177, 177, 187, 187, fill="red")
        self.pos = [12, 32, 52, 72, 92, 112, 132, 152, 172, 192, 212, 232, 252, 272, 292, 312, 332]
        self.scatter()

        self.ded = self.gamewin.create_text(182, 182, text="You died!", justify="center", font=("Arial", 30), state="hidden")

        self.cs_var = t.StringVar(parent)
        self.cs_var.set("color scheme")
        self.colorset = t.OptionMenu(lower_set, self.cs_var, "color scheme", "normal", "neon blue", "neon yellow", "grayscale", "sky", "ocean")
        self.colorset["highlightthickness"] = 0
        self.colorset.pack(side="left")

        self.kb_var = t.StringVar(parent)
        self.kb_var.set("key bindings")
        self.ctrlset = t.OptionMenu(lower_set, self.kb_var, "key bindings", "wasd", "arrow keys", "ijkl")
        self.ctrlset["highlightthickness"] = 0
        self.ctrlset.pack(side="left")

        self.gm_var = t.StringVar(parent)
        self.gm_var.set("game mode")
        self.gameset = t.OptionMenu(lower_set, self.gm_var, "game mode", "normal", "timed")
        self.gameset["highlightthickness"] = 0
        self.gameset.pack(side="left")

        self.apply = t.Button(lower_set, text="Apply")
        self.apply.pack(side="right", fill="y")
        self.apply.bind("<ButtonRelease-1>", self.settings)

        self.colorscheme = {
            "normal": ["SystemButtonFace", "white", "SystemButtonText", "SystemButtonFace", "blue", "red", "SystemWindowFrame", "SystemDisabledText"],
            "neon blue": ["black", "black", "deep sky blue", "gray15", "deep sky blue", "OrangeRed2", "deep sky blue", "white"],
            "neon yellow": ["black", "black", "yellow2", "gray15", "yellow2", "OrangeRed2", "yellow2", "white"],
            "grayscale": ["gray50", "gray60", "black", "gray30", "dark slate gray", "black", "dark slate gray", "gray60"],
            "sky": ["sky blue", "light sky blue", "yellow", "gray85", "gold", "snow", "snow", "gray70"],
            "ocean": ["medium blue", "blue", "lawn green", "dodger blue", "dark orange", "salmon", "dodger blue", "dark green"]
        }

        self.keybind = {
            "wasd": ["w", "a", "s", "d"],
            "arrow keys": ["Up", "Left", "Down", "Right"],
            "ijkl": ["i", "j", "k", "l"]
        }
        self.u = "w"
        self.l = "a"
        self.d = "s"
        self.r = "d"

    def slither(self, event):
        """moves the snake on user input"""
        if self.status:
            dir = str(event.keysym)
            dx = 0
            dy = 0
            if dir == self.l:
                dx = -20
            elif dir == self.r:
                dx = 20
            elif dir == self.u:
                dy = -20
            elif dir == self.d:
                dy = 20
            self.gamewin.move(self.snake, dx, dy)
            loc = self.gamewin.coords(self.snake)
            if self.gamewin.find_overlapping(loc[0], loc[1], loc[2], loc[3]) == (1, 2):
                self.scatter()
                self.score = self.score + 1
                self.scr_lab["text"] = "Score: " + str(self.score)
            if (loc[0] < 12 or loc[0] > 332) or (loc[1] < 12 or loc[1] > 332):
                self.status = False
                self.gamewin.itemconfig(self.ded, state="normal")

    def scatter(self):
        """randomizes location of the dot"""
        loc = self.gamewin.coords(self.dot)
        newx = self.pos[r.randint(0, 16)]
        newy = self.pos[r.randint(0, 16)]
        self.gamewin.move(self.dot, newx - (loc[0]) + 5, newy - (loc[1]) + 5)

    def start(self, event):
        """starts the game, only called once per window"""
        self.status = True
        self.s_btn["state"] = "disabled"
        self.r_btn["state"] = "normal"
        if self.timed:
            self.timedgame()

    def retry(self, event):
        """resets the game"""
        if not self.r_btn["state"] == "disabled":
            self.score = 0
            self.scr_lab["text"] = "Score: 0"
            loc = self.gamewin.coords(self.snake)
            self.gamewin.move(self.snake, 172 - loc[0], 172 - loc[1])
            self.scatter()
            self.status = True
            self.gamewin.itemconfig(self.ded, state="hidden")
            if self.timed:
                self.timedgame()

    def colorize(self, opt):
        """changes game window color scheme"""
        if not opt == "color scheme":
            self.parent["bg"] = self.colorscheme[opt][0]
            self.title["bg"] = self.colorscheme[opt][0]
            self.title["foreground"] = self.colorscheme[opt][2]
            self.s_btn["bg"] = self.colorscheme[opt][3]
            self.s_btn["activebackground"] = self.colorscheme[opt][3]
            self.s_btn["foreground"] = self.colorscheme[opt][2]
            self.s_btn["disabledforeground"] = self.colorscheme[opt][7]
            self.r_btn["bg"] = self.colorscheme[opt][3]
            self.r_btn["activebackground"] = self.colorscheme[opt][3]
            self.r_btn["foreground"] = self.colorscheme[opt][2]
            self.r_btn["disabledforeground"] = self.colorscheme[opt][7]
            self.scr_lab["bg"] = self.colorscheme[opt][0]
            self.scr_lab["foreground"] = self.colorscheme[opt][2]
            self.time_lab["bg"] = self.colorscheme[opt][0]
            self.time_lab["foreground"] = self.colorscheme[opt][2]
            self.time_lab["disabledforeground"] = self.colorscheme[opt][7]
            self.colorset["bg"] = self.colorscheme[opt][3]
            self.colorset["activebackground"] = self.colorscheme[opt][3]
            self.colorset["fg"] = self.colorscheme[opt][2]
            self.colorset["activeforeground"] = self.colorscheme[opt][2]
            self.ctrlset["bg"] = self.colorscheme[opt][3]
            self.ctrlset["activebackground"] = self.colorscheme[opt][3]
            self.ctrlset["fg"] = self.colorscheme[opt][2]
            self.ctrlset["activeforeground"] = self.colorscheme[opt][2]
            self.gameset["bg"] = self.colorscheme[opt][3]
            self.gameset["activebackground"] = self.colorscheme[opt][3]
            self.gameset["fg"] = self.colorscheme[opt][2]
            self.gameset["activeforeground"] = self.colorscheme[opt][2]
            self.apply["bg"] = self.colorscheme[opt][3]
            self.apply["activebackground"] = self.colorscheme[opt][3]
            self.apply["foreground"] = self.colorscheme[opt][2]
            self.gamewin["bg"] = self.colorscheme[opt][1]
            self.gamewin["highlightcolor"] = self.colorscheme[opt][6]
            self.gamewin.itemconfig(self.snake, fill=self.colorscheme[opt][4])
            self.gamewin.itemconfig(self.dot, fill=self.colorscheme[opt][5])
            self.gamewin.itemconfig(self.ded, fill=self.colorscheme[opt][2])

    def rebind(self, opt):
        """changes movement key bindings"""
        if not opt == "key bindings":
            self.u = self.keybind[opt][0]
            self.l = self.keybind[opt][1]
            self.d = self.keybind[opt][2]
            self.r = self.keybind[opt][3]
            self.title["text"] = "Snake - Use " + opt + " to control"

    def modeswap(self):
        """changes the game mode"""
        if not self.timed:
            self.timed = True
        else:
            self.timed = False
        self.time_lab["state"] = "normal"


    def settings(self, event):
        """changes all settings"""
        self.colorize(self.cs_var.get())
        self.rebind(self.kb_var.get())
        self.modeswap()

    def timedgame(self):
        """executes a 30-second timed game of snake"""
        tim = 30
        while tim > 0:
            time.sleep(1)
            tim -= 1
            self.time_lab["text"] = "Time left: " + str(tim)
        self.gamewin.itemconfig(self.ded, state="normal")
        self.status = False


main()
