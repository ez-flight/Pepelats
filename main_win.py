#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from tkinter import *

from drawsigma import *

global sat_name

def but_open_clicked():
    print("Hello World!")


def but_1_clicked():
    print("Hello World!")
    # прочесть поле со спутником!!!

    sat_name

    sat_name = Entry.get()

    openfile(sat_name)

    
def but_2_clicked():
    print("Hello World!")


def close():
    root.destroy()
    root.quit()


def main(): 

    root = Tk()
    root.title("Hello World!")
    root.geometry('400x60')
    # устанавливаем минимальный размер окна 
    # root.minsize(325,230)
    # выключаем возможность изменять окно
    # root.resizable(width=False, height=False)


    button_open = Button(root)
#    but_open['text'] = 'выбрать каталог'
#    but_open['command'] = but_open_clicked
    button_open.pack(fill=BOTH)
#    
#    print("first but")

#    text = Entry(root, font='Arial 14')
#    text.pack(fill=BOTH)

#    but_1 = Button(root)
#    but_1['text'] = 'Граф. Короткие интервалы'
#    but_1['command'] = but_1_clicked
#    but_1.pack(fill=BOTH)

#    but_2 = Button(root)
#    but_2['text'] = 'Граф. Длинные интервалы'
#    but_2['command'] = but_2_clicked
#    but_2.pack(fill=BOTH)

    root.protocol('WM_DELETE_WINDOW', close)

    # теперь окно будет отображено при запуске
    root.mainloop()


if __name__ == "__main__":
    main()


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

