#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from imp import reload
from tkinter import ttk
import tkinter as tk
from math import *
import numpy as np

from readtle import CatalogTLE
from config import *
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
        self.addMenu()
        self._placeWorkarea(CatalogTLE())
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.winfo_toplevel().geometry("")

    def addMenu(self):
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Выбрать каталог", command=self.open)
        self.menubar.add_separator()
        self.menubar.config(bg=BASECOLOR, fg=TEXTCOLOR, activeborderwidth=3)
        self.master.config(menu=self.menubar)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        return self

    def open(self):
        self.catalogfile = tk.filedialog.askopenfilename()
        self._master.title('%s %s' % (PROJ, self.catalogfile))
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
