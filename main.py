#Project developed by Virginia Torrazza and Iván Avila

from distutils.debug import DEBUG
from email.policy import default
from tkinter.font import Font
from pynput.keyboard import *
from tkinter import simpledialog
from tkinter.tix import COLUMN
import sys
import PIL
import glob
from datetime import datetime
import pygame
from sudokuvalidator import *
from solutions import *
import tkinter as tk
from tkinter import *
import functools
from tkinter import HORIZONTAL, LEFT, NW, RAISED, TOP, PhotoImage, Toplevel, ttk,messagebox
import operator
import threading
import time
cancel_tmr=False
global debug
debug =0
global numberseq
numberseq=0

#Class for drawing setup
class Drawing:
    def __init__(self, root):
        self.root=root
        self.root.title("Sudoku City")
        self.mainWidth=0
        self.mainHeight=0
        self.positionRight=0
        self.positionDown=0
        self.root.state("zoomed") #Maximize window (default)
        self.root.bind('<Escape>', lambda e: self.on_closing())
        self.username=None
        self.setGeometry()
        self.scenel=["Images/Scenaries/Ruins.png","Images/Scenaries/BuenosAires.png","Images/Scenaries/Rome.png","Images/Scenaries/Sydney.png","Images/Scenaries/Paris.png","Images/Scenaries/Mexico.png","Images/Scenaries/Madrid.png","Images/Scenaries/Dubai.png","Images/Scenaries/Dublin.png","Images/Scenaries/London.png","Images/Scenaries/Shanghai.png","Images/Scenaries/NewYork.png","Images/Scenaries/Tokyo.png","Images/Scenaries/FutureCity.png","Images/Scenaries/7thCity.png"]
        self.atelier=Canvas(self.root,width=self.mainWidth,height=self.mainHeight,bd=0,highlightthickness=0)
        self.atelier.pack(fill="both",expand=True)
        self.scenei=PhotoImage(file=self.scenel[0])
        self.currentscene=self.atelier.create_image(0,0,image=self.scenei,anchor=NW)
        self.root.iconbitmap(default="Images/Ornate/sudoku.ico")
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)
        self.toolFont=Font(family="Monotype Corsiva", size=10)
        self.tlevel=self.atelier.create_text(120,40,text="Level 0 : Ruins",font=("Tower Ruins",20),fill="#edf6f9")
        self.bounds=self.atelier.bbox(self.tlevel)
        self.twidth=self.bounds[2] -self.bounds[0]
        self.theight=self.bounds[3] -self.bounds[1]
        self.atelier.coords(self.tlevel,(self.mainWidth//2),40)
        if (debug==1):
            self.idebug=tk.PhotoImage(file="Images/Ornate/bug.png")
            self.atelier.create_image(self.mainWidth-45,0,image=self.idebug,anchor=NW)
        self.fontsl=[("BuenosAiresNF",24),("King of Rome",24),("Black Way - Personal Use",26),("Homeday",32),("King Luau",24),("Café Madrid",26),("ArabDances",27),("Helmantica",21),("Imperial Force",22),("Chinatown Champs",24), ("New York City",28),("JAPANBRUSH",26),("Future Now",24),("New Wave Aztec",14)]
        self.ilevelc=tk.PhotoImage(file="Images/Ornate/completed_150x67.png")
        self.ltcompleted=self.atelier.create_image((self.mainWidth//2),self.bounds[3]-43,image=self.ilevelc,anchor=NW)
        self.atelier.itemconfig(self.ltcompleted,state="hidden")
        self.ilevelf=tk.PhotoImage(file="Images/Ornate/failed_150x67.png")
        self.ltfailed=self.atelier.create_image((self.mainWidth//2),self.bounds[3]-43,image=self.ilevelf,anchor=NW)
        self.atelier.itemconfig(self.ltfailed,state="hidden")
        self.imframe=tk.PhotoImage(file="Images/Ornate/musicframe.png")
        self.mfheight=206 #Height of the music frame
        self.mfwidth=280 #Width of the music frame
        self.musict="MUSIC MENU"
        self.fmusic=self.atelier.create_image((self.mainWidth-self.mfwidth),(self.mainHeight -self.mfheight)-25,image=self.imframe,anchor=NW)
        self.iplayM=tk.PhotoImage(file="Images/Buttons/mplay.png")
        self.ipauseM=tk.PhotoImage(file="Images/Buttons/mpause.png")
        self.istopM=tk.PhotoImage(file="Images/Buttons/mstop.png")
        self.istats=tk.PhotoImage(file="Images/Buttons/stats_20x20.png")
        self.isave=tk.PhotoImage(file="Images/Buttons/save_20x20.png")
        self.bplayM=tk.Button(image=self.iplayM,borderwidth=2,command=self.button_playMusic)
        self.bpauseM=tk.Button(image=self.ipauseM,borderwidth=2,state="disabled",command=self.button_pauseMusic)
        self.bstopM=tk.Button(image=self.istopM,borderwidth=2,state="disabled",command=self.button_stopMusic)
        self.stopMWindow=self.atelier.create_window((self.mainWidth-self.mfwidth)+185,self.mainHeight-(self.mfheight)+70,anchor=NW,window=self.bstopM)
        self.pauseMWindow=self.atelier.create_window((self.mainWidth-self.mfwidth)+55,self.mainHeight-(self.mfheight)+70,anchor=NW,window=self.bpauseM)
        self.playMWindow=self.atelier.create_window((self.mainWidth-self.mfwidth)+108,self.mainHeight-(self.mfheight)+70,anchor=NW,window=self.bplayM)
        self.tmframe=self.atelier.create_text((self.mainWidth-self.mfwidth)+135,self.mainHeight-(self.mfheight)+26,text=self.musict,font=("Amadeus",20))
        self.frame=tk.Frame(self.root) #create a frame for widgets
        self.frame.config(bg="#ee6c4d",width=520,height=500)
        self.positionboardx=(self.mainWidth//2)-(225)
        self.positionboardy=(self.mainHeight//2)-(185)
        self.boardWindow=self.atelier.create_window(self.positionboardx, self.positionboardy,anchor=NW, window=self.frame)
        self.iplay=PhotoImage(file="Images/Buttons/play_18x20.png") 
        self.iclear=PhotoImage(file="Images/Buttons/clear_20x20.png")
        self.twinkling_color="SystemWindow"
        self.icheck=PhotoImage(file="Images/Buttons/check_20x20.png")
        self.ianswer=PhotoImage(file="Images/Buttons/answer_18x20.png")
        self.initc= "00:00:00"
        self.running=False #Flag that enables the running time of the game
        self.hour=0
        self.minute=0
        self.second=0
        self.cbinit=False
        
        self.elist=[]
        self.tflag=True #Flag for verification process
        self.flag_isStarted=False
        self.countanswer=0
        self.playcount=0
        self.isLevelUp=False
        self.count=0
        self.lpassed=0
        self.bonusflag=False
        self.lback=0
        self.checkcounter=0 #Counts number of checks made in each level 
        self.response=2 #Flag that indicates the ask yes/no quit answer
        self.cityl=["Buenos Aires", "Rome","Sydney","Paris","Mexico","Madrid","Dubai","Dublin","London","Shanghai","New York", "Tokio", "Future City", "Seventh City of Gold"]
        self.textl=[]
        self.textn=0
        self.solutionsl=[s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14]
        self.wrotemapl=[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14]
        self.atelier.create_rectangle(0,(self.mainHeight -20),self.mainWidth,self.mainHeight, fill="#e9edc9")
        self.today=datetime.today().strftime('%Y-%m-%d')
        self.trect=self.atelier.create_text(200,self.mainHeight -10,text=self.today,font=self.toolFont)
        self.isPaused=0
        self.musicl=["Sounds/01-Wuxia Village.mp3","Sounds/02-Wuxia Tea House.mp3","Sounds/03-Mushroom Forest.mp3","Sounds/04-A New Beginning.mp3","Sounds/05-The Frozen Trail.mp3","Sounds/06-Jahzzar Siesta.mp3","Sounds/07-Jelsonic Saying Goodbye.mp3","Sounds/08-Zen Spa.mp3","Sounds/09-Meditation Music.mp3","Sounds/10-Beethoven Moonlight Sonata.mp3","Sounds/11-Dexter Britain The Time To Run Finale.mp3","Sounds/12-Erik Satie  La 1ere lent et douloreux.mp3","Sounds/13-Evgeny Grinko Winter Sunshine.mp3","Sounds/14-Breathing.mp3","Sounds/15-Timofiy Starenkov The Journey.mp3","Sounds/16-Zero Project Llotana.mp3","Sounds/17-Vexento Now.mp3","Sounds/18-Relaxing Instrumental.mp3","Sounds/19-Scottbuckley Titan.mp3","Sounds/20-Tristan Lohengrin A Peaceful Sanctuary.mp3"]
        self.track=1
        self.indexm=0
        self.isStopped=0
        self.eventprev=0
        self.eventnext=0
        self.levelsdone=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.filenames=[]
        self.ttrackName=self.atelier.create_text((self.mainWidth-self.mfwidth)+135,self.mainHeight-(self.mfheight)+130,text="",font=("Monotype Corsiva",14))
        self.statsFile=None
        self.contentFile=[]
        self.savel=[]
        self.statstext=None
        self.Tstyle=ttk.Style()
        self.Tstyle.theme_use("default")
        self.Tstyle.configure("TreeView",background="#D3D3D3",foreground="black",rowheight=25,fieldbackground="#D3D3D3")
        self.Tstyle.map("Treeview", background=[('selected','#e07a5f')])
        self.treeFrame=tk.Frame(self.root)
        self.treeScroll=Scrollbar(self.treeFrame) 
        self.file_Tree=ttk.Treeview(self.treeFrame,yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side=RIGHT,fill=Y)
        self.treeScroll.config(command=self.file_Tree.yview)
        self.file_Tree.pack()
        self.fileTreeWindow=self.atelier.create_window(5,60,anchor=NW,window=self.treeFrame)
        self.atelier.itemconfigure(self.fileTreeWindow,state='hidden')
        self.make_Board()
        self.root.update()
        self.bplay=tk.Button(image=self.iplay,text="PLAY",borderwidth=4, compound="left",state="disabled",height=18,width=50,command=self.button_play)
        self.bplay.bind("<Leave>",self.leaveplayhover)
        self.bplay.bind("<Enter>",self.enterplayhover)
        self.playWindow=self.atelier.create_window((self.mainWidth//2)-32,self.frame.winfo_height()+ self.positionboardy+36,anchor=NW,window=self.bplay)
        self.iprev=PhotoImage(file="Images/Buttons/prev_29x20.png")
        self.bprev=tk.Button(text="PREV",image=self.iprev,state= "disabled",borderwidth=4,compound="top",width=40, height=36,command=self.button_prev)
        self.inext=PhotoImage(file="Images/Buttons/next_29x20.png")
        self.bnext=tk.Button(text="NEXT",image=self.inext,state="disabled",borderwidth=4,compound="top",width=40, height=36,command=self.button_next)
        self.prevWindow=self.atelier.create_window((self.mainWidth//2)-190,self.frame.winfo_height()+ self.positionboardy+18,anchor=NW,window=self.bprev)
        self.nextWindow=self.atelier.create_window((self.mainWidth//2)+134,self.frame.winfo_height()+ self.positionboardy+18,anchor=NW,window=self.bnext)
        self.banswer=tk.Button(text="Answer",image=self.ianswer, compound="left",state="disabled",borderwidth=4,bg="#ff928b",activebackground="#772e25", width=65, height=18,justify="center", font=('Arial',10), command=self.button_answer)
        self.checkWindow=self.atelier.create_window((self.mainWidth//2)-130,self.frame.winfo_height()+ self.positionboardy+85,anchor=NW,window=self.banswer)
        self.banswer.bind("<Enter>",self.enterahover)
        self.banswer.bind("<Leave>",self.leaveahover)
        self.bcheck=tk.Button(text="Check", image=self.icheck,compound="left",state="disabled",borderwidth=4,bg="#99d98c",width=65,height=18,activebackground="#4c956c", justify="center", font=('Arial',10), command=self.button_check)
        self.checkWindow=self.atelier.create_window((self.mainWidth//2)+50,self.frame.winfo_height()+ self.positionboardy+85,anchor=NW,window=self.bcheck)
        self.bcheck.bind("<Enter>",self.enterhover)
        self.bcheck.bind("<Leave>",self.leavehover)
        self.bclear=tk.Button(text="Clear", image=self.iclear,compound="left",state="disabled",borderwidth=4,bg="#f5dd90",activebackground="#d08c60", justify="center",width=65,height=18, font=('Arial',10),command=self.button_clear)
        self.clearWindow=self.atelier.create_window((self.mainWidth//2)-40,self.frame.winfo_height()+ self.positionboardy+85,anchor=NW,window=self.bclear)
        self.bclear.bind("<Enter>",self.enterclearhover)
        self.bclear.bind("<Leave>",self.leaveclearhover)
        self.bstats=tk.Button(image=self.istats,text=" STATS",borderwidth=2,compound="left", height=20,width=60,state="disabled",command=self.button_stats)
        self.statsWindow=self.atelier.create_window(5,5,anchor=NW,window=self.bstats)
        self.bstats.bind("<Enter>",self.enterstatshover)
        self.bstats.bind("<Leave>",self.leavestatshover)
        self.bsave=tk.Button(image=self.isave,text=" SAVE",borderwidth=2,compound="left",height=20,width=60,state="normal",command=self.button_save)
        self.saveWindow=self.atelier.create_window(77,5,anchor=NW,window=self.bsave)
        self.bsave.bind("<Enter>",self.entersavehover)
        self.bsave.bind("<Leave>",self.leavesavehover)
        self.lclock=tk.Label(text=self.initc,font=("Helvetica",15),fg="red",bg="black")
        self.clockWindow=self.atelier.create_window((self.mainWidth//2)-45,self.frame.winfo_height()+ self.positionboardy+128,anchor=NW,window=self.lclock)
        self.initFtree()
        self.levelsdone=self.loadGame()
        self.fPlay=1
        self.savedt="Game saved"
        self.flaglevstate=0
    
    #Function that initializes the table/filetree with its columns and rows
    def initFtree(self):
        self.file_Tree['columns']=("City","Completed in", "Times checked", "Answer required")
        self.file_Tree.column("#0",width=35,minwidth=25,anchor=W)
        self.file_Tree.column("City",width=90,minwidth=25,anchor=W)
        self.file_Tree.column("Completed in",width=60,minwidth=25,anchor=CENTER)
        self.file_Tree.column("Times checked",width=60,minwidth=25,anchor=CENTER)
        self.file_Tree.column("Answer required",width=60,minwidth=25,anchor=CENTER)
        self.file_Tree.heading("#0",text="Level", anchor=W)
        self.file_Tree.heading("City",text="City",anchor=W)
        self.file_Tree.heading("Completed in",text="Time",anchor=W)
        self.file_Tree.heading("Times checked",text="N° checks",anchor=W)
        self.file_Tree.heading("Answer required",text="Answer",anchor=W)
        self.initPlayMusic()
        self.getUserName()

    #Function to get a widget dimension
    def getWidDimensions (self,widget):
        width=widget.winfo_width()
        heigth=widget.winfo_height()
        return width, heigth
        
    #Function to get the player's name for the game
    def getUserName(self):
            self.username=simpledialog.askstring("Player Setup","Enter your name",parent=self.root)
            if (self.username==None):
                self.username="Player1"
            self.habilitateBtn(self.bplay,1)
        
    #Function that inits the music tracks
    def initPlayMusic(self): 
        pygame.mixer.init()
        pygame.display.init()
        pygame.mixer.music.load(self.musicl[0])
        pygame.mixer.music.queue(self.musicl[1])
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
    
    #Function linked to button stats
    def button_stats(self): 
        self.openFile("statistics.txt")
        textFl=self.readFile()
        for i in self.file_Tree.get_children():    
            self.file_Tree.delete(i)
        for x in range (0,len(textFl)):
            laux=textFl[x].split(";")
            self.file_Tree.insert(parent='',index='end',iid=x,text=str(x+1),values=(self.cityl[int(laux[0])-1],laux[1],laux[2],laux[3]))
            
        self.atelier.itemconfigure(self.fileTreeWindow,state='normal')
        self.closeFile() 
       
    #Custom function to open a file
    def openFile(self, path): 
        try:
            self.statsFile=open(path,"a+",encoding='utf8')
        except Exception as e:
            self.statsFile=open(path,"a+",encoding="utf8")
    
    #Custom function to close a file
    def closeFile(self):
        self.statsFile.close()

    #Custom function to read a file
    def readFile(self):
        try:
            self.statsFile.seek(0,0)
            self.contentFile=self.statsFile.readlines()
            print("contentfile")
            print(self.contentFile)
            return self.contentFile
        except Exception as e:
            if(DEBUG==1):
                print("Exception {} occurred".format(e))
    
    #Function linked to button save
    def button_save(self):
        self.saveGame()
        self.saveText=self.atelier.create_text(185,20,text=self.savedt,font=("Monotype Corsiva",15),fill="white")
        colorThd=threading.Thread(name="color",target=self.change_Color)
        colorThd.start() #Thread that changes color of "saved"
       
    def change_Color(self):
        flagcolor=0
        i=0
        n=8
        while(i<n):
            if (flagcolor==0):
                self.atelier.itemconfig(self.saveText,fill="red")
                flagcolor=1
            else:
                self.atelier.itemconfig(self.saveText,fill="white")
                flagcolor=0

            time.sleep(0.50)
            i+=1
        self.atelier.itemconfig(self.saveText,state="hidden")

    #Function that writes a file to save game state
    def saveGame(self):
        self.saveFile=open("archivo.save","w")
        l=self.levelsdone.copy()
        for i in range(0, len(l)):
            if(i!=len(l)-1):
                l[i]= str(l[i])+ '\n'
            else:
                l[i]= str(l[i])
        self.saveFile.writelines(l)
        self.saveFile.close()
    
    #Function that loads the saved game
    def loadGame(self):
        try:
            self.saveFile=open("archivo.save","r")
            self.savel=self.saveFile.readlines()
            i=0  
            for item in self.savel:
                if (int(item) ==0):
                    self.loadLevel(i)  
                    break
                i+=1
        except:
            self.savel=['0','0','0','0','0','0','0','0','0','0','0','0','0','0']
        
        return([int(x) for x in self.savel])
    
    #Function that loads the saved level
    def loadLevel(self,i):
        current_level=i
        self.loadinitialCity(i)
        self.changeScenary()
        self.habilitateBtn(self.bprev,1)
        self.habilitateb()

    #Function that loads the city according to level
    def loadinitialCity(self,j): 
        sl="Level"
        new_text=sl + " " + str(j+1) + " " + ":" + " " + self.cityl[j]
        self.atelier.itemconfigure(self.tlevel,font=self.fontsl[j])
        self.atelier.itemconfigure(self.tlevel,text=new_text)
        if(j==2 or j==0):
            self.atelier.itemconfig(self.tlevel,fill='#edf6f9')
        else:
            self.atelier.itemconfig(self.tlevel,fill='#000000')

    #Custom function to write a file          
    def writeFile(self):
        listitem=[]
        listitem.append(str(self.get_glevel()))
        listitem.append(self.lclock.cget("text"))
        listitem.append(str(self.checkcounter))
        answers=""
        if(self.countanswer==0):
            answers="No"
        else:
            answers="Yes"
        listitem.append(answers)
        wstr=";".join(listitem)
        self.statsFile.write(wstr+ '\n')
        self.statsFile.close()

    #Function to make a sequence of images animated(gif)
    def gifSequence(self):
        if (debug!=1):
            self.habilitateBtn(self.bnext,0)
        global numberseq
        path="Images/Gif/firework-sequence"
        path2="Images/Gif/firework-sequence2"
        imgs=glob.glob(path +'/*.png')
        imgs2=glob.glob(path2 +'/*.png')
        while(numberseq<3):        
            for i in range (0,len(imgs)):
                self.imagegif=PhotoImage(file=imgs[i])
                self.atelier.create_image(100,130,image=self.imagegif,anchor=NW,tags="im")
                self.imagegif2=PhotoImage(file=imgs2[i])
                self.atelier.create_image(800,50,image=self.imagegif2,anchor=NW,tags="im")
                time.sleep(0.15)
                self.atelier.delete("im")
            numberseq+=1
        if (numberseq==3):
            numberseq=0
        
    #Function to play fireworks sound
    def playfw(self):
        pygame.mixer.set_num_channels(15)
        sound2 = pygame.mixer.Sound("Sounds/Effects/FireWorks.mp3")
        pygame.mixer.find_channel().play(sound2)
           
    def fail(self):
        sound2 = pygame.mixer.Sound("Sounds/Effects/FailTrombone.mp3")
        pygame.mixer.find_channel().play(sound2)

#Function that returns the name of reproducing track
    def trackName(self):
        sp1=self.musicl[self.indexm].split("-")
        sp2=sp1[1].split(".")
        return sp2[0]
    
#Function that writes the track name in the music panel
    def writeTrack(self):
        self.atelier.itemconfig(self.ttrackName,text="\" "+self.trackName()+"\'\"")

#Function to close program according to user's decision
    def on_closing(self):
        self.response=tk.messagebox.askyesno("Exit Menu","Are you sure you want to quit?")
        if self.response ==1:
            pygame.mixer.music.stop()
            self.root.destroy()
    
    
    #Function linked to button playmusic
    def button_playMusic(self):
        self.isStopped=0
        self.selectRepState(1)

        if (self.isPaused==0):
            pygame.mixer.music.play(0)
            self.writeTrack()
        else:
            pygame.mixer.music.unpause()
        
        self.isPaused=0
    
    #Function to enable or disable buttons
    def habilitateBtn(self,btn,state): 
        if(state==1):
            btn["state"]=tk.NORMAL
        else:
            btn["state"]=tk.DISABLED

#Function that manages the music reproduction state of music buttons
    def selectRepState(self,repstate):
        if(repstate==0):
            self.habilitateBtn(self.bstopM,0)
            self.habilitateBtn(self.bplayM,1)
            self.habilitateBtn(self.bpauseM,0)
        elif(repstate==1):
            self.habilitateBtn(self.bstopM,1)
            self.habilitateBtn(self.bplayM,0)
            self.habilitateBtn(self.bpauseM,1)

    #Function that changes the city scenary (photo)
    def changeScenary(self):
        self.scenei=PhotoImage(file=self.scenel[self.get_glevel()])
        self.atelier.itemconfig(self.currentscene,image=self.scenei)   

    #Function linked to pausemusic button
    def button_pauseMusic(self):
        pygame.mixer.music.pause()
        self.isPaused=1
        self.selectRepState(0)

    #Function linked to stopmusic button
    def button_stopMusic(self):
        self.selectRepState(0)
        self.isStopped=1
        pygame.mixer.music.stop()
    
    #Function that initializes the game in DEBUG mode
    def debug_initialize(self):
        if (self.flag_isStarted== False):
            self.habilitateBtn(self.banswer,0)
            self.habilitateBtn(self.bcheck,0)
            self.habilitateBtn(self.bclear,0)
        else:
            self.define_Newlevel()
            self.habilitateBtn(self.banswer,1)
            self.habilitateBtn(self.bcheck,1)
            self.habilitateBtn(self.bclear,1)
            self.habilitateBtn(self.bplay,self.fPlay)
            self.running=True
            time.sleep(0.25)
            self.initial_Values(self.wrotemapl[self.get_glevel()-1])
            self.auto_completed(self.solutionsl[self.get_glevel()-1])
            
    #Function to autocomplete the board
    def auto_completed(self,s):
        flatlist=sum(s,[])
        for x in range (0, len(flatlist)): 
                self.elist[x].insert(0,flatlist[x])
                
    def initialize(self):
        if (self.flag_isStarted== False):
            self.habilitateBtn(self.banswer,0)
            self.habilitateBtn(self.bcheck,0)
            self.habilitateBtn(self.bclear,0)
        else:
            self.define_Newlevel()
            self.habilitateBtn(self.banswer,1)
            self.habilitateBtn(self.bcheck,1)
            self.habilitateBtn(self.bclear,1)
            self.habilitateBtn(self.bplay,self.fPlay)
            self.running=True
            time.sleep(0.25)
            self.initial_Values(self.wrotemapl[self.get_glevel()-1])
            #self.auto_completed(self.solutionsl[self.get_glevel()-1])

    #Function to define a new level
    def define_Newlevel(self):
        new_level=self.get_glevel()
        if (new_level==0):
            self.atelier.itemconfigure(self.tlevel,font=self.fontsl[0])
            self.atelier.itemconfig(self.tlevel,text='Level 1 : Buenos Aires',fill="#edf6f9")
            self.changeScenary()
    
    #Function that blanks the sudoku's board
    def blankmap(self): 
        for x in self.elist:
            x.configure(state="normal")
            x.delete(0,tk.END)
    
    #Function to initialize previous level
    def init_blevel(self):
        self.habilitateBtn(self.banswer,1)
        self.habilitateBtn(self.bcheck,1)
        self.habilitateBtn(self.bclear,1)
        self.habilitateBtn(self.bplay,self.fPlay)
        self.resetClock()

        if(debug==1):
           self.auto_completed(self.solutionsl[self.get_glevel()-1])

      
    #Function to set initial level
    def initialLevel(self):
        self.habilitateBtn(self.bcheck,1)
        self.habilitateBtn(self.bclear,1)
        self.habilitateBtn(self.banswer,1)
        self.habilitateBtn(self.bplay,self.fPlay)
        self.resetClock()
        self.isLevelUp=False
        self.lpassed=0
        self.running=True
        self.tflag=True
        self.sclock()
        #self.auto_completed(self.solutionsl[self.get_glevel()-1])

        if(debug==1):
            self.auto_completed(self.solutionsl[self.get_glevel()-1])

    #Function for entering check button (tooltip)
    def enterhover(self,e): 
        self.atelier.itemconfig(self.trect,text="Board must be full to check")
    
    #Function for leaving check button(tooltip)
    def leavehover(self,e): 
        self.atelier.itemconfig(self.trect,text=self.username + " " +self.today)
    
    #Function for entering stats button(tooltip)
    def enterstatshover(self,e): 
        self.atelier.itemconfig(self.trect,text="Click after level completion to view game statistics")

    #Function for leaving stats button(tooltip)
    def leavestatshover(self,e): 
        self.atelier.itemconfig(self.trect,text=self.username + " "+self.today)
    
    
    #Function for entering save button(tooltip)
    def entersavehover(self,e): 
        self.atelier.itemconfig(self.trect,text="Click to save game")
    
    #Function for leaving save button(tooltip)
    def leavesavehover(self,e): 
        self.atelier.itemconfig(self.trect,text= self.username +" " +self.today)
    
        
    #Function for entering clear button(tooltip)
    def enterclearhover(self,e): 
        self.atelier.itemconfig(self.trect,text="This will automatically clear Sudoku's board")
    
    #Function for leaving clear button(tooltip)
    def leaveclearhover(self,e): 
        self.atelier.itemconfig(self.trect,text=self.username +" " +self.today)
    
    #Function for entering play button(tooltip)
    def enterplayhover(self,e): 
        self.atelier.itemconfig(self.trect,text="GOOD LUCK"+ " " + self.username.upper() +"!")
    
    #Function for leaving play button(tooltip)
    def leaveplayhover(self,e): 
        self.atelier.itemconfig(self.trect,text=self.username +" " +self.today)
    
    #Function for entering answer button (tooltip)
    def enterahover(self,e): 
        self.atelier.itemconfig(self.trect,text="Asking for answer will automatically disable Bonus")
    
    #Function for leaving answer button (tooltip)
    def leaveahover(self,e): 
        self.atelier.itemconfig(self.trect,text= self.username +" " +self.today)
  
    #Function for entering prev button
    def prevehover(self,e):
        self.atelier.itemconfig(self.trect,text="No more levels availables")

    #Function for leaving prev button
    def prevlhover(self,e):
       self.atelier.itemconfig(self.trect,text=self.today)
    
    #Function for entering next button
    def nextehover(self,e):
        self.atelier.itemconfig(self.trect,text="if completed and not failed levels, bonus will be available")
    
    #Function for leaving next button
    def nextlhover(self,e):
        self.atelier.itemconfig(self.trect,text=self.today)
        
    #Function that creates the sudoku's board
    def make_Board(self):
        contr=1 #Counter for rows
        contc=1 #Counter for columns
        
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
    
    #Function that set the dimensions of root acording to screen
    def setGeometry(self):
        auxWidth=1366
        auxHeight=700
        self.root.update()
        self.mainHeight=self.root.winfo_height()
        self.mainWidth=self.root.winfo_width()
        if(auxWidth>= self.mainWidth): #Fix the resolution for different screen sizes
            self.mainWidth=self.root.winfo_width()
            
        else:
            self.mainWidth=auxWidth
        
        if(auxHeight>= self.mainHeight):
            self.mainHeight=self.root.winfo_height()
            
        else:
            self.mainHeight=auxHeight

        self.fullScreenState = False
        self.root.attributes("-fullscreen", self.fullScreenState)
        self.positionRight = int(self.root.winfo_screenwidth()/2 - int(self.mainWidth)/2)
        self.positionDown = int(self.root.winfo_screenheight()/2 - int(self.mainHeight)/2)
        self.root.geometry("{}x{}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        
        print("esto es el alto {}".format (self.mainHeight))
        print("ahora viene el ancho{}".format(self.mainWidth))
    #Timer to determine tracks and if entries are correct
    def verify_Timer(self):
        if(self.response!=1):
            for event in pygame.event.get():
                if (event.type == pygame.USEREVENT):
                    self.track+=1
                    self.indexm+=1
                    if (self.isStopped!=1):
                        self.writeTrack()
                    else:
                        self.indexm=0
                        self.atelier.itemconfig(self.ttrackName,text="")
                    if(len(self.musicl)>self.track):
                        pygame.mixer.music.queue (self.musicl[self.track] )
                    else:
                        self.reinitMusic()    
        
            if (self.tflag==True):
                self.verify_Bentry()
                self.is_completed()
            if (not cancel_tmr):
                threading.Timer(0.25,self.verify_Timer).start()

    #Function to restart music
    def reinitMusic(self):
        self.track=0
        pygame.mixer.music.queue(self.musicl[self.track] )
    
    #Function that takes care of flashing of screen in case of erroneous entries in the board
    def twinkling(self):
        self.count+=1 #Counter for times blinking
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
                self.isLevelUp=True
                self.openFile("statistics.txt")
                filevar=self.readFile()
                listvar=[]
                levellist=[]
                for x in filevar:
                    listvar= x.split(";")
                    levellist.append(int(listvar[0]))
                
                elem=levellist.count(self.get_glevel())
                if (elem<1):
                    self.writeFile()
                self.closeFile()  
                if(self.flaglevstate==0 and debug!=1):
                    thGseq=threading.Thread(name="tgifseq",target=self.gifSequence)
                    thGseq.start()
                    thFwsong=threading.Thread(name="tfireworks",target=self.playfw)
                    thFwsong.start()
                    time.sleep(14)
                
                self.initialize()
                self.levelsdone[self.get_glevel()-1]=1
                self.habilitateBtn(self.bstats,1)
                if (self.lpassed==0):
                    self.habilitateBtn(self.bnext,1)
                else:
                    self.habilitateBtn(self.bnext,0)
                self.habilitateb()
                if(self.flaglevstate==0):
                    self.atelier.itemconfig(self.ltfailed,state="hidden")
                    self.atelier.itemconfig(self.ltcompleted,state="normal")
                    self.flaglevstate=0

    def habilitateb(self):
        if(self.countanswer==0):
            self.bonusflag=True
        else:
            self.bonusflag=False
        if(self.get_glevel()==13 and self.bonusflag==False):
            self.habilitateBtn(self.bnext,0)
            self.bnext.bind("<Enter>",self.nextehover)
            self.bnext.bind("<Leave>",self.nextlhover)
        
        if(self.get_glevel()==14):
            self.habilitateBtn(self.bnext,0)

    #Function that gets the int value of the current level 
    def get_glevel(self): 
        texts=self.atelier.itemcget(self.tlevel,"text")
        self.textl=texts.split()
        self.textn= int(self.textl[1])
        return self.textn
    
    #Setter of game level
    def set_glevel(self,x):
        self.textn=x #Game level int
    
    #Function that increases a level  
    def next_level(self): 
        current_level=self.get_glevel()
        if(current_level<14 and self.lpassed==0):
            self.lpassed=1
            self.set_glevel(current_level +1)
            self.LevelUp()
            self.checkdones()
   
   #Function that decreases a level
    def prev_level(self): 
        current_level=self.get_glevel()-1
        self.set_glevel(current_level)
        if (current_level >=1):
            self.lback=1
            self.LevelDown()
            if(current_level==1):
                self.habilitateBtn(self.bprev,0)
                self.bprev.bind("<Enter>",self.prevehover)
                self.bprev.bind("<Leave>",self.prevlhover)
                
    #Function to go back(levels)
    def LevelDown(self):
        self.define_prevcity()
        self.changeScenary()
        self.blankmap()
        self.checkdones()
        self.initial_Values(self.wrotemapl[self.get_glevel()-1])
        self.init_blevel()

    #Function to define previous city when going back
    def define_prevcity(self):
        lvel=self.get_glevel()-1
        for i in range (0, len(self.cityl)):
            if (i==lvel):
                self.atelier.itemconfig(self.tlevel,text="")
                sl="Level"
                new_text=sl + " " + str(i) + " " + ":" + " " + self.cityl[i-1]
                self.atelier.itemconfigure(self.tlevel,font=self.fontsl[i-1])
                self.atelier.itemconfig(self.tlevel,text=new_text)
                if(lvel==1 or lvel==3 or lvel==4 or lvel==7 or lvel==11 or lvel==13):
                    self.atelier.itemconfig(self.tlevel,fill='#edf6f9')
                else:
                    self.atelier.itemconfig(self.tlevel,fill='#000000')
                break
    
    #Getter of isLevelUp variable
    def get_isLevelUp(self): 
        return self.isLevelUp

    #Function to define level up actions
    def LevelUp (self):
            self.define_cities()
            self.changeScenary()
            self.blankmap()
            self.initial_Values(self.wrotemapl[self.get_glevel()-1])
            self.habilitateb()
            if(self.lpassed==0):
                self.habilitateBtn(self.bnext,1)
            else:
                self.habilitateBtn(self.bnext,0)
            self.initialLevel()  
            self.hback()
    
    #Function that checks levels completed
    def checkdones(self):
        if(self.eventprev==1):
            if(self.levelsdone[self.get_glevel()-1]==1):
                self.habilitateBtn(self.bnext,1)
                
        elif(self.eventnext==1):
            if(self.levelsdone[self.get_glevel()-1]==1):
                self.habilitateBtn(self.bnext,1)

    #Function that configurates button prev
    def hback(self):
        self.habilitateBtn(self.bprev,1)

    #Function thet initializes the sudoku according to the level
    def initial_Values(self,a): 
        flatlist=sum(a,[])
        for x in range (0, len(flatlist)): 
            if(flatlist[x]!=0):
                self.elist[x].configure(state="normal")
                self.elist[x].insert(0,flatlist[x])
                self.elist[x].configure(state="disabled")
            else:
                self.elist[x].configure(state="normal")
                self.elist[x].insert(0,"")

    #Function that verifies if entries are valid.If not, they are painted red
    def verify_Bentry(self): 
        if self.response!=1:
            lsnum=["0","1","2","3","4","5","6","7","8","9",""]
            for elem in self.elist:           
                xtext=elem.get()
                if (xtext not in lsnum):
                    elem.config({"fg":"Red"})
                else:
                    elem.config({"fg":"Black"})
    
    #Function linked with bplay
    def button_play(self):
        self.fPlay=0
        self.flag_isStarted=True
        self.playcount+=1
        if (debug ==0):
            self.initialize()
        else:
            self.debug_initialize()
        
    #Function linked with bclear
    def button_clear(self):
        self.hour=0
        self.minute=0
        self.second=0
        self.tflag=True #Flag for entry verification process
        for x in self.elist:
            bstate= x.cget('state')
            if (bstate=="normal"):
                x.delete(0,tk.END)
        
        self.lclock.config(text=self.initc)
    
    #Function linked with banswer
    def button_answer(self):
        thFail=threading.Thread(name="tfail",target=self.fail)
        thFail.start()
        self.flaglevstate=1
        self.countanswer+=1
        self.bcheck.bind("<Enter>",self.leavehover)
        self.running=False
        self.atelier.itemconfig(self.ltfailed,state="normal")
        flatlist=sum(self.solutionsl[self.textn -1],[])
        self.tflag=False
        for x in range (0, len(self.elist)):
            bstate=self.elist[x].cget("state")
            self.elist[x].config(foreground="#d00000")
            if (bstate!="disabled"):
                self.elist[x].delete(0,tk.END)
                self.elist[x].insert(0,flatlist[x])
            else:
                continue
        self.lclock.config(text=self.initc)
        
    #Function that checks if the sudoku's entries are full
    def is_completed(self):
        scontentl=[]
        for x in self.elist:
            bstate= x.cget('state')
            if (bstate =="normal"):
                content=x.get()
                scontentl.append(content)
        
        if (self.flag_isStarted==True):
            if (any(x=="" for x in scontentl)):
                self.habilitateBtn(self.bcheck,0)
            else:
                self.habilitateBtn(self.bcheck,1)

    #Function linked with bprev
    def button_prev(self):
        self.atelier.itemconfig(self.fileTreeWindow,state="hidden")
        self.habilitateBtn(self.bstats,1)
        self.eventprev=1
        self.prev_level()
        self.eventprev=0

    #Function linked with bnext
    def button_next(self):
        self.habilitateBtn(self.bstats,0)
        self.atelier.itemconfig(self.fileTreeWindow,state="hidden")
        self.eventnext=1
        self.atelier.itemconfig(self.ltfailed,state="hidden")
        self.atelier.itemconfig(self.ltcompleted,state="hidden")
        self.next_level()
        self.habilitateb()
        self.eventnext=0
        
        
    #Function linked with bcheck
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
            self.pwindow.iconbitmap("Images/Ornate/hourglass.ico")
            self.pbar=ttk.Progressbar(self.pwindow,orient=HORIZONTAL,length=200,mode="indeterminate")
            self.pbar.place(relx=0.5,rely=0.5,anchor="center")
            self.pwindow.geometry('250x50+600+300' )
            self.pwindow.resizable(False,False)
            thpbar=threading.Thread(name="tpbar",target=self.run_progressBar)
            thpbar.start()
        else:
            self.running= True
            self.twinkling()
    
    #Function that handles the progressbar and timer during checking
    def run_progressBar (self):
        self.pbar.start(10)
        threading.Timer(5,self.timeout).start()
        time.sleep(5)
    
    #Function that stops the progress bar and proceed with the blinking of erroneous entries
    def timeout(self):
        self.pbar.stop()
        self.running=True
        self.twinklingThread()
        self.pwindow.destroy()
      
    #Function linked to blinking
    def twinklingThread(self):
        self.t3=threading.Thread(name="tblink",target=self.twinkling)
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
        
        #String format to include leading zeros
        shour= f'{self.hour}' if self.hour >9 else f'{self.hour}'
        sminute= f'{self.minute}' if self.minute >9 else f'{self.minute}'
        ssecond= f'{self.second}' if self.second >9 else f'{self.second}'

        self.lclock.config(text=shour + ":" + sminute + ":" + ssecond)
        if (self.isLevelUp==False):
            self.lclock.after(1000,self.sclock)
    
    #Function that resets clock values to zero
    def resetClock(self):
        self.hour=0
        self.minute=0
        self.second=0

    #Function that defines the city according to each level
    def define_cities(self): 
        for i in range (0, len(self.cityl)):
            n=i+1
            if (n==self.get_glevel()):
                self.atelier.itemconfigure(self.tlevel,text="")
                sl="Level"
                new_text=sl + " " + str(n+1) + " " + ":" + " " + self.cityl[i+1]
                self.atelier.itemconfigure(self.tlevel,font=self.fontsl[i+1])
                self.atelier.itemconfigure(self.tlevel,text=new_text)
                if(n==2 or n==3 or n==6 or n==10 or n==12):
                    self.atelier.itemconfig(self.tlevel,fill='#edf6f9')
                else:
                    self.atelier.itemconfig(self.tlevel,fill='#000000')

                break
            
def main(): 
    root= tk.Tk()
    sud1= Drawing(root)
    sud1.sclock()
    sud1.verify_Timer()
    root.mainloop()


if __name__ == '__main__':
    main()
    
    



