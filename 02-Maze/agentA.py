from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Literal, Union
from priorityQueue import PriorityQueue
from fifoQueue import FifoQueue
import numpy as np
import math
import time

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
        actual_position = 0
        all_rewards = 0
        env.render()
        goal_position = -1
        matr_maze = self.charge_maze(env)
        actions = []

        while not done:
            print(step_counter)
            #time.sleep(1)
            action = ''
            goalId = self.model.get_goal(step_counter)[0]
            env.set_goal(goalId)
            if(goal_position == -1 or goal_position != goalId):
                goal_position = goalId
                actions = self.next_actions(actual_position, matr_maze, goal_position)
            
            action = actions.pop(0)

            if(action == 'N'):
                actual_position -= 10
            elif(action == 'S'):
                actual_position += 10
            elif(action == 'W'):
                actual_position -= 1
            else:
                actual_position += 1

            self.check_action(action)
            obs, reward, done_env, _ = env.step(action)
            print(f'{obs=} {reward=} {done_env=}')
            all_rewards += reward
            done = done_env and self.model.is_win_goal()
            env.render()
            step_counter += 1

        return all_rewards, step_counter

    def next_actions(self, actual_position, matr_maze, goal_position):
        reached = False

        visited = [None]*100
        for x in range(100):
            visited[x] = 0
        priorityQ= PriorityQueue()
        matr_from = [None]*100
        for x in range(100):
            matr_from[x] = [None]*100
            for y in range(100):
                matr_from[x][y] = -1


        arr_h = self.charge_heuristic(goal_position)

        """ posicion y desde donde """
        priorityQ.push(actual_position, arr_h[actual_position])
        visited[actual_position] = 1
        matr_from[actual_position][actual_position] = actual_position

        while(not reached and not priorityQ.is_empty()):
            vortix_touple = priorityQ.pop()
            vortix = vortix_touple[0]
            visited[vortix] = 1

            for x in range(100):
                if(matr_maze[vortix][x] != 0 and x != vortix):
                    if(visited[x] == 0):
                        if(x != goal_position):
                            matr_from[vortix][x] = vortix
                            priorityQ.push(x, arr_h[x])
                        else:
                            matr_from[vortix][x] = vortix
                            reached = True

        actions = self.generate_path(matr_from, goal_position, matr_maze)
        return actions
    
    def generate_path(self, matr_from, goal_position, matr_maze):
        actions_bk = []
        end = False
        pos = goal_position
        while(not end):
            for x in range(100):
                it = matr_from[x][pos]
                if(it != -1):
                    actions_bk.append(matr_maze[x][pos])
                    if(it == pos):
                        end = True
                        actions_bk.pop()
                    else:
                        pos = it
        actions = []

        for x in reversed(actions_bk):
            if(x == 1):
                actions.append('N')
            elif(x == 2):
                actions.append('S')
            elif(x == 3):
                actions.append('E')
            else:
                actions.append('W')

        return actions
    
    def charge_heuristic(self, goal_position):
        arr_h = np.zeros(100)
        goal_y = math.floor(goal_position / 10)
        goal_x = goal_position - (goal_y * 10)
        for it in range(100):
            it_y = math.floor(it / 10)
            it_x = it - (it_y * 10)
            dx = abs(goal_x - it_x)
            dy = abs(goal_y - it_y)
            # Manhattan distance is ok because never over estimate, always underestimate or its ok
            # it is the shortest path if not walls exists
            manhattan_distance = abs(dx + dy)
            arr_h[it] = manhattan_distance
        return arr_h

    def check_action(self, action):
        if action not in ["N", "E", "S", "W"]:
            raise ValueError("Run Ended - Invalid Action")

    def charge_maze(self, env):
        matr_maze = np.zeros((100, 100))
        file1 = open('C:\\Users\\fnico\\OneDrive\\Documentos\\Github\\InteligenciaArtificial\\Maze\\gym_maze\\envs\\maze_samples\\MazeEnv10x10_1.txt', 'r')
        
        Lines = file1.readlines()
        for line in Lines:
            step = line.split()
            start = int(step[0])
            action = step[1]
            end = int(step[2])

            if(start != end):
                if(action == 'N'):
                    matr_maze[start][end] = 1
                    matr_maze[end][start] = 2
                elif(action == 'S'):
                    matr_maze[start][end] = 2
                    matr_maze[end][start] = 1
                elif(action == 'E'):
                    matr_maze[start][end] = 3
                    matr_maze[end][start] = 4
                else:
                    matr_maze[start][end] = 4
                    matr_maze[end][start] = 3
        return matr_maze
