from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Literal, Union
from fifoQueue import FifoQueue
import numpy as np
import math
import time
from modelExample import ModelExample

class Agent():

    def __init__(self, model: ModelExample):
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
        fifoQ = FifoQueue()
        self.model.reset_maze()
        """ posicion y desde donde """
        fifoQ.push(self.model.ActualPosition)
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

    def check_action(self, action):
        if action not in ["N", "E", "S", "W"]:
            raise ValueError("Run Ended - Invalid Action")
