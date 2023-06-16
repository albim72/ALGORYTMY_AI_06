"""
Tworzenia deterministycznego  świata QWorld [6 wymiarów -> 6 stanów]
Uwzględniamy algorytm Q-learning [uczenie ze wzmocnieniem]
"""

from collections import deque
import numpy as np
import argparse
import os
import time
from termcolor import colored

class QWorld:
    def __init__(self):
        self.col=4 #ruchy
        self.row=6 #stany
        
        #ustawienia otoczenia
        self.q_table = np.zeros([self.row,self.col])
        self.init_transition_table()
        self.init_reward_table()
        
        #współczynnik dyskontowy
        self.gamma = 0.9
        
        #90%eksploracja, 10%sksploatacja
        self.epsilon = 0.9
        
        #współczynnik zmiejszenia eksploracji po każdym epizodzie
        self.epsilon_decay = 0.9
        
        #długofalowo , 10%eksploracja, 90%eksploatacja
        self.epsilon_min = 0.1
        
        #reset otoczenia
        self.reset()
        self.is_explore = True
        
        
        
        
