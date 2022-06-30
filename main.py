import time
import tkinter as tk
import tkinter.simpledialog
from tkinter import messagebox
from ctypes import windll
import win32gui

from tkwebview2.tkwebview2 import WebView2
from threading import Thread
from System.Threading import (Thread,ApartmentState,ThreadStart)

from pystray import MenuItem as item
import pystray
from PIL import Image

application_name = 'live-stream-wallpaper'

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        WIDTH = 0
        HEIGHT = 0

        x = int((self.winfo_screenwidth() / 2) - (WIDTH / 2))
        y = int((self.winfo_screenheight() / 2) - (HEIGHT / 2))
        self.overrideredirect(True)
        self.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')

        self.youtube_url = None
        
        value = tkinter.simpledialog.askstring("Enter Value","enter a youtube url\t\t\t\t\t\t",parent=self)
        self.set_youtube_url(value)

        self.title(application_name)
        self.overrideredirect(False)
        self.attributes('-fullscreen', True)
        self.attributes('-disabled', True)
        self.resizable(False, False)

        self.frame = WebView2(self, 1920, 1080)
        self.frame.pack()
        self.loadHtml()
        
        self.after(500,lambda: self.setAsBackground())

    def set_youtube_url(self, url):
        self.youtube_url = url.replace('watch?v=', 'embed/')
    
    def loadHtml(self):
        self.frame.load_html(f'<iframe style="position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;" src="{self.youtube_url}?controls=0&mute=1&autoplay=1" frameborder="0" allow="accelerometer; autoplay=1; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')

    def find_desktop_hwnd(self):
        hwnd = windll.user32.FindWindowW(0, u'Program Manager')
        win32gui.SendMessageTimeout(hwnd, 0x052C, 0, None, 0, 0x03E8)
        hwnd_WorkW = None
        while 1:
            hwnd_WorkW = windll.user32.FindWindowExW(None, hwnd_WorkW, "WorkerW", None)
            if not hwnd_WorkW:
                continue
            hView = windll.user32.FindWindowExW(hwnd_WorkW, None, "SHELLDLL_DefView", None)
            if not hView:
                continue
            h = windll.user32.FindWindowExW(None, hwnd_WorkW, "WorkerW", None)
            while h:
                win32gui.SendMessage(h, 0x0010, 0, 0)
                h = windll.user32.FindWindowExW(None, hwnd_WorkW, "WorkerW", None)
            break
        return hwnd

    # set background handle as application window's parent
    def setAsBackground(self):
        h = windll.user32.FindWindowW(0, application_name)
        windll.user32.SetParent(h, self.find_desktop_hwnd())

class SystemTrayIcon():
    def __init__(self, app):
        self.app = app
        image=Image.open("favicon.ico")
        #menu=(item('Update url', self.update_url), item('Quit', self.quit_window))
        menu=(item('Quit', self.quit_window),)
        icon = pystray.Icon("name", image, "live stream wallpaper", menu)
        icon.run_detached()
    
    def update_url(self, icon, item):
        print ('show_window')

        # temp = tk.Tk()
        # temp.withdraw()
        # fix tkinter dialog focus bug
        # https://stackoverflow.com/questions/53763079/tkinter-filedialog-is-stealing-focus-and-not-returning-it-without-alt-tab-in-p/53765237#53765237
        # temp.update_idletasks()
        # value = tkinter.simpledialog.askstring("Enter Value","enter a youtube url\t\t\t\t\t\t",parent=temp)
        # print(value)
        #self.app.youtube_url=value
        #self.app.loadHtml()
        # temp.destroy()
        
    def quit_window(self, icon, item):
        icon.stop()
        self.app.destroy()

def main():
    app = App()
    trayIcon = SystemTrayIcon(app)
    app.mainloop()

if __name__ == "__main__":
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
