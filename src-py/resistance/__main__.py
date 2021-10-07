from random_agent import RandomAgent
from resistance import Resistance
from spy import Spy

from game import Game

agents = [Spy(name='s1'), 
        Spy(name='s2'),  
        Resistance(name='r1'),  
        Resistance(name='r2'),  
        Resistance(name='r3'),  
        ]

b = 100
c = 0
for j in range(b):
        a = 0
        for i in range(b):
                game = Game(agents)
                game.play()
                if str(game)[:3] == "won":
                        a+=1
                #print(game)
        c += a

c = c / b
print(str(c) + "/" + str(b))


