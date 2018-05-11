from abstractFrame import *
from config import *
from readtle import CatalogTLE
from tkinter.filedialog import askopenfilename

import numpy as np

class MainWindow(RubberSubFrame):
    def __init__(self, master=None, width=MAINWIDTH, height=MAINHEIGHT, bg="black"):
        RubberSubFrame.__init__(self, master, width=width, height=height,
                                bg=bg, schema=Schema(0, 0, 3, 2))
        self.addMenu()
        self._panes = {}
        self.addPane(Schema(0, 3, 2, 1), bg=CONTROLCOLOR, name='control')
        self.addPane(Schema(2, 3, 1, 1), bg=BASECOLOR, name='log')
        self.addPane(Schema(0, 0, 3, 2), bg=BASECOLOR, name='plot')

    def addPane(self, schema, bg, name):
        width = self._width * schema._columns / self._columns
        height = self._height * schema._rows / self._rows
        pane = RubberSubFrame(self, width=width, height=height,
                              bg=bg, schema=schema)
        pane.configure(bd=1)
        self._panes[name] = pane
        return self

    def addMenu(self):
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Выбрать",
                command=self.open, accelerator="Ctrl + o")
        self.master.bind('<Control-Key-o>', self.open)
        self.menubar.add_separator()
        self.menubar.config(bg=BASECOLOR, fg=TEXTCOLOR)
        self.master.config(menu=self.menubar)
        return self

    def open(self, event='notByKey'):
        self.catalogfile = askopenfilename()
        self.master.title('%s %s' % (setting.PROJ, self.catalogfile))
        self.catalog = CatalogTLE()
        self.catalog.readFullTLE(self.catalogfile)
        # self._workArea.setCatalog(self.catalog)
        print("open")
        return 1

root = tk.Tk()
app = MainWindow(master=root)
app.mainloop()

