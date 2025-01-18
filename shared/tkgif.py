##Author: Shantanu gupta
##This short script helps to display GIF in tkinter label
##note: missing pause gif function
import _thread
from tkinter import *
import time
class gifplay:
    """
    Usage: mygif=gifplay(<<tkinter.label Objec>>,<<GIF path>>,<<frame_rate(in ms)>>)
    example:
    gif=GIF.gifplay(self.model2,'./res/neural.gif',0.1)
    gif.play()
    This will play gif infinitely
    """
    def __init__(self,label,giffile,delay):
        self.frame=[]
        i=0
        while 1:
            try:
                image=PhotoImage(file = giffile, format="gif -index "+str(i))
                self.frame.append(image)
                i=i+1
            except:
                break
        print(i)
        self.totalFrames=i-1
        self.delay=delay
        self.labelspace=label
        self.labelspace.image=self.frame[0]

    def play(self):
        """
        plays the gif
        """
        _thread.start_new_thread(self.infinite,())

    def infinite(self):
        i=0
        while 1:
            self.labelspace.configure(image=self.frame[i])
            i=(i+1)%self.totalFrames
            time.sleep(self.delay)