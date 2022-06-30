from pprint import pprint
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfile, askopenfile
from core.FTP_controller import FtpController
from core.Custom import FLabel, SatatusLabel
import threading


class App:
    def __init__(self, master):
        # Set app title
        self.thread = None  
        self.ftp_controller = None
        self.select_path = None
        self.master = master
        master.title(' ' * 80 + 'FTP Client')
        # Disable window resizing function
        master.resizable(False, False)
        # Get the size of the screen
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        # Set window size and display
        width = 800
        height = 600
        master.geometry(f'{width}x{height}+{(screen_width - width) // 2}+{(screen_height - height) // 2}')
        # Set Window icon
        master.iconbitmap('./icon/ftp.ico')
        # Crate Tkinter Frame toolbar
        self.tool_bar = ttk.Frame(master)
        self.tool_bar.pack(fill=X)
        # Crate Tkinter Frame entry_bar
        self.entry_bar = ttk.Frame(master)
        self.entry_bar.pack(fill=X, ipady=5)

        # Load icon
        self.folder_icon = PhotoImage(file='./image/Icon/folder.png')
        self.file_icon = PhotoImage(file='./image/Icon/file.png')
        self.connect_icon = PhotoImage(file='./image/Icon/play-button.png')
        self.upload_icon = PhotoImage(file='./image/Icon/upload_folder.png')
        self.download_icon = PhotoImage(file='./image/Icon/download_folder.png')
        self.addfolder_icon = PhotoImage(file='./image/Icon/add-folder.png')
        self.remove_icon = PhotoImage(file='./image/Icon/trash-bin.png')
        self.disconnect_icon = PhotoImage(file='./image/Icon/disconnect.png')
        # Load Icon Hover
        self.connect_icon_hover = PhotoImage(file='./image/Icon_Hover/play-button.png')
        # Load Icon Active
        self.connect_icon_active = PhotoImage(file='./image/Icon_Active/play-button.png')
        # Create connect button
        self.connect_button = tk.Button(
            master=self.tool_bar,
            text=" Connect",
            image=self.connect_icon,
            compound="left",
            borderwidth=0,
            command=self.connect_to_ftp
        )
        self.connect_button.pack(side='left', padx=5, ipadx=5)
        # Create upload button
        self.upload_button = tk.Button(
            master=self.tool_bar,
            text=" Upload",
            image=self.upload_icon,
            compound="left",
            borderwidth=0,
            command=self.upload
        )
        self.upload_button.pack(side='left', padx=5, ipadx=5)
        # Create download button
        self.download_button = tk.Button(
            master=self.tool_bar,
            text=" Download",
            image=self.download_icon,
            compound="left",
            borderwidth=0,
            command=self.download
        )
        self.download_button.pack(side='left', padx=5, ipadx=5)
        self.addfolder_button = tk.Button(
            master=self.tool_bar,
            text=" New Folder",
            image=self.addfolder_icon,
            compound="left",
            borderwidth=0,
            command=self.disconnect
        )
        self.addfolder_button.pack(side='left', padx=5, ipadx=5)
        self.remove_button = tk.Button(
            master=self.tool_bar,
            text=" Remove",
            image=self.remove_icon,
            compound="left",
            borderwidth=0,
            command=self.remove
        )
        self.remove_button.pack(side='left', padx=5, ipadx=5)
        # Create disconnect button
        self.disconnect_button = tk.Button(
            master=self.tool_bar,
            text=" Disconnect",
            image=self.disconnect_icon,
            compound="left",
            borderwidth=0,
            command=self.disconnect
        )
        self.disconnect_button.pack(side='left', padx=5, ipadx=5)
        
        # Create label field for hostname
        self.label_hostname = ttk.Label(self.entry_bar, text='Host:')
        self.label_hostname.pack(side='left', padx=2)
        # Create entry field for hostname
        self.hostname_entry = ttk.Entry(self.entry_bar)
        self.hostname_entry.pack(side='left', expand=True, fill=X)
        # Create label for username
        self.label_username = ttk.Label(self.entry_bar, text='Username:')
        self.label_username.pack(side='left', padx=2)
        # Create text field for username
        self.username_entry = ttk.Entry(self.entry_bar)
        self.username_entry.pack(side='left', expand=True, fill=X)
        # Create label for password
        self.label_pass = ttk.Label(self.entry_bar, text='Password:')
        self.label_pass.pack(side='left', padx=2)
        # Create textfield for password
        self.pass_entry = ttk.Entry(self.entry_bar, show='*')
        self.pass_entry.pack(side='left', expand=True, fill=X)
        # Create label for port
        self.label_port = ttk.Label(self.entry_bar, text='Port:')
        self.label_port.pack(side='left', padx=2)
        # Create textfield for port
        self.port_entry = ttk.Entry(self.entry_bar, width=4)
        self.port_entry.pack(side='left', padx=(0, 2))
        self.port_entry.insert(END, '21')

        self.pad_frame = ttk.Frame(root)
        # self.myscrollbar = Scrollbar(self.pad_frame, orient="vertical")
        # self. myscrollbar.pack(side="right", fill="y")
        # self.vbar = ttk.Scrollbar(self.pad_frame, orient=VERTICAL, style='Vertical.TScrollbar')
        # self.vbar.pack(anchor=E, side=RIGHT, fill=Y)

        self.pad_frame.pack(fill=BOTH, expand=True)

        self.good_icon = PhotoImage(file='./image/Icon/check.png')
        self.bad_icon = PhotoImage(file='./image/Icon/multiply.png')
        self.neutral_icon = PhotoImage(file='./image/Icon/full-moon.png')
        self.status_frame = ttk.Frame(root)
        self.status_frame.pack(fill=BOTH, expand=True)
        self.status = SatatusLabel(root,self.good_icon, self.bad_icon, self.neutral_icon)
        self.status.pack(fill=X, side = BOTTOM)

    def connect_to_ftp(self, event=None):
        try:
            self.ftp_controller.disconnect()
            del self.ftp_controller
        except Exception as e:
            pass
        self.ftp_controller = FtpController()
        self.thread = threading.Thread(target=self.connect_thread, args=(self.ftp_controller,
                                                                         self.hostname_entry.get(),
                                                                         self.username_entry.get(),
                                                                         self.pass_entry.get(),
                                                                         int(self.port_entry.get())))
        self.thread.daemon = True

        self.thread.start()
        self.set_status('neutral', 'connecting...')

    def connect_thread(self, ftp_controller, host, username, passwd, port):
        try:
            ftp_controller.connect_to(host, username, passwd, port)
            
        except:
            pass
        self.update_pad()
        self.set_status('good', 'connected')
        
    def update_pad(self):
        try:
            if self.arr_f:
                for x in self.arr_f:
                    x.destroy()
                del self.arr_f
        except:
            pass
        self.arr_f = []
        if self.ftp_controller:
            self.arr_f.append(FLabel(self.pad_frame, '.', self.folder_icon,'.',self.left_click_folder))
            self.arr_f.append(FLabel(self.pad_frame, '..', self.folder_icon,'..',self.left_click_folder))
            data = self.ftp_controller.get_file_and_folder()
            for i in range(len(data)):
                if data[i][0][0]=='d':
                    self.arr_f.append(FLabel(self.pad_frame, str(data[i][-1]), self.folder_icon,str(data[i][-1]),self.left_click_folder, self.right_click_folder))
                else:
                    self.arr_f.append(FLabel(self.pad_frame, str(data[i][-1]), self.file_icon,str(data[i][-1]),None, self.right_click_folder))
    def left_click_folder(self, name):
        self.ftp_controller.change_directory(name)
        self.update_pad()
        
    def right_click_folder(self, name):
        path = self.ftp_controller.get_path()+'/'+name
        if path == self.select_path:
            self.select_path = None
            for x in self.arr_f:
                x.deselect(None)
        else:
            self.select_path = path
            for x in self.arr_f:
                if x.path == name:
                    x.select(None)
                else:
                    x.deselect(None)
    
    def download(self):
        self.set_status('neutral','downloading ...')
        try:
            with asksaveasfile(initialfile=self.select_path.split('/')[-1]) as file:
                self.ftp_controller.download_file(file.name)       
                self.set_status('good','downloaded')
        except Exception as e:
            self.set_status('bad','download failed')
    
    def upload(self):
        self.set_status('neutral','oppening ...')
        try:
            with askopenfile(mode ='r') as file:
                self.ftp_controller.upload_file(file.name)
                self.set_status('good','uploaded')
        except:
            self.set_status('bad','upload failed')
        self.update_pad()
    
    def remove(self):
        data = self.ftp_controller.get_file_and_folder()
        try:
            if self.select_path != None:
                for f in data:
                    if self.select_path.split('/')[-1]==f[-1]:
                        if f[0][0]=='d':
                            self.ftp_controller.remove_folder(self.select_path)
                        else:
                            self.ftp_controller.remove_file(self.select_path)
            self.set_status('good', 'Successful')    
        except:
            self.set_status('bad', 'Failure') 
        self.update_pad()
            
    
    def disconnect(self):
        self.ftp_controller.disconnect()
        self.set_status('good','disconnected')
        del self.ftp_controller
        self.update_pad()
        
    def set_status(self, status, content):
        if status=='good':
            self.status.good_status(content)
        elif status=='bad':
            self.status.bad_status(content)
        elif status=='neutral':
            self.status.neutral_status(content)
            

root = tk.Tk()
FTP_Client = App(root)
root.mainloop()
