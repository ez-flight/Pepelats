from tkinter import ttk
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as mpl
from math import *
import numpy as np

from readtle import CatalogTLE
from processingCenter import *

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
        self.addMenu()
        self._placeWorkarea()
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
        print("open")
        self.catalogfile = tk.filedialog.askopenfilename()
        self.catalog = CatalogTLE()
        self.catalog.ReadFullTLE(self.catalogfile)
        self._workArea.setCatalog(self.catalog)
        return self

    def _placeWorkarea(self):
        self._workArea = Work(self.master)
        self._workArea.rowconfigure(0, weight=1)
        self._workArea.columnconfigure(0, weight=1)
        return self
parameters = ['sin', 'cos', '2 cos', '2 sin']
signalos = {'sin': np.sin, 'cos': np.cos, '2 cos': lambda x: 2 * np.cos(x), '2 sin': lambda x: 2 * np.sin(x)}

class Work(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=MAINWIDTH,
                          height=MAINHEIGHT, bg=BASECOLOR, bd=1,
                          relief=tk.FLAT)
        self._master = master
        self.parameter = 'sin'
        self.catalog = CatalogTLE()
        self.fig = Figure(figsize=(6,4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self._placeControlPane()
        self._placePlots()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, columnspan=3, sticky="wesn")
        self.winfo_toplevel().geometry("")

    def setCatalog(self, catalog):
        self.catalog = catalog
        return self

    def _placeControlPane(self):
        self._control= tk.Frame(self, width=400, height=320, bd=1,
                                relief=tk.FLAT, bg=BASECOLOR)
        self._control.grid(row=0, column=2, sticky="wesn")
        self._makeButtons()
        self._makeCombobox()
        return self

    def _makeButtons(self):
        self._processButton = tk.Button(self._control)
        self._processButton["text"] = "Сделай график"
        self._processButton["bg"] = ITEMCOLOR
        self._processButton["fg"] = TEXTCOLOR
        self._processButton["command"] = self.showProcessingResults
        self._processButton.grid(column=0, row=0, sticky='w')
        return self

    def _makeCombobox(self):
        self.combobox = ttk.Combobox(self._control, values=parameters,
                state='readonly', textvariable=self.parameter)
        self.combobox.current(0)
        self.combobox.bind('<<ComboboxSelected>>', self._plot_of_parameter)
        self.combobox.grid(row=1, sticky='w')
        return self


    def _placePlots(self):
        self._plots = tk.Frame(self, width=400, height=320, bd=1,
                               relief=tk.FLAT, bg=ITEMCOLOR)
        self._plots.grid(row=0, column=0, columnspan=2, sticky="wesn")
        self._makeFigure()
        return self

    def _makeFigure(self):
        self.fig.patch.set_facecolor(BASECOLOR)
        self.ax.set_facecolor(SHADOWCOLOR)
        self.canvas = FigureCanvasTkAgg(self.fig, self._plots)
        self.canvas.get_tk_widget().pack(side="top", fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self._plots)
        self.toolbar["background"] = BASECOLOR
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.canvas.show()
        return self

    def showProcessingResults(self):
        self.ax.clear()
        self.ax.grid(True)
        processedCatalog = ProcessingCatalog(self.catalog)
        with mpl.style.context('./presentation.mplstyle'):
            # self.ax.plot(np.random.normal(0, 1, 100))
            self.ax.plot(processedCatalog.extrapolateShort())
            self.fig.canvas.draw()
            self.ax.set_xlabel('Epoсh')
            self.ax.set_ylabel(r'$\sigma R$')
            self.ax.set_title(self.catalog.name[1])
        return self

    def _plot_of_parameter(self, event):
        self.ax.clear()
        self.ax.grid(True, color='white', linewidth=2, which='both', alpha=0.3)
        with mpl.style.context('./presentation.mplstyle'):
            f = 1000
            t = np.arange(0, 0.001, 1/100e3)
            self.ax.plot(np.random.normal(0, 0.1, 100) + signalos[self.combobox.get()](2 * pi * f * t))
            self.fig.canvas.draw()
            self.ax.set_xlabel(r'$\xi$')
            self.ax.set_ylabel(r'$%s\left(\xi\right)$' % self.combobox.get())
            self.ax.set_title('Signal with normal distributed noise')
            self.fig.canvas.draw()
        return self


root = tk.Tk()
app = MainWindow(master=root)
app.mainloop()
