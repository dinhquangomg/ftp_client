import os
from os import listdir
from os.path import isfile, join
import shutil
import sys
from ftplib import FTP

class FtpController:
    def __init__(self):
        self.ftp = None

    def connect_to(self, host, username=' ', password=' ', port=21):
        self.ftp = FTP()
        self.ftp.connect(host, port)
        self.ftp.login(username, password)

    def get_file_and_folder(self):
        data = []
        self.ftp.dir(data.append)
        result = []
        for x in data:
            result.append([i for i in x.split(' ') if i != ''])
        return result

    def change_directory(self, name):
        self.ftp.cwd(name)
    
    def get_path(self):
        return self.ftp.pwd()
    
    def download_file(self, path):
        filename = path.split('/')[-1]
        print(path)
        with open(path, "wb") as file:
            self.ftp.retrbinary(f"RETR {filename}", file.write)
    
    def upload_file(self, path):
        filename = path.split('/')[-1]
        with open(path, 'rb') as file:
            self.ftp.storbinary(f'STOR {filename}', file)
            
    def add_folder(self, name):
        self.ftp.mkd(name)
    
    def remove_file(self, name):
        self.ftp.delete(name)
        
    def remove_folder(self, name):
        self.ftp.rmd(name)
    
    def disconnect(self):
        self.ftp.close()
        
    
            

