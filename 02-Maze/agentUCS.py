from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Literal, Union
from fifoQueue import FifoQueue
import numpy as np
import math
import time
#from modelExample import ModelExample

# DO NOT CHANGE THIS CLASS: EXTEND IT WITH YOUR OWN


class Agent():

    def __init__(self, model):
        super().__init__()
        self.model = model
        print(model)

    def run(self, env):
        self.model.reset()
        return self._loop(env)

    def _loop(self, env):
        print("Play manually...")
        obs = env.reset()
        print(obs)
        done = False
        step_counter = 0
        all_rewards = 0
        env.render()
        goal_position = -1
        actions = []

        while not done:
            print(step_counter)
            time.sleep(1)
            action = ''
            goalId = self.model.get_goal(step_counter)[0]
            env.set_goal(goalId)
            if(goal_position == -1 or goal_position != goalId):
                goal_position = goalId
                actions = self.next_actions(goal_position)
            
            action = actions.pop(0)

            # if(action == 'N'):
            #     actual_position -= 10
            # elif(action == 'S'):
            #     actual_position += 10
            # elif(action == 'W'):
            #     actual_position -= 1
            # else:
            #     actual_position += 1
            self.model.charge_position(action)
            
            self.check_action(action)
            obs, reward, done_env, _ = env.step(action)
            print(f'{obs=} {reward=} {done_env=}')
            all_rewards += reward
            done = done_env and self.model.is_win_goal()
            env.render()
            step_counter += 1

        return all_rewards, step_counter

    def next_actions(self, goal_position):
        reached = False
        len = len(self.model.Maze)

        # visited = [None]*len
        # for x in range(len):
        #     visited[x] = 0
        fifoQ = FifoQueue()
        # matr_from = [None]*len
        # for x in range(len):
        #     matr_from[x] = [None]*len
        #     for y in range(len):
        #         matr_from[x][y] = -1

        """ posicion y desde donde """
        fifoQ.push(self.model.ActualPosition)
        # visited[self.model.ActualPosition] = 1
        # matr_from[self.model.ActualPosition][self.model.ActualPosition] = self.model.ActualPosition
        self.model.set_visited_from(self.model.ActualPosition,self.model.ActualPosition)

        while(not reached and not fifoQ.is_empty()):
            vertex = fifoQ.pop()
            self.model.set_visited(vertex)
            neighbours = self.model.get_neighbour(vertex)
            for v in neighbours:
                if not self.model.was_visited(v):
                    self.model.set_visited_from(v, vertex)
                    if(v != goal_position):
                        fifoQ.push(v)
                    else:
                        reached = True

        actions = self.model.get_path(goal_position)
        return actions
    
    # def generate_path(self, matr_from, goal_position):
    #     actions_bk = []
    #     end = False
    #     pos = goal_position
    #     while(not end):
    #         for x in range(100):
    #             it = matr_from[x][pos]
    #             if(it != -1):
    #                 actions_bk.append(self.model.Maze[x][pos])
    #                 if(it == pos):
    #                     end = True
    #                     actions_bk.pop()
    #                 else:
    #                     pos = it
    #     actions = []

    #     for x in reversed(actions_bk):
    #         if(x == 1):
    #             actions.append('N')
    #         elif(x == 2):
    #             actions.append('S')
    #         elif(x == 3):
    #             actions.append('E')
    #         else:
    #             actions.append('W')

    #     return actions

    def check_action(self, action):
        if action not in ["N", "E", "S", "W"]:
            raise ValueError("Run Ended - Invalid Action")
