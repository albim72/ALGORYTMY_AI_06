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

    def reset(self):
        """początek epizodu"""
        self.state = 0
        return self.state

    def is_in_win_state(self):
        return self.state == 2

    def init_reward_table(self):
        """
        # 0 - lewo, 1 - dół, 2 - prawo, 3 - góra
        ___________________________
        |   0   |   0   |   100  |
        ___________________________
        |   0   |   0   |   -100  |
        ___________________________

        """
        self.reward_table = np.zeros([self.row],[self.col])
        self.reward_table[1,2] = 100.
        self.reward_table[4,2] = -100.

    def init_transition_table(self):
        """
        # 0 - lewo, 1 - dół, 2 - prawo, 3 - góra
        ___________________________
        |   0   |   1   |   2  |
        ___________________________
        |   3   |   4   |   5  |
        ___________________________

        """
        self.transition_table = np.zeros([self.row,self.col],dtype=int)

        self.transition_table[0,0]= 0
        self.transition_table[0,1]= 3
        self.transition_table[0,2]= 1
        self.transition_table[0,3]= 0

        self.transition_table[1, 0] = 0
        self.transition_table[1, 1] = 4
        self.transition_table[1, 2] = 2
        self.transition_table[1, 3] = 1

        #graniczny stan docelowy

        self.transition_table[2, 0] = 2
        self.transition_table[2, 1] = 2
        self.transition_table[2, 2] = 2
        self.transition_table[2, 3] = 2

        self.transition_table[3, 0] = 3
        self.transition_table[3, 1] = 3
        self.transition_table[3, 2] = 4
        self.transition_table[3, 3] = 0

        self.transition_table[4, 0] = 3
        self.transition_table[4, 1] = 4
        self.transition_table[4, 2] = 5
        self.transition_table[4, 3] = 1

        # graniczny stan dziura

        self.transition_table[5, 0] = 5
        self.transition_table[5, 1] = 5
        self.transition_table[5, 2] = 5
        self.transition_table[5, 3] = 5

    def step(self,action):
        """
        wykonuje akcję na otoczeniu
        Argument:
        action(tensor): akcja w przestrzeni akcji
        Zwraca:
        next_state(tensor): następmny stan otoczenia
        reward(float):nagroda dla agenta
        done(Bool):czy osiągnięto cel graniczny
        """
        
        #definicja następnego stanu (next_state), mając dany stan i akcję
        next_state = self.transition_table[self.state,action]
        #done ma wartość True, jeśsli next_state to cel albo dziura
        done = next_state == 2 or next_state == 5
        #nagroda dla stanu i akcji
        reward = self.reward_table[self.state,action]
        #otoczenie jest w nowy stanie
        self.state = next_state
        return next_state,reward,done



