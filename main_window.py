#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from tkinter import *

from tkinter.filedialog import * 

from readtle import CatalogTLE

from drawsigma import draw1
from drawsigma import draw2


global catalog

global sat_name


def btnopen_clicked():
    # диалоговое окно открытия файла
    global catalog
    global sat_name
    
    file_open = askopenfilename()

    sat_name = entry_sat.get()

    catalog = CatalogTLE()
    
    catalog.ReadFullTLE(file_open)


def btn1_clicked():
    # корткие интервалы!
    global catalog
    draw1(catalog)

    
def btn2_clicked():
    # длинные интервалы
    global catalog
    draw2(catalog)


def close():
    root.destroy()
    root.quit()


root = Tk()
root.title("Sattelarium!")
#root.geometry('400x200')
# выключаем возможность изменять окно
root.resizable(width=False, height=False)


label1 = Label(root, text="Sattelarium ver 0.1", font=20, fg="blue")

textbox = Text(root, font='Arial 14', wrap='word', width=25, height=10)


btnopen = Button(root)
btnopen['text'] = 'выбрать каталог'
btnopen['command'] = btnopen_clicked

entry_sat = Entry()
entry_sat.place(relx=.5, rely=.1, anchor="c")

btn1 = Button(root)
btn1['text'] = 'Граф. Короткие интервалы'
btn1['command'] = btn1_clicked

btn2 = Button(root)
btn2['text'] = 'Граф. Длинные интервалы'
btn2['command'] = btn2_clicked

## первый вариант расположения
#label1.pack()
#btnopen.pack(fill='both')
#entry_sat.pack()
#btn1.pack()
#btn2.pack()

## второй вариант расопложения
label1.grid(row=0, column=0, columnspan=2)
textbox.grid(row=1, column=0, rowspan=4)
btnopen.grid(row=1, column=1)
entry_sat.grid(row=2, column=1)
btn1.grid(row=3, column=1)
btn2.grid(row=4, column=1)


root.protocol('WM_DELETE_WINDOW', close)

root.mainloop()



# ========================  та супер--утилитка: ===============================
#
# quickly create ubuntu-application foo
# quickly edit
# quickly design
# quickly run
# quickly add help-guide <имя руководства>
# quickly add dialog <имя диалога>
#
# Где подключать сигналы к функциям.
#
# def on_button1_clicked(self, widget, data=None):
#    //Тут ваш код
#
# Как обращаться к виджетам из python кода.
# self.builder.get_object("object_name")
# self.builder.get_object("text").set_text("Text") 
# Или
# text = self.builder.get_object("text")
# text.set_text("Text")

