from abstractFrame import *
from loghandler import *
from config import *
from readtle import CatalogTLE
from tkinter.filedialog import askopenfilename

import numpy as np
import logging
import logging.config

class MainWindow(RubberSubFrame):
    def __init__(self, master=None, width=MAINWIDTH, height=MAINHEIGHT, bg="black"):
        RubberSubFrame.__init__(self, master, width=width, height=height,
                                bg=bg, schema=Schema(0, 0, 3, 2))
        self._panes = {}
        self.logtext = tk.StringVar()
        self.addMenu()
        self.addPane(Schema(0, 3, 2, 1), bg=CONTROLCOLOR, name='control')
        self.addPane(Schema(2, 3, 1, 1), bg=CONTROLCOLOR, name='log')
        self.addPane(Schema(0, 0, 3, 2), bg=BASECOLOR, name='plot')
        self.makeLoggerView()

    def makeLoggerView(self):
        # logrec = logging.LogRecord('__main__.readtle', logging.INFO,
                                   # './readtle.py', 40,
                                   # self.logtext, '', None)
        # ch.emit(logrec)
        self.LoggerView = tk.Message(self._panes['log'], bg=DARKCOLOR,
                                     fg=LOGTEXTCOLOR,
                                     justify=tk.LEFT,
                                     width=self._width / 3,
                                     textvariable=self.logtext)
        self.LoggerView.grid(row=0, column=0, sticky='wesn', padx=5, pady=5)
        return self

    def addPane(self, schema, bg, name):
        width = self._width * schema._columns / self._columns
        height = self._height * schema._rows / self._rows
        pane = RubberSubFrame(self, width=width, height=height,
                              bg=bg, schema=schema)
        pane.configure(bd=1)
        self._panes[name] = pane
        # self.logtext.set(self.logtext.get() + '\n' +  name)
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
        self.master.title('%s %s' % (PROJ, self.catalogfile))
        self.catalog = CatalogTLE()
        self.catalog.readFullTLE(self.catalogfile)
        # self._workArea.setCatalog(self.catalog)
        return 1


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(master=root)
    app.mainloop()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    texthandler = LogMessage(app.LoggerView)
    logger.addHandler(texthandler)
    # logger.info('start')

