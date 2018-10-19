import os
while(1):
    a=input()
    if a=='1':
    	os.system('play straight.mp3')
    if a=='2':
    	os.system('play turnleft.mp3')
    if a=='3':
    	os.system('play turnright.mp3')
    if a=='4':
    	os.system('play hardleft.mp3')
    if a=='5':
    	os.system('play hardright.mp3')
    if a=='0':
    	os.system('play STOP.mp3')
