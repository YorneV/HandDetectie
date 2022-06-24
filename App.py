import tkinter as tk
from tkinter import font,colorchooser
from win32api import GetSystemMetrics
import keyboard as kb
import numpy as np
import cv2
from PIL import Image as Im


class Select(tk.Canvas):
    def __init__(self):
        self.Points = {}
        self.Index = 0
        self.curPoints = []
        self.x, self.y = None, None
        self.lineWidth = 1
        self.lineColor = '#ffffff'
        tk.Canvas.__init__(self,width=GetSystemMetrics(0),height=GetSystemMetrics(1),bg='#3b3535',border=0)
        #self.bind("<Button-2>",self.save)
        self.bind("<Button-1>",self.createIndex)
        self.bind("<Button-3>",self.delPoint)
        self.bind("<B1-Motion>", self.drawLine)
        self.bind('<ButtonRelease-1>',self.isIdle)
        #Rand
        self.topBar = tk.Message(self,bg='#2b2727',text='MS Paint maar beter',fg='#ffffff')
        leftBar = tk.Message(self,bg='#2b2727')
        rightBar = tk.Message(self,bg='#2b2727')
        bottomBar = tk.Message(self,bg='#2b2727')
        self.topBar.place(x=0,y=0,height=80,width=GetSystemMetrics(0))
        bottomBar.place(x=0, y=GetSystemMetrics(1)-10,height=10,width=GetSystemMetrics(0))
        leftBar.place(x=0,y=80,height=GetSystemMetrics(1),width=30)
        rightBar.place(x=GetSystemMetrics(0)-30,y=80,height=GetSystemMetrics(1),width=30)
        #Scherm = (sys - 2*30 , sys - (80 + 10)) = (1476 , 774)
        #Knoppekes
        buttonQuit = tk.Button(self.topBar,bg='#3b3535',text="Quit & Don't Save", command=self.quit, fg='#ffffff')
        buttonQuit.place(x=15,y=15,height=50,width=120)
        buttonSave = tk.Button(self.topBar,bg='#3b3535',text="Save", command=self.save, fg='#ffffff')
        buttonSave.place(x=15*2+120,y=15,height=50,width=60)
        buttonWidth1 = tk.Button(self.topBar,bg='#3b3535',text='|', command=lambda: self.changeWidth('1'), fg='#ffffff',font=font.Font(size=12))
        buttonWidth1.place(x=15*3+120+60,y=15,height=20,width=40)
        buttonWidth2 = tk.Button(self.topBar,bg='#3b3535',text='|', command=lambda: self.changeWidth('3'), fg='#ffffff',font=font.Font(size=32))
        buttonWidth2.place(x=15*4+120+60+40,y=15,height=20,width=40)
        buttonWidth3 = tk.Button(self.topBar,bg='#3b3535',text='|', command=lambda: self.changeWidth('5'), fg='#ffffff',font=font.Font(size=52))
        buttonWidth3.place(x=15*3+120+60,y=15+10+20,height=20,width=40)
        buttonWidth4 = tk.Button(self.topBar,bg='#3b3535',text='|', command=lambda: self.changeWidth('7'), fg='#ffffff',font=font.Font(size=72))
        buttonWidth4.place(x=15*4+120+60+40,y=15+10+20,height=20,width=40)
        buttonColor1 = tk.Button(self.topBar,bg='#3b3535',text='•', command=lambda: self.changeColor(), fg='#02c98e',font=font.Font(size=90))
        buttonColor1.place(x=15*5+120+60+40*2,y=15,height=50,width=50)
        self.message = tk.Message(master=self.topBar,bg='#3b3535',text='Welcome!', fg='#ffffff',justify=tk.LEFT,width=285)
        self.message.place(x=(GetSystemMetrics(0) - 315),y=15,height=50,width=285)

    def changeWidth(self,width):
        self.lineWidth = int(width)

    def changeColor(self):
        self.lineColor = colorchooser.askcolor(title ="Choose color.")
        print('color',self.lineColor)
        self.lineColor = self.lineColor[1]

    def quit(self):
        exit()

    def isIdle(self,_):
        self.message.destroy
        self.message = tk.Message(master=self.topBar,bg='#3b3535',text='Idle...', fg='#ffffff',justify=tk.LEFT,width=285)
        self.message.place(x=(GetSystemMetrics(0) - 315),y=15,height=50,width=285)

    def sendFeedback(self,input):
        self.message.destroy
        self.message = tk.Message(master=self.topBar,bg='#3b3535',text=input, fg='#ffffff',justify=tk.LEFT,width=285)
        self.message.place(x=(GetSystemMetrics(0) - 315),y=15,height=50,width=285)

    def save(self):
        self.sendFeedback('Saving...')
        newImage = np.zeros([865 , 1537], np.uint8)
        points = []
        for key in self.Points:
            points.extend(self.Points[key])
        for teller in range(len(points)-1):
            newImage[points[teller][1]][points[teller][0]] = 255
        try:
            im = Im.fromarray(newImage)
            im.save("Drawn.png",'png')
            self.sendFeedback('Saved!')
        except:
            self.sendFeedback('Failed to save!')
            pass

    def createIndex(self,event):
        self.sendFeedback('Drawing Line...')
        self.Index += 1
        self.updatePoint(event)
        if len(self.curPoints) != 0:
            self.submitPoints()
    
    def submitPoints(self):
        self.Points[str(self.Index)] = self.curPoints

    def updatePoint(self,event):
        self.curPoints.append((event.x,event.y))
        self.x, self.y = event.x, event.y

    def drawLine(self,event):
        self.create_line(self.x, self.y, event.x, event.y, tags='a'*self.Index,fill=self.lineColor,width=self.lineWidth)
        self.updatePoint(event)

    def delPoint(self,_):
        self.sendFeedback('Deleted previous line.')
        self.delete('a'*self.Index)
        if len(self.Points) != 0:
            self.Points.pop(str(self.Index))
        self.Index = max(0, self.Index - 1)
    
    def drawArea(self,_):
        print('here')
        points = []
        for key in self.Points:
            points.extend(self.Points[key])
        self.create_polygon(xy_pairs=points)

window = tk.Tk()
#window.state('zoomed')
window.attributes('-fullscreen',True,'-alpha',1,'-topmost',False)
run = Select()
run.pack()
#print(GetSystemMetrics(0),GetSystemMetrics(1))
window.mainloop() 