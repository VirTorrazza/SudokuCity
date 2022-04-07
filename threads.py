import threading
from tkinter import HORIZONTAL, Toplevel, ttk

class ThreadPbar (threading.Thread):
    def __init__(self, namet, running):
        threading.Thread.__init__(self,name=namet, target=self.run)
        self.namethread= namet   
        
        self.running=running
    
    
        
        