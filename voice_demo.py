from playsound import playsound as play
play_dict = {
          0: 'sounds/guitar.wav',
          1: 'sounds/left.wav',
          -1: 'sounds/right.wav',
          3: 'voice/STOP.mp3',
          2 : 'voice/WAIT.mp3',
          4 : 'sounds/chair.mp3'
      }
while(1):
	a=int(input())
	play(play_dict[a])
