#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from math import *
import numpy as np

BASECOLOR="#c0c0c0"
ITEMCOLOR="#d3d3d3"
SHADOWCOLOR="#a9a9a9"
BORDERCOLOR="#808080"
HIGHLIGHTCOLOR="#5F9EA0"
TEXTCOLOR="#484848"

class MainWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=640, height=330,
                          bg=BASECOLOR)
        self.master = master
        self.addMenu()
        self.addArea()
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.winfo_toplevel().geometry("")

    def addMenu(self):
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Выбрать каталог", command=self.open)
        self.menubar.config(bg=BASECOLOR, fg=TEXTCOLOR)
        self.master.config(menu=self.menubar)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        return self

    def addArea(self):
        area = tk.Frame(self, width=500, height=200, bg=HIGHLIGHTCOLOR)
        area.grid(row=0, column=0, columnspan=3, sticky="wesn")
        area.rowconfigure(0, weight=1)
        area.columnconfigure(0, weight=1)
        area.columnconfigure(1, weight=4)
        subarea = tk.Frame(area, width=200, height=200, bg=TEXTCOLOR)
        subarea.grid(row=0, column=0, columnspan=2, sticky="wesn")
        subarea2 = tk.Frame(area, width=400, height=200, bg="green")
        subarea2.grid(row=0, column=2, sticky="wesn")
        return self

    def open(self):
        print('open')
        return self




root = tk.Tk()
app = MainWindow(master=root)
app.mainloop()
