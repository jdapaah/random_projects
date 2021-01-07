from random import randrange
from time import sleep

""" Guitar Barre Chords:
F  : E  - 1st fret
F#m: Em - 2nd fret
B m: Am - 2nd fret
"""
keys = ['G', 'D', 'C']
numbers = ['1', '2m', '3m', '4', '5', '6m']
notes = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#']


def major(r, n):
        start = notes.index(r)
        first3 = []
        if start<9:
                first3 = notes[start:start+5:2]
        else:
                first3 = notes[start::2] + notes[:start-7:2]                
        start-=12
        scale = []
        if start<0:
                scale = first3 + notes[start+5::2] + notes[:start+12:2]
        else:
                scale = first3 + notes[start+5:start+12:2]
        print(scale[int(n[:1])-1], end = 'm\n' if 'm' in n else '\n') 
                
        
while input()+'.':
	root = keys[randrange(3)]
	number = numbers[randrange(6)]
	print(root, number)
	print('Chord', end = ' - ')
	sleep(3)
	major(root, number)
