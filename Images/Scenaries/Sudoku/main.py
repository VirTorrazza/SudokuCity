from ctypes import resize
from datetime import datetime
from sudokuvalidator import *
from solutions import *
import tkinter as tk
from tkinter import *
import functools
#from threads import *
from tkinter import HORIZONTAL, LEFT, NW, RAISED, TOP, PhotoImage, Toplevel, ttk,messagebox
import operator
import threading
import time
cancel_tmr=False
global debug
debug =1

class Drawing:# Drawing setup
    def __init__(self, root):
        self.root=root
        self.root.title("Sudoku City")
        self.mainWidth=0
        self.mainHeight=0
        self.positionRight=0
        self.positionDown=0
        self.root.state("zoomed") #maximize window (default)
        self.setGeometry()
        self.scenel=["Images/Scenaries/ruinsoriginal.png","Images/Scenaries/BuenosAires.png","Images/Scenaries/Rome.png","Images/Scenaries/Sydney.png","Images/Scenaries/Paris.png","Images/Scenaries/Mexico.png","Images/Scenaries/Madrid.png","Images/Scenaries/Dubai.png""Images/Scenaries/Dublin.png","Images/Scenaries/London.png","Images/Scenaries/Shangai.png","Images/Scenaries/NewYork.png","Images/Scenaries/Tokyo.png","Images/Scenaries/FutureCity.png","Images/Scenaries/7thCity.png"]
        self.atelier=Canvas(self.root,width=self.mainWidth,height=self.mainHeight,bd=0,highlightthickness=0)
        self.atelier.pack(fill="both",expand=True)
        self.scenei=tk.PhotoImage(file=self.scenel[0])
        self.atelier.create_image(0,0,image=self.scenei,anchor=NW)
        self.root.iconbitmap("Images/sudoku1.ico")
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.tlevel=self.atelier.create_text(120,40,text="Level 0 : Ruins",font=("Tower Ruins",20))
        self.bounds=self.atelier.bbox(self.tlevel)
        self.twidth=self.bounds[2] -self.bounds[0]
        self.theight=self.bounds[3] -self.bounds[1]
        self.atelier.coords(self.tlevel,(self.mainWidth//2),40)
        self.idebug=tk.PhotoImage(file="Images/bug.png")
        self.atelier.create_image(0,0,image=self.idebug,anchor=NW)
        self.lmdebug=tk.Label(self.root,image=self.idebug)
        if (debug==1):
            self.lmdebug.pack(pady=(0,0),padx=(0,0),expand=False)
        else:
            self.lmdebug.pack_forget()
        self.fontsl=[("BuenosAiresNF",22),("King of Rome",22),("Black Way - Personal Use",24),("Homeday",28),("King Luau",24),("Café Madrid",24),("ArabDances",27),("Helmantica",21),("Imperial Force",22),("Chinatown Champs",20), ("New York City",26),("JAPANBRUSH",24),("Future Now",22),("New Wave Aztec",12)]
        self.ilevelc=tk.PhotoImage(file="Images/completed150x68.png")
        #self.ltcompleted=self.atelier.create_image((self.mainWidth//2),self.bounds[3]-30,image=self.ilevelc,anchor=NW)
        self.ilevelf=tk.PhotoImage(file="Images/failed150x80.png")
        self.ltfailed=self.atelier.create_image((self.mainWidth//2),self.bounds[3]-43,image=self.ilevelf,anchor=NW)
        self.frame=tk.Frame(self.root) #create a frame for widgets
        self.frame.config(bg="#ee6c4d",width=520,height=500)
        self.boardWindow=self.atelier.create_window(((self.mainWidth//2)-(225)),(self.mainHeight//2-(185)),anchor=NW, window=self.frame)
        self.iplay=PhotoImage(file="Images/play_18x20.png")
        self.bplay=tk.Button(image=self.iplay,text="PLAY",borderwidth=4, compound="left",command=self.button_play)
        self.bpWidht=47
        self.playWindow=self.atelier.create_window((self.mainWidth//2)-self.bpWidht,520,anchor=NW,window=self.bplay)
        self.iclear=PhotoImage(file="Images/clear_20x20.png")
        self.bclear=tk.Button(text="Clear", image=self.iclear,compound="left",state="disabled",borderwidth=4,bg="#f5dd90",activebackground="#d08c60", justify="center", font=('Arial',10),command=self.button_clear)
        self.clearWindow=self.atelier.create_window((self.mainWidth//2)-30,580,anchor=NW,window=self.bclear)
        self.twinkling_color="SystemWindow"
        self.icheck=PhotoImage(file="Images/check_20x20.png")
        self.bcheck=tk.Button(text="Check", image=self.icheck,compound="left",state="disabled",borderwidth=4,bg="#99d98c",activebackground="#4c956c", justify="center", font=('Arial',10), command=self.button_check)
        self.checkWindow=self.atelier.create_window((self.mainWidth//2)+50,580,anchor=NW,window=self.bcheck)
        self.ianswer=PhotoImage(file="Images/answer_18x20.png")
        self.banswer=tk.Button(text="Answer",image=self.ianswer, compound="left",state="disabled",borderwidth=4,bg="#ff928b",activebackground="#772e25", justify="center", font=('Arial',10), command=self.button_answer)
        self.checkWindow=self.atelier.create_window((self.mainWidth//2)-111,580,anchor=NW,window=self.banswer)
        self.iprev=PhotoImage(file="Images/prev_29x20.png")
        self.bprev=tk.Button(text="PREV",image=self.iprev,state= "disabled",borderwidth=4,compound="top",command=self.button_prev)
        self.inext=PhotoImage(file="Images/next_29x20.png")
        self.bnext=tk.Button(text="NEXT",image=self.inext,state="disabled",borderwidth=4,compound="top",command=self.button_next)
        self.prevWindow=self.atelier.create_window((self.mainWidth//2)-170,520,anchor=NW,window=self.bprev)
        self.nextWindow=self.atelier.create_window((self.mainWidth//2)+130,520,anchor=NW,window=self.bnext)
        self.banswer.bind("<Enter>",self.enterahover)
        self.banswer.bind("<Leave>",self.leaveahover)
        self.bcheck.bind("<Enter>",self.enterhover)
        self.bcheck.bind("<Leave>",self.leavehover)
        self.initc= "00:00:00"
        self.running=False #flag that enables the running time of the game
        self.hour=0
        self.minute=0
        self.second=0
        self.cbinit=False
        self.lclock=tk.Label(text=self.initc, font=("Helvetica",15),fg="red",bg="black")
        self.clockWindow=self.atelier.create_window(654,self.mainHeight-90,anchor=NW,window=self.lclock)
        self.elist=[]
        self.tflag=True #flag for verification process
        self.flag_isStarted=False
        self.countanswer=0
        self.playcount=0
        self.isLevelUp=False
        self.count=0
        self.lpassed=0
        self.bonusflag=False
        self.lback=0
        self.checkcounter=0 #counts number of checks made in each level 
        self.response=2 #flag that indicates the ask yes/no quit answer
        self.cityl=["Buenos Aires", "Rome","Sydney","Paris","Mexico","Madrid","Dubai","Dublin","London","Shangai","New York", "Tokio", "Future City", "Seventh City of Gold"]
        self.textl=[]
        self.textn=0
        self.solutionsl=[s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14]
        self.wrotemapl=[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14]
        self.atelier.create_rectangle(0,(self.mainHeight -20),self.mainWidth,self.mainHeight, fill="#e9edc9")
        self.today=datetime.today().strftime('%Y-%m-%d')
        self.trect=self.atelier.create_text(200,self.mainHeight -10,text=self.today,font=("Times New Roman",10))
   
        
    
    def on_closing(self):
        self.response=tk.messagebox.askyesno("Exit Menu","Are you sure you want to quit?")
        if self.response ==1:
            self.root.destroy()
    

    def debug_initialize(self):
        
        if (self.flag_isStarted== False):
            self.banswer.configure(state="disabled")
            self.bcheck.configure(state="disabled")
            self.bclear.configure(state="disabled")
        
        else:
            self.define_Newlevel()
            self.banswer.configure(state="normal")
            self.bcheck.configure(state="normal")
            self.bclear.configure(state="normal")
            self.bplay.configure(state="disabled")
            self.running=True
            time.sleep(0.25)
            self.initial_Values(self.wrotemapl[self.textn])
            self.auto_completed(self.solutionsl[self.textn])

    def auto_completed(self,s):
        flatlist=sum(s,[])
        for x in range (0, len(flatlist)): 
                self.elist[x].insert(0,flatlist[x])
                

    def initialize(self):
        if (self.flag_isStarted== False):
            self.banswer.configure(state="disabled")
            self.bcheck.configure(state="disabled")
            self.bclear.configure(state="disabled")
        
        else:
            self.define_Newlevel()
            self.banswer.configure(state="normal")
            self.bcheck.configure(state="normal")
            self.bclear.configure(state="normal")
            self.bplay.configure(state="disabled")
            self.running=True
            time.sleep(0.25)
            self.initial_Values(self.wrotemapl[self.textn])
            
    def define_Newlevel(self):
        new_level=self.get_glevel()
        if (new_level==0):
            self.llevel.configure(font=self.fontsl[0])
            self.llevel.configure({'text':'Level 1 : Buenos Aires'})
    
    def blankmap(self): #Function that blanks the sudoku's board
        for x in self.elist:
            x.configure(state="normal")
            x.delete(0,tk.END)
    
    def init_blevel(self):
        self.banswer.configure(state="normal")
        self.bcheck.configure(state="normal")
        self.bclear.configure(state="normal")
        self.bplay.configure(state="disabled")
        self.resetClock()
        #self.running=True
        #self.tflag=True
        if(debug==1):
            self.auto_completed(self.solutionsl[self.get_glevel()-1])
      
            
    def initialLevel(self):
        self.banswer.configure(state="normal")
        self.bcheck.configure(state="normal")
        self.bclear.configure(state="normal")
        self.bplay.configure(state="disabled")
        self.resetClock()
        self.isLevelUp=False
        self.lpassed=0
        self.running=True
        self.tflag=True
        self.sclock()
        if(debug==1):
            self.auto_completed(self.solutionsl[self.textn])



    def enterhover(self,e): # function for entering check botton (tooltip)
        self.atelier.itemconfig(self.trect,text="Board must be full to check")
    
    def leavehover(self,e): # function for leaving check botton (tooltip)
        self.atelier.itemconfig(self.trect,text=self.today)
    
    def enterahover(self,e): # function for entering answer botton (tooltip)
        self.atelier.itemconfig(self.trect,text="Asking for answer will automatically disable Bonus")
    
    def leaveahover(self,e): # function for leaving answer botton (tooltip)
        self.atelier.itemconfig(self.trect,text=self.today)
  

    def make_Board(self):# function that creates the sudoku's board
        contr=1 #counter for rows
        contc=1 #counter for columns
        
        
        for x in range(0,9):
            for j in range (0,9):
                if (contr % 3==0 and contr!=9):
                    pdl=2
                else:
                    pdl=0
                
                if (contc %3==0 and contc!=9):
                    padc=2
                else:
                    padc=0

                
                e=tk.Entry(self.frame, width=3,justify="center", font=('Arial',20))
              
                if (self.flag_isStarted==False):
                    e.configure(state="disabled")
                   
                else:
                    e.configure(state="normal")
                e.grid(row=x,column=j,padx=(0,pdl),pady=(0,padc))
                self.elist.append(e)                 
                contr+=1
            contr=1
            contc+=1
        #self.setGeometry()
    
    #Function that set the dimensions of root acording to screen
    def setGeometry(self):
        self.root.update()
        self.mainWidth=self.root.winfo_width()
        self.mainHeight=self.root.winfo_height()
        #self.root.update_idletasks()
        self.fullScreenState = False
        self.root.attributes("-fullscreen", self.fullScreenState)
        self.positionRight = int(self.root.winfo_screenwidth()/2 - int(self.mainWidth)/2)
        self.positionDown = int(self.root.winfo_screenheight()/2 - int(self.mainHeight)/2)
        #self.root.geometry("+{}+{}".format(self.positionRight, (self.positionDown-30)))
        self.root.geometry("{}x{}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        
        
        print(self.mainWidth)
        print(self.mainHeight)
        print(self.positionRight)
        print(self.positionDown)

    def verify_Timer(self):
        if(self.response!=1):
            if (self.tflag==True):
                self.verify_Bentry()
                self.is_completed()
            if (not cancel_tmr):
                threading.Timer(0.25,self.verify_Timer).start()
    
    def twinkling(self):
        self.count+=1 #counter for times blinking
        for x in self.ltw:
            self.elist[x].config({"fg": "#ae2012"})
            self.current_color= self.elist[x].cget("background")
            if (self.current_color=="SystemWindow"):
                self.twinkling_color="yellow"
                
            else:
                self.twinkling_color="SystemWindow"
                

            self.elist[x].config(background=self.twinkling_color)
        
        if(self.count<20 and (len(self.ltw)!=0)):
            self.elist[x].after(350,self.twinkling)
            
        else:
            self.count=0
            if(len(self.ltw)!=0):
                self.isLevelUp=False
                for x in self.ltw:
                    self.elist[x].config({"bg": "SystemWindow"})
                self.tflag=True
        
            else:
                self.tflag=False
                self.flag_isStarted=False
                self.initialize()
                self.isLevelUp=True
                self.habilitateb()
                self.lcompleted.pack(pady=(0,0),padx=(0,0),expand=False)
            
    def habilitateb(self):
        if(self.lpassed ==0):
            self.bnext.config(state="normal")
        else:
            self.bnext.config(state="disabled")
        
        if(self.countanswer==0):
            self.bonusflag=True
        else:
            self.bonusflag=False
        if(self.get_glevel()==13 and self.bonusflag==False):
            self.bnext.config(state="disabled")
            self.bnext.bind("<Enter>",self.nextehover)
            self.bnext.bind("<Leave>",self.nextlhover)
        
        if(self.get_glevel()==14):
            self.bnext.config(state="disabled")

    def get_glevel(self): #function that gets the int value of the current level 
        texts=self.llevel.cget("text")
        self.textl=texts.split()
        self.textn= int(self.textl[1])
        return self.textn
    
    def set_glevel(self,x):
        self.textn=x #game level int
    
    def next_level(self):#function that increases a level   
        current_level=self.get_glevel()
        if(current_level<14 and self.lpassed==0):
            self.lpassed=1
            self.set_glevel(current_level +1)
            self.LevelUp()
   
            
    
    def prev_level(self): #function that decreases a level
        current_level=self.get_glevel()-1
        self.set_glevel(current_level)
        if (current_level >=1):
            self.lback=1
            self.LevelDown()
            if(current_level==1):
                self.bprev.config(state="disabled")
                self.bprev.bind("<Enter>",self.prevehover)
                self.bprev.bind("<Leave>",self.prevlhover)
            
         
    def prevehover(self,e):
        self.atelier.itemconfig(self.trect,text="No more levels availables")

    def prevlhover(self,e):
       self.atelier.itemconfig(self.trect,text=self.today)
    
    def nextehover(self,e):
        self.atelier.itemconfig(self.trect,text="if completed and not failed levels, bonus will be available")
    
    def nextlhover(self,e):
        self.atelier.itemconfig(self.trect,text=self.today)
        
    def LevelDown(self):
        self.define_prevcity()
        self.blankmap()
        self.initial_Values(self.wrotemapl[self.get_glevel()-1])
        print("soy textn {}".format (self.textn))
        print("soy level {}".format (self.get_glevel()))
        self.init_blevel()
            
    
    def define_prevcity(self):
        nivel=self.get_glevel()-1
        for i in range (0, len(self.cityl)):
            if (i==nivel):
                self.llevel.config(text="")
                sl="Level"
                new_text=sl + " " + str(i) + " " + ":" + " " + self.cityl[i-1]
                self.llevel.configure(font=self.fontsl[i-1])
                self.llevel.config(text=new_text)
                break
    
    def get_isLevelUp(self): #getter of isLevelUp variable
        return self.isLevelUp


    def LevelUp (self):
            self.define_cities()
            self.blankmap()
            self.initial_Values(self.wrotemapl[self.textn])
            self.initialLevel()
            self.habilitateb()
            self.hback()
    
    def hback(self):
        self.bprev.config(state="normal")


    def initial_Values(self,a): #function thet initializes the sudoku according to the level
        flatlist=sum(a,[])
        for x in range (0, len(flatlist)): 
            if(flatlist[x]!=0):
                self.elist[x].configure(state="normal")
                self.elist[x].insert(0,flatlist[x])
                self.elist[x].configure(state="disabled")
            else:
                self.elist[x].configure(state="normal")
                self.elist[x].insert(0,"")

    def verify_Bentry(self): #function that verifies if entries are valid. If not, they are painted red
        if self.response!=1:
            lsnum=["0","1","2","3","4","5","6","7","8","9",""]
            for elem in self.elist:           
                xtext=elem.get()
                if (xtext not in lsnum):
                    elem.config({"fg":"Red"})
                else:
                    elem.config({"fg":"Black"})
    

    def button_play(self):
        self.flag_isStarted=True
        self.playcount+=1
        if (debug ==0):
            self.initialize()
        else:
            self.debug_initialize()
        
    def button_clear(self):
        self.hour=0
        self.minute=0
        self.second=0
        self.tflag=True #flag for entry verification process
        for x in self.elist:
            bstate= x.cget('state')
            if (bstate=="normal"):
                x.delete(0,tk.END)
        
        self.lclock.config(text=self.initc)
    
    def button_answer(self):
        self.countanswer+=1
        self.bcheck.bind("<Enter>",self.leavehover)
        self.running=False
        self.lfailed.pack(pady=(0,0),padx=(0,0),expand=False)
        flatlist=sum(self.solutionsl[self.textn -1],[])
        self.tflag=False
        # en el drswing capaz debería tener un id para ver a qué sudoku corresponde cada rta o level
        for x in range (0, len(self.elist)):
            bstate=self.elist[x].cget("state")
            self.elist[x].config(foreground="#d00000")
            if (bstate!="disabled"):
                self.elist[x].delete(0,tk.END)
                self.elist[x].insert(0,flatlist[x])
                
            else:
                continue
        self.lclock.config(text=self.initc)
        
    def is_completed(self):# checks if the sudoku's entries are full
        scontentl=[]
        for x in self.elist:
            bstate= x.cget('state')
            if (bstate =="normal"):
                content=x.get()
                scontentl.append(content)
        
        if (self.flag_isStarted==True):
        
            if (any(x=="" for x in scontentl)):
                self.bcheck.config(state="disabled")
            else:
                self.bcheck.config(state="normal")

    def button_prev(self):
        self.prev_level()

    def button_next(self):
        self.lcompleted.pack_forget()
        self.next_level()
        self.habilitateb()
        
    def button_check(self):
        self.running=False
        self.tflag=False
        self.vbooln=0
        self.checkcounter+=1
        self.ltw=[]
        flatl= functools.reduce(operator.__iconcat__,self.solutionsl[self.get_glevel()-1],[])
        for x in range(0, len(self.elist)):
            evalue=self.elist[x].get()       
            if(evalue == str(flatl[x])):
                self.vbooln+=True
            else:
                self.vbooln+=False
                self.ltw.append(x)
        
        if(debug!=1):
            self.pwindow=Toplevel()
            self.pwindow.title("Checking...")
            self.pwindow.geometry("330x60")
            self.pwindow.iconbitmap("Images/hourglass1.ico")
            self.pwindow.resizable(False,False)
            self.pbar=ttk.Progressbar(self.pwindow,orient=HORIZONTAL,length=200,mode="indeterminate")
            self.pbar.place(relx=0.5,rely=0.5,anchor="center")
            self.pwindow.geometry('250x50+600+300' )
            thpbar=threading.Thread(name="t1",target=self.run_progressBar)
            thpbar.start()
        else:
            self.running= True
            self.twinkling()
    
    def run_progressBar (self):
        self.pbar.start(10)
        threading.Timer(5,self.timeout).start()
        time.sleep(5)
    
    def timeout(self):
        self.pbar.stop()
        self.running=True
        self.twinklingThread()
        self.pwindow.destroy()
  
        
    def twinklingThread(self):
        self.t3=threading.Thread(name="t3",target=self.twinkling)
        self.t3.start()
        

    def sclock(self):
        if self.running:
            self.second+=1
            if (self.second==60):
                self.minute+=1
                self.second=0
        
            if (self.minute==60):
                self.hour+=1
                self.minute=0
        
        #string format to include leading zeros
        shour= f'{self.hour}' if self.hour >9 else f'{self.hour}'
        sminute= f'{self.minute}' if self.minute >9 else f'{self.minute}'
        ssecond= f'{self.second}' if self.second >9 else f'{self.second}'

        self.lclock.config(text=shour + ":" + sminute + ":" + ssecond)
        if (self.isLevelUp==False):
            self.lclock.after(1000,self.sclock)
    
    def resetClock(self):
        self.hour=0
        self.minute=0
        self.second=0

    def define_cities(self): #Function that defines the city according to each level
        for i in range (0, len(self.cityl)):
            n=i+1
            if (n==self.get_glevel()):
                self.llevel.config(text="")
                sl="Level"
                new_text=sl + " " + str(n+1) + " " + ":" + " " + self.cityl[i+1]
                self.llevel.configure(font=self.fontsl[i+1])
                self.llevel.config(text=new_text)
                break
            
        
            
            
        

        

def main(): 
    root= tk.Tk()
    sud1= Drawing(root)
    sud1.make_Board()
    #sud1.initialize()
    sud1.sclock()
    #sud1.elist[0].insert(0,"3")
    #sud1.elist[1].insert(0,"q")
    #sud1.elist[2].insert(0,"13")
    #sud1.initial_Values(a)
    sud1.verify_Timer()
    root.mainloop()


if __name__ == '__main__':
    main()
    #cancel_tmr=True
    



