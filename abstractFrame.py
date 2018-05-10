from tkinter import ttk
import tkinter as tk

class Schema():
    def __init__(self, row, column, rows, columns):
        self._row = row
        self._column = column
        self._rows = rows
        self._columns = columns

class RubberSubFrame(tk.Frame):
    def __init__(self, master=None, width=40, height=20, bg="white",
                 schema=Schema(0, 0, 1, 1)):
        tk.Frame.__init__(self, master, width=width, height=height, bg=bg)
        self.master = master
        self._width = width
        self._height = height
        self._rows = schema._rows
        self._columns = schema._columns
        self.top = self.winfo_toplevel()
        self.top.geometry("")
        self.grid(sticky='wesn',
                  row=schema._row, column=schema._column,
                  rowspan=self._rows, columnspan=self._columns)
        for row in range(self._rows):
            self.rowconfigure(row, weight=self._rows)
            self.top.rowconfigure(row, weight=self._rows)
        for column in range(self._columns):
            self.columnconfigure(column, weight=self._columns)
            self.top.columnconfigure(column, weight=self._columns)


