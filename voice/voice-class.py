import sys
import os
import time
class VoiceInterface(object):

  def __init__(self):
    self.straight_file= 'straight.mp3'
    self.turnleft_file= 'turnleft.mp3'
    self.turnright_file='turnright.mp3'
    self.hardleft_file='hardleft.mp3'
    self.hardright_file='hardright.mp3'
    self.STOP_file='STOP.mp3'
    self.noway_file='noway.mp3'

  def play(self, pat, width):
    b=10
    center=width/2-0.5
    if len(pat)==0:
        cmd = 'play' + ' ' + self.noway_file
        os.system(cmd)
        time.sleep(1)
        return
    path=[]
    path.append(pat[0]-center)
    for i in range (1,len(pat)):
        path.append(pat[i]-pat[i-1])
    print(path)
    for step in path:
        if step == 1 and step!=b:
            cmd = 'play' + ' ' + self.turnleft
            os.system(cmd)
        if step == 2 and step!=b:
            cmd = 'play' + ' ' + self.hardleft_file
            os.system(cmd)
        if step == -1 and step!=b:
            cmd = 'play' + ' ' + self.turnright_file
            os.system(cmd)
        if step == -2 and step!=b:
            cmd = 'play' + ' ' + self.hardright_file
            os.system(cmd)
        if step == 0 and step!=b:
            cmd = 'play' + ' ' + self.straight_file
            os.system(cmd)
        b=step
        time.sleep(1)
    cmd = 'play' + ' ' + self.STOP_file
    os.system(cmd)

if __name__=="__main__":

    interface = VoiceInterface()
    interface.play([],5)
