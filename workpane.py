import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as mpl

from calcsigma import *
from config import *

class Work(tk.Frame):
    def __init__(self, master, catalogtle):
        tk.Frame.__init__(self, master, width=MAINWIDTH,
                          height=MAINHEIGHT, bg=BASECOLOR, bd=1,
                          relief=tk.FLAT)
        self._master = master
        self.ephemeris = ephemerisNames[0]
        self.catalog = catalogtle
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
        self._scalePeriod['from_'] = 0
        self._scalePeriod['to'] = len(self.catalog.name) - 1
        return self

    def _placeControlPane(self):
        self._control = tk.Frame(self, width=400, height=320, bd=1,
                                relief=tk.FLAT, bg=BASECOLOR)
        self._control.grid(row=0, column=2, sticky="wesn")
        self._makePeriodTypeFrame()
        self._makeParametersFrame()
        self._makeScalePeriod()
        return self

    def _makeButtons(self):
        self._processButton = tk.Button(self._control)
        self._processButton["text"] = "Очистить"
        self._processButton["bg"] = ITEMCOLOR
        self._processButton["fg"] = TEXTCOLOR
        self._processButton["command"] = self._clear_plot
        self._processButton.grid(column=0, row=2, sticky='we')
        return self

    def _makePeriodTypeFrame(self):
        self._periodArea = tk.Frame(self._control, width=400, height=20,
                relief=tk.FLAT)
        self._periodArea.grid(row=0, column=0, sticky='we')
        self._periodType = tk.IntVar()
        self._periodTypeButton = tk.Radiobutton(self._periodArea,
                bg=BASECOLOR, fg=TEXTCOLOR, indicatoron=1, height=3,
                activebackground=HIGHLIGHTCOLOR, takefocus="on",
                text="Короткие интервалы", variable=self._periodType,
                command=self._isToggledShort, value=0)
        self._periodTypeButton.grid(row=0, column=0, sticky='we')
        self._periodTypeButton.select()
        self._periodTypeButton= tk.Radiobutton(self._periodArea,
                bg=BASECOLOR, fg=TEXTCOLOR, indicatoron=1, height=3,
                activebackground=HIGHLIGHTCOLOR,
                text="Длинные интервалы", variable=self._periodType,
                command=self._isToggledLong, value=1)
        self._periodTypeButton.grid(row=0, column=1, sticky='we')
        return self

    def _makeParametersFrame(self):
        self.parametersArea = tk.Frame(self._control, width=400,
                height=50, relief=tk.FLAT, bg=BASECOLOR)
        self.parametersArea.grid(row=1, column=0, columnspan=2, sticky='we')
        self._makeEphemerisBox()
        self._makeButtons()
        return self

    def _isToggledShort(self):
        self._periodType = 0
        self._clear_plot()
        self._scalePeriod.grid_forget()
        return self

    def _isToggledLong(self):
        self._periodType = 1
        self._clear_plot()
        self._placeScalePeriod()
        return self

    def _makeEphemerisBox(self):
        self.ephemerisBox = ttk.Combobox(self.parametersArea, values=ephemerisNames,
                state='readonly', textvariable=self.ephemeris)
        self.ephemerisBox.current(0)
        self.ephemerisBox.configure(width=40, height=80)
        self.ephemerisBox.bind('<<ComboboxSelected>>', self._plot_of_ephemeris)
        self.ephemerisBox.grid(row=0,column=0, sticky='we')
        return self

    def _placeScalePeriod(self):
        self._scalePeriod.grid(row=1, column=0, sticky='we')
        return self

    def _makeScalePeriod(self):
        self._scalePeriod = tk.Scale(self.parametersArea,
                orient= tk.HORIZONTAL,length=250,from_=0,to=1,tickinterval=10,
                resolution=1, bg=BASECOLOR)
        self._scalePeriod.bind('<ButtonRelease-1>', self._plot_of_ephemeris)
        return self


    def _placePlots(self):
        self._plots = tk.Frame(self, width=400, height=320, bd=1, relief=tk.FLAT, bg=ITEMCOLOR)
        self._plots.grid(row=0, column=0, columnspan=2, sticky="wesn")
        self._makeFigure()
        return self

    def _makeFigure(self):
        self.fig.patch.set_facecolor(BASECOLOR)
        self.ax.set_facecolor(SHADOWCOLOR)
        with mpl.style.context('./presentation.mplstyle'):
            self.ax.grid(True)
        self.canvas = FigureCanvasTkAgg(self.fig, self._plots)
        self.canvas.get_tk_widget().pack(side="top", fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self._plots)
        self.toolbar["background"] = BASECOLOR
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.canvas.show()
        return self

    def _clear_plot(self):
        with mpl.style.context('./presentation.mplstyle'):
            self.ax.clear()
            self.ax.grid(True)
            self.fig.canvas.draw()
        return self

    def _plot_of_ephemeris(self, event):
        title = ''
        with mpl.style.context('./presentation.mplstyle'):
            if self._periodType == 0:
                self.ax.plot(calcShort_ephem(self.catalog, self.ephemerisBox.get()))
                title = 'Короткие интервалы'
            elif self._periodType == 1:
                self.ax.plot(calcLong_ephem(self.catalog,
                    self.ephemerisBox.get(), self._scalePeriod.get()))
                title = 'Длинные интервалы'
            self.ax.set_xlabel(r'Epoch')
            self.ax.set_ylabel(r'%s' % self.ephemerisBox.get())
            self.ax.set_title(title)
            self.ax.grid(True, color='white', linewidth=2, alpha=0.3)
            self.fig.canvas.draw()
        return self

