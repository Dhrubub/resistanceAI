from random_agent import RandomAgent
from resistance import Resistance
from spy import Spy

from game import Game

agents5 = [Resistance(name='s1'), 
        Resistance(name='s2'),
        Resistance(name='r1'),  
        Resistance(name='r2'),  
        Resistance(name='r3'),
        ]

agents6 = [Resistance(name='s1'), 
        Resistance(name='s2'),
        Resistance(name='r1'),  
        Resistance(name='r2'),  
        Resistance(name='r3'),
        Resistance(name='r4'),
        ]

agents7 = [Resistance(name='s1'), 
        Resistance(name='s2'),
        Resistance(name='s3'),  
        Resistance(name='r1'),  
        Resistance(name='r2'),  
        Resistance(name='r3'),
        Resistance(name='r4'),   
        ]

agents8 = [Resistance(name='s1'), 
        Resistance(name='s2'),
        Resistance(name='s3'),  
        Resistance(name='r1'),  
        Resistance(name='r2'),  
        Resistance(name='r3'),
        Resistance(name='r4'), 
        Resistance(name='r5'),  
        ]

agents9 = [Resistance(name='s1'), 
        Resistance(name='s2'),
        Resistance(name='s3'),  
        Resistance(name='r1'),  
        Resistance(name='r2'),  
        Resistance(name='r3'),
        Resistance(name='r4'),  
        Resistance(name='r5'), 
        Resistance(name='r6'), 
        ]

agents10 = [Resistance(name='s1'), 
        Resistance(name='s2'),
        Resistance(name='s3'),  
        Resistance(name='s3'),  
        Resistance(name='r1'),  
        Resistance(name='r2'),  
        Resistance(name='r3'),
        Resistance(name='r4'),  
        Resistance(name='r5'), 
        Resistance(name='r6'),   
        ]

all_agents = [agents5, agents6, agents7, agents8, agents9, agents10]
for agents in all_agents:
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


