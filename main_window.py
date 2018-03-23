#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from tkinter import *

from tkinter.filedialog import * 

from readtle import CatalogTLE

from drawsigma import DrawShort_R
from drawsigma import DrawLong_R
from drawsigma import DrawLong_3

global catalog

global sat_name


def btn_open_clicked():
    # диалоговое окно открытия файла
    global catalog
    global sat_name
    
    file_open = askopenfilename()

    catalog = CatalogTLE()
    
    catalog.ReadFullTLE(file_open)
    
    label_sat1['text'] = catalog.name[1]
    label_sat2['text'] = 'элеметов: ', len(catalog.name)
    label_sat3['text'] = 'период:', catalog.JD[-1] - catalog.JD[1]


def btnShort_R_clicked():           # короткие интервалы!
    global catalog
    DrawShort_R(catalog)

def btnShort_3_clicked():
    '''
    '''

def btnShort_a_clicked():
    '''
    '''        
    
def btnLong_R_clicked():            # длинные интервалы
    global catalog
    DrawLong_R(catalog)


def btnLong_3_clicked():
    global catalog
    DrawLong_3(catalog)
    '''
    '''

def btnLong_a_clicked():
    '''
    '''

def close():
    root.destroy()
    root.quit()


root = Tk()
root.title("Sattelarium!")
#root.geometry('400x200')
# выключаем возможность изменять окно
root.resizable(width=False, height=False)


label_main = Label(root, text="Sattelarium ver 0.1", font='GentiumAlt 24', fg="blue")

textbox = Text(root, font='Arial 12', wrap='word', width=25, height=10)

label_sat1 = Label(root, text=" -- ", font='arial 10')
label_sat2 = Label(root, text=" -- ", font='arial 10')
label_sat3 = Label(root, text=" -- ", font='arial 10')

btn_open = Button(root)
btn_open['text'] = 'выбрать каталог'
btn_open['command'] = btn_open_clicked

labelShort = Label(root, text="Короткие интервалы", font='arial 12')

btnShort_R = Button(root)
btnShort_R['text'] = 'Граф. (R)'
btnShort_R['command'] = btnShort_R_clicked

btnShort_3 = Button(root)
btnShort_3['text'] = 'Граф.  (3)'
btnShort_3['command'] = btnShort_3_clicked

btnShort_a = Button(root)
btnShort_a['text'] = 'Граф.  (A)'
btnShort_a['command'] = btnShort_a_clicked

labelLong = Label(root, text="Длинные интервалы", font='arial 12')

btnLong_R = Button(root)
btnLong_R['text'] = 'Граф. (R)'
btnLong_R['command'] = btnLong_R_clicked

btnLong_3 = Button(root)
btnLong_3['text'] = 'Граф. (3)'
btnLong_3['command'] = btnLong_3_clicked

btnLong_a = Button(root)
btnLong_a['text'] = 'Граф. (A)'
btnLong_a['command'] = btnLong_a_clicked


##                  РАСПОЛОЖЕНИЕ
label_main.grid(row=0,          column=0, columnspan=4)

textbox.grid(row=1,         column=0, rowspan=4)

label_sat1.grid(row=1,       column=1)
label_sat2.grid(row=2,       column=1)
label_sat3.grid(row=3,       column=1)
btn_open.grid(row=4,         column=1)

labelShort.grid(row=1,      column=2)
btnShort_R.grid(row=2,      column=2)
btnShort_3.grid(row=3,      column=2)
btnShort_a.grid(row=4,      column=2)

labelLong.grid(row=1,       column=3)
btnLong_R.grid(row=2,       column=3)
btnLong_3.grid(row=3,       column=3)
btnLong_a.grid(row=4,       column=3)


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

