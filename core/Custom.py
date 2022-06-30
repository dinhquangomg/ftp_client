import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

#Custom button class for whipFTP, Copyrights Vishnu Shankar B,

class FLabel(ttk.Label):
    def __init__(self, parent, name, icon, path, command, command2=None):
        #Save reference to path and function
        self.path = path
        self.path_function = command
        self.select_bool = False
        #Create the label
        super().__init__(parent, text = name, image = icon, compound = 'left')
        super().pack(side = 'top', pady = 3, padx = 3, fill = tk.X)
        #Bind events
        super().bind('<Button-1>', lambda name : command(path))
        super().bind('<Button-3>', lambda name : command2(path))
        # super().bind('<Enter>', self.hover)
        # super().bind('<Leave>', self.leave)

    def select(self, event):
        if not self.select_bool:
            super().configure(background = '#cfd6e6')
            self.select_bool = True
        else:
            super().configure(background = '#f5f6f7')
            self.select_bool = False

    def deselect(self, event):
        super().configure(background = '#f5f6f7')
    # def hover(self, event):
    #     super().configure(background = '#cfd6e6')
    
    # def leave(self, event):
    #     super().configure(background = '#f5f6f7')


class SatatusLabel(ttk.Label):
    
    def __init__(self, master, good_icon, bad_iconn, neutral_icon):
        super().__init__(master)
        super().config(text='')
        super().config(compound = 'left')
        self.good_icon =good_icon
        self.bad_icon = bad_iconn
        self.neutral_icon = neutral_icon
        self.neutral_status("")
        
    def good_status(self, content):
        super().config(image=self.good_icon)
        self.config(text=content)
    
    def bad_status(self, content):
        super().config(image=self.bad_icon)
        self.config(text=content)
    
    def neutral_status(self, content):
        super().config(image=self.neutral_icon)
        self.config(text=content)
              


class FileAndFolder(ttk.Frame):
    def __init__(self, master, name, icon, path):
        super().__init__(master)
        img = './image/ftp.png'
        img = (Image.open(img))
        img = img.resize((24, 24), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img)
        self.label = ttk.Label(self, image=self.img, text=name,  compound='left', font=('Times new roman', 18))
        self.label.pack()
        self.path = path
        self.run()
        # self.menu = tk.Menu(self, tearoff=0)
        # self.menu.add_command(label="Menu 1")
        # self.menu.add_command(label="Menu 2")
        # self.menu.add_command(label="Menu 3")
        # self.menu.add_command(label="Menu 4")
        # super().bind("<Button-3>", self.do_popup)

    def popup(self):
        self.popup_menu = tk.Menu(self,
                                       tearoff=0)

        self.popup_menu.add_command(label="say hi")

        self.popup_menu.add_command(label="say hello")
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="say bye")

    # def do_popup(self, event):
    #     try:
    #         self.menu.tk_popup(event.x_root, event.y_root)
    #     finally:
    #         self.menu.grab_release()

    def do_popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root,
                                     event.y_root)
        finally:
            self.popup_menu.grab_release()

    def run(self):
        self.popup()
        self.bind("<Button-3>", self.do_popup) 