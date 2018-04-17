#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from imp import reload
from tkinter import ttk
import tkinter as tk
from math import *
import numpy as np

from readtle import CatalogTLE
from config import *
import config as setting
import workpane
reload(workpane)
from workpane import *

class MainWindow(tk.Frame):
    '''
    в главном окне две области: меню и рабочая область
    '''
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg="orange")
        self._master = master
        self._master.title(PROJ)
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.ephemerisToDraw = {}
        self.addMenu()
        self._placeWorkarea(CatalogTLE())
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.winfo_toplevel().geometry("")

    def addMenu(self):
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Выбрать каталог",
                command=self.open, accelerator="Ctrl + o")
        self._master.bind('<Control-Key-o>', self.open)
        self.menubar.add_separator()
        self.addExtrapolationSubmenu()
        self.menubar.config(**setting.standard)
        self.master.config(menu=self.menubar)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        return self

    def addExtrapolationSubmenu(self):
        self.extrapolation = tk.Menu(self.menubar, tearoff=1)
        self.extrapolation.config(**setting.standard)
        self.extrapolation.add_command(label='Эфемериды')
        self.extrapolation.add_separator()
        for name in setting.ephemerisNames:
            self.ephemerisToDraw[name] = tk.BooleanVar()
            self.extrapolation.add_checkbutton(label=name,
                    variable=self.ephemerisToDraw[name],
                    command=self.setEphemeris)
        self.extrapolation.add_command(label='Элементы орбиты', command=self.setOrbital)
        self.menubar.add_cascade(label='Экстраполяция',
                menu=self.extrapolation)
        self.extrapolation.config(tearoffcommand=self.hideExtrapolation)
        return self

    def hideExtrapolation(self):
        self.extrapolation.config(tearoff=1)
        return self

    def setEphemeris(self):
        for name in self.ephemerisToDraw:
            if ( self.ephemerisToDraw[name].get() ):
                print(name, self.ephemerisToDraw[name].get())
        return self

    def setOrbital(self):
        return self

    def open(self, event="notByKey"):
        self.catalogfile = tk.filedialog.askopenfilename()
        self._master.title('%s %s' % (setting.PROJ, self.catalogfile))
        self.catalog = CatalogTLE()
        self.catalog.readFullTLE(self.catalogfile)
        self._workArea.setCatalog(self.catalog)
        return self

    def _placeWorkarea(self, catalogtle):
        self._workArea = Work(self.master, catalogtle)
        self._workArea.rowconfigure(0, weight=1)
        self._workArea.columnconfigure(0, weight=1)
        return self

root = tk.Tk()
app = MainWindow(master=root)
app.mainloop()
