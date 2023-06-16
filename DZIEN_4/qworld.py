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

    def act(self):
        """
        określenie następnej akcji: albo z tabeli Q(eksploatacja) albo wybór losowy
        :return:
            action(tensor): akcja którą musi wykonać agent
        """

        # 0 - lewo, 1 - dół, 2 - prawo, 3 - góra
        if np.random.rand() <= self.epsilon:
            #eksploruj - wykonaj losową akcję
            self.is_explore = True
            return np.random.choice(4,1)[0]

        #lub eksploatacja  - wybór akcji z maksymalną wartością Q
        self.is_explore = False
        action = np.argmax(self.q_table[self.state])
        return action

    def update_q_table(self,state,action,reward,next_state):
        """
        Q-uczenie aktualizacja tabeli Q przy użyciu Q(s,a)
        :param state(tensor): stan agent
        :param action(tensor): akcja wykonywana przez agenta
        :param reward(float): nagroda po wykonaniu akcji dla dane stanu
        :param next_state(tensor): następny stan po wykonaniu akcji dla danego stanu
        :return:
        """

        #Q(s,a) = nagroda + gamma*max_a' Q(s',a')

        q_value = self.gamma*np.amax(self.q_table[next_state])
        q_value += reward
        self.q_table[state,action] = q_value

    def print_q_table(self):
        print("Q-Table (Epsilon: %0.2f)" %self.epsilon)
        print(self.q_table)

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def print_cell(self,row=0):
        """Interfejs użytkownika do wyswietlania agenta poruszającego się po siatce"""
        print("")
        for i in range(13):
            j = i-2
            if j in [0,4,8]:
                if j==8:
                    if self.state==2 and row==0:
                        marker = "\033[4mG\033[0m"
                    elif self.state==5 and row==1:
                        marker = "\033[4mH\033[0m"
                    else:
                        marker = 'G' if row == 0 else 'H'
                    color = self.state == 2 and row==0
                    color = color or (self.state == 5 and row==1)
                    color = 'red' if color else 'blue'
                    print(colored(marker,color), end='')
                elif self.state in [0,1,3,4]:
                    cell = [(0,0,0),(1,0,4),(3,1,0),(4,1,4)]
                    marker = '_' if(self.state, row,j) in cell else ' '
                    print(colored(marker,'red'),end='')
                else:
                    print(' ',end='')
            elif i%4 == 0:
                print("|",end='')
            else:
                print(' ',end='')
        print("")

    def print_world(self,action,step):
        """Interfejs użytkownika do wyświetlania trybu i akcji agenta"""
        actions = {0:"(Lewo)",1:"(Dol)",2:"(Prawo)",3:"(Gora)"}
        explore = "Eksploracja" if self.is_explore else "Eksploatacja"
        print("Krok",step,":",explore,actions[action])
        for _ in range(13):
            print("-",end='')
        self.print_cell()
        for _ in range(13):
            print("-",end='')
        self.print_cell(row=1)
        for _ in range(13):
            print("-",end='')
        print("")

def print_episode(episode, delay=1):
    """
    Interfejs użytkownia do wyświetlenia zlicznia epizodów
    :param episode(int):numer epizodu 
    :param delay(int):opóźnienie [sek] 
    :return: 
    """
    
    os.system('clear')
    for _ in range(13):
        print("-", end='')
    print("")
    print(f"Epizod: {episode}")
    for _ in range(13):
        print("-", end='')
    print("")
    time.sleep(delay)




