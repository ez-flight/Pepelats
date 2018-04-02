import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from math import *
import numpy as np

MAINWIDTH=640
MAINHEIGHT=402
ITEMWIDTH=80
ITEMHEIGHT=32
BASECOLOR="#c0c0c0"
ITEMCOLOR="#d3d3d3"
SHADOWCOLOR="#a9a9a9"
BORDERCOLOR="#808080"
HIGHLIGHTCOLOR="#5F9EA0"
TEXTCOLOR="#484848"

class MainWindow(tk.Frame):
    '''
    в главном окне две области: меню и рабочая область
    '''
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg="orange")
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self._placeMenu()
        self._placeWorkarea()
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.rowconfigure(1, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def _placeMenu(self):
        self._menu = Menu(self.master)
        self._menu.grid(row=0, columnspan=8, sticky=tk.N + tk.E + tk.W)
        self._menu.rowconfigure(0, weight=0)
        self._menu.columnconfigure(1, weight=1)
        return self

    def _placeWorkarea(self):
        self._workArea = Work(self.master)
        self._workArea.grid(row=1, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W)
        self._workArea.rowconfigure(0, weight=1)
        self._workArea.columnconfigure(0, weight=1)
        return self

class Work(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=MAINWIDTH,
                          height=MAINHEIGHT, bg=BASECOLOR, bd=1,
                          relief=tk.FLAT)
        self._master = master
        self._placeControlPane()
        self._placePlots()
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)

    def _placeControlPane(self):
        self._control= tk.Frame(self, width=400, height=320, bd=1,
                                relief=tk.FLAT, bg=SHADOWCOLOR)
        self._control.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        return self

    def _placePlots(self):
        self._plots = tk.Frame(self, width=400, height=320, bd=1, relief=tk.FLAT, bg=HIGHLIGHTCOLOR)
        self._plots.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        return self


class Menu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=MAINWIDTH,
                          height=ITEMHEIGHT + 5, bg=BASECOLOR, bd=1,
                          relief=tk.SUNKEN)
        self._master = master
        self._openImage = tk.PhotoImage(file="./icons/folder.png")
        self._placeOpen()

    def _placeOpen(self):
        self._open= tk.Button(self, text="Открыть",
                              command=self.open, relief=tk.GROOVE)
        self._open.grid(row=0, column=0, sticky=tk.N + tk.W)
        self._open.config(image=self._openImage, bg=ITEMCOLOR,
                          width=ITEMWIDTH, height=ITEMHEIGHT, bd=1)
        self._open.image = self._openImage
        return self

    def open(self):
        print("open")
        return self

    def __del__(self):
        del self._open
        del self

    # def _placeFrames(self):
        # self._plotsArea = tk.Frame(self.master, bd=1, relief=tk.FLAT)
        # self._plotsArea.grid(row=1, rowspan=2, columnspan=2)

        # self._toolbar = tk.Frame(self.master, bd=1, relief=tk.FLAT)
        # self._toolbar.grid(row=0, columnspan=4)

        # self._topleft = tk.Frame(self._plotsArea, bd=1, relief=tk.FLAT)
        # self._topright = tk.Frame(self._plotsArea, bd=1, relief=tk.FLAT)
        # self._bottomleft = tk.Frame(self._plotsArea, bd=1, relief=tk.FLAT)
        # self._bottomright = tk.Frame(self._plotsArea, bd=1, relief=tk.FLAT)
        # self._topleft.grid(row=0, column=0)
        # self._topright.grid(row=0, column=1)
        # self._bottomleft.grid(row=1, column=0)
        # self._bottomright.grid(row=1, column=1)

        # return self

    # def _placePlot(self, placer):
        # fig = Figure(figsize=(6,4), dpi=100)
        # ax = fig.add_subplot(111)
        # canvas = FigureCanvasTkAgg(fig, placer)
        # canvas.get_tk_widget().pack(side="top")
        # canvas.show()
        # return self

    # def _placeEmptyPlots(self):
        # self._placePlot(self._topleft)
        # self._placePlot(self._topright)
        # self._placePlot(self._bottomleft)
        # self._placePlot(self._bottomright)
        # return self

    # def _placeButtons(self):
        # self._config = tk.Button(self._toolbar, text="Настройка", command=self.setConfig)
        # self._show = tk.Button(self._toolbar, text="Вывести на графики", command=self.setPlots)
        # self._save = tk.Button(self._toolbar, text="Сохранить графики", command=self.savePlots)
        # self._quit = tk.Button(self._toolbar, text="Выход", fg="red", command=root.destroy)

        # self._config.grid(row=0, column=0)
        # self._show.grid(row=0, column=1)
        # self._save.grid(row=0, column=2)
        # self._quit.grid(row=0, column=3)
        # return self

    # def setConfig(self):
        # self._config["bg"] = "green"
        # self._config["fg"] = "white"
        # return self

    # def setPlots(self):
        # self._show["bg"] = "orange"
        # return self

    # def savePlots(self):
        # self._save["bg"] = "blue"
        # self._save["fg"] = "white"
        # return self

    # # def __del__(self):
        # # del self._bottomleft
        # # del self._bottomright
        # # del self._topleft
        # # del self._topright
        # # del self._save
        # # del self._show
        # # del self._config
        # # del self._quit
        # # del self._plotsArea
        # # del self._toolbar

root = tk.Tk()
app = MainWindow(master=root)
app.mainloop()
