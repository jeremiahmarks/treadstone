#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Jeremiah Marks
# @Date:   2015-09-28 19:34:35
# @Last Modified 2015-10-01
# @Last Modified time: 2015-10-01 20:58:15

#Since I did not push my changes from work, this is going to be some of the functions that
# need to be implemented.

# Gui stuff is what is needed most.

# Working mostly from this place
# https://github.com/daleathan/thinkingintkinter

from Tkinter import *

class ImportDisplay:
    def __init__(self, parent):
        button_width = 6

        button_padx = "2m"    ### (2)
        button_pady = "1m"    ### (2)

        buttons_frame_padx =  "3m"   ### (3)
        buttons_frame_pady =  "2m"   ### (3)
        buttons_frame_ipadx = "3m"   ### (3)
        buttons_frame_ipady = "1m"   ### (3)
        # -------------- end constants ----------------

        self.myParent = parent
        self.csvFunctionsLabel = Label(parent,  text = "Hello There!")
        self.csvFunctionsLabel.grid(
            row = 0, column = 0
            )
        self.csvFunctionsOptionFrame = Frame(parent)
        self.csvFunctionsOptionFrame.grid( row = 0, column = 1, rowspan = 6)
        self.firstOptionButton = Button(self.csvFunctionsOptionFrame, text = "Apples.", command=lambda: self.pairing("baddle"))
        self.firstOptionButton.grid(sticky = N)
        self.buttons_frame = Frame(parent)

        self.buttons_frame.grid(    ### (4)
            ipadx=buttons_frame_ipadx,  ### (3)
            ipady=buttons_frame_ipady,  ### (3)
            padx=buttons_frame_padx,    ### (3)
            pady=buttons_frame_pady,    ### (3)
            )


        self.button1 = Button(self.buttons_frame, command=self.button1Click)
        self.button1.configure(text="OK", background= "green")
        self.button1.focus_force()
        self.button1.configure(
            width=button_width,  ### (1)
            padx=button_padx,    ### (2)
            pady=button_pady     ### (2)
            )

        self.button1.grid(sticky=E)
        self.button1.bind("<Return>", self.button1Click_a)

        self.button2 = Button(self.buttons_frame, command=self.button2Click)
        self.button2.configure(text="Cancel", background="red")
        self.button2.configure(
            width=button_width,  ### (1)
            padx=button_padx,    ### (2)
            pady=button_pady     ### (2)
            )

        self.button2.grid(sticky=E)
        self.button2.bind("<Return>", self.button2Click_a)

    def button1Click(self):
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
        else:
            self.button1["background"] = "green"
    def pairing(self, something = "Apples"):
        print "Hello " + str(something)

    def button2Click(self):
        self.myParent.destroy()

    def button1Click_a(self, event):
        self.button1Click()

    def button2Click_a(self, event):
        self.button2Click()

def hello():
    print "hello!"

root = Tk()
menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="split csv to 10Mb", command=hello)
filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

myapp = ImportDisplay(root)
root.mainloop()
