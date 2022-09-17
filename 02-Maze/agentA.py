from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Literal, Union
from priorityQueue import PriorityQueue
from fifoQueue import FifoQueue
import numpy as np
import time
from modelAS import ModelExample

class Agent():

    def __init__(self, model: ModelExample):
        super().__init__()
        self.model = model
        print(model)

    def run(self, env):
        self.model.reset()
        return self._loop(env)

    def _loop(self, env):
        print("Play A*...")
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
                actions = self.next_actions(goal_position, step_counter)
            
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

    def next_actions(self, goal_position, step):
        reached = False
        priorityQ = PriorityQueue()
        self.model.reset_maze(steps=step)
        """ posicion y desde donde """
        priorityQ.push(self.model.ActualPosition, self.model.Maze[self.model.ActualPosition]['h'])
        self.model.set_visited_from(self.model.ActualPosition,self.model.ActualPosition)

        while(not reached and not priorityQ.is_empty()):
            vertex_touple = priorityQ.pop()
            vertex = vertex_touple[0]
            self.model.set_visited(vertex)
            neighbours = self.model.get_neighbour(vertex)

            for v in neighbours:
                if not self.model.was_visited(v):
                    self.model.set_visited_from(v, vertex)
                    if(v != goal_position):
                        priorityQ.push(v, self.model.Maze[v]['h'])
                    else:
                        reached = True

        actions = self.model.get_path(goal_position)
        return actions

    def check_action(self, action):
        if action not in ["N", "E", "S", "W"]:
            raise ValueError("Run Ended - Invalid Action")
