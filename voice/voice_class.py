import sys
import os
import time
from playsound import playsound as play
class VoiceInterface(object):

  def __init__(self, straight_file = 'straight.mp3',
                     turnleft_file = 'turnleft.mp3',
                     turnright_file = 'turnright.mp3',
                     hardleft_file = 'hardleft.mp3',
                     hardright_file = 'hardright.mp3',
                     STOP_file = 'STOP.mp3',
                     noway_file = 'noway.mp3'):
    self.straight_file= straight_file
    self.turnleft_file= turnleft_file
    self.turnright_file=turnright_file
    self.hardleft_file=hardleft_file
    self.hardright_file=hardright_file
    self.STOP_file=STOP_file
    self.noway_file=noway_file

    self.prev_path = None

  def play(self, pat, width):
    b=10
    center=width/2-0.5
    if len(pat)==0:
        play(self.noway_file)
        time.sleep(0.7)
        return
    path=[]
    path.append(pat[0]-center)
    for i in range (1,len(pat)):
        path.append(pat[i]-pat[i-1])
    print(path)
    for step in path:
        if step == 1 and step!=b:
            play(self.turnleft_file)
        if step == 2 and step!=b:
            play(self.hardleft_file)
        if step == -1 and step!=b:
            play(self.turnright_file)
        if step == -2 and step!=b:
            play(self.hardright_file)
        if step == 0 and step!=b:
            play(self.straight_file)
        b=step
        time.sleep(0.7)
    play(self.STOP_file)
  def play1(self, pat, width):
    center=width/2-0.5
    if len(pat)==0:
        play(self.noway_file)
        time.sleep(0)
        return
    path=[]
    path.append(pat[0]-center)
    for i in range (1,len(pat)):
        path.append(pat[i]-pat[i-1])
    print(path)
    for step in path:
        if step == 1:
            play(self.turnleft_file)
        if step == 2:
            play(self.hardleft_file)
        if step == -1:
            play(self.turnright_file)
        if step == -2:
            play(self.hardright_file)
        if step == 0:
            play(self.straight_file)
    play(self.STOP_file)

  def play2(self, pat, width):
    center=width/2-0.5
    if len(pat)==0:
        play(self.noway_file)
        self.prev_path=10
        return
    path=[]
    path.append(pat[0]-center)
    for i in range (1,len(pat)):
        path.append(pat[i]-pat[i-1])
    print(path)
    step=path[0]
    if step == -1 and step!=self.prev_path:
        play(self.turnleft_file)
    if step == -2 and step!=self.prev_path:
        play(self.hardleft_file)
    if step == 1 and step!=self.prev_path:
        play(self.turnright_file)
    if step == 2 and step!=self.prev_path:
        play(self.hardright_file)
    if step == 0 and step!=self.prev_path:
        play(self.straight_file)

    self.prev_path = step

if __name__=="__main__":

    interface = VoiceInterface()
    interface.play([2,1,2,3,2],5)