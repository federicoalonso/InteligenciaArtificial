from abc import ABC, abstractmethod
from dataclasses import asdict
import math
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
        self.Maze = dict()
        self.Steps = 0
        self.GoalPosition = self.model.get_goal(self.Steps)[0]
        self.set_initial_maze()
        self.ActualPosition = 0
        self.UnknownNeigbours = PriorityQueue()

    def run(self, env):
        self.model.reset()
        return self._loop(env)

    def _loop(self, env):
        print("Play LRTA*...")
        obs = env.reset()
        print(obs)
        done = False
        all_rewards = 0
        env.render()
        actions = []
        prev_goal_position = 0

        while not done:
            time.sleep(1)
            action = ''
            self.GoalPosition = self.model.get_goal(self.Steps)[0]
            env.set_goal(self.GoalPosition)



            if len(actions) == 0:
                if(self.Steps == 0 or prev_goal_position != self.GoalPosition):
                    prev_goal_position = self.GoalPosition
                    reacheble = self.goal_is_reacheable()
                    if reacheble:
                        actions = self.next_actions(self.GoalPosition)
                actions = self.charge_new_possibilities(self.ActualPosition)
            
            action = actions.pop(0)

            print(f"Pasos {self.Steps} y la accion es {action}.")
            if self.Steps == 31:
                print(f"Error.")

            self.check_action(action)
            obs, reward, done_env, _ = env.step(action)
            
            prev_pos = self.ActualPosition
            self.ActualPosition = obs[1] * 10 + obs[0]
            self.save_move(prev_pos, action)

            print(f'{obs=} {reward=} {done_env=}')
            all_rewards += reward
            done = done_env and self.model.is_win_goal()
            env.render()
            self.Steps += 1

        return all_rewards, self.Steps

    def save_move(self, prev_position, action):
        if prev_position == self.ActualPosition:
            self.Maze[prev_position][action] = prev_position
        else:
            self.Maze[prev_position][action] = self.ActualPosition
            if action == 'N':
                self.Maze[self.ActualPosition]['S'] = prev_position
            elif action == 'S':
                self.Maze[self.ActualPosition]['N'] = prev_position
            elif action == 'E':
                self.Maze[self.ActualPosition]['W'] = prev_position
            else:
                self.Maze[self.ActualPosition]['E'] = prev_position

    def charge_new_possibilities(self, position):
        if self.Maze[position]['enqueue_unknown_actions'] == -1:
            self.Maze[position]['enqueue_unknown_actions'] = 0
            if self.Maze[position]['W'] == -1:
                self.UnknownNeigbours.push((position, 'W'), self.charge_heuristic(position - 1))
            if self.Maze[position]['E'] == -1:
                self.UnknownNeigbours.push((position, 'E'), self.charge_heuristic(position + 1))
            if self.Maze[position]['S'] == -1:
                self.UnknownNeigbours.push((position, 'S'), self.charge_heuristic(position + 10))
            if self.Maze[position]['N'] == -1:
                self.UnknownNeigbours.push((position, 'N'), self.charge_heuristic(position - 10))
        self.update_weights()
        better = self.UnknownNeigbours.pop()
        actions = self.next_actions(better[0][0])
        betteraction = better[0][1]
        return actions + [betteraction]

    def update_weights(self):
        list = []
        while not self.UnknownNeigbours.is_empty():
            it = self.UnknownNeigbours.pop()
            list.append(it)
        # ((pos, act), h)
        while len(list) != 0:
            it = list.pop()
            act = self.next_actions(it[0][0])
            cost = self.Maze[it[0][0]]['h'] + len(act)
            #cost = self.Maze[it[0][0]]['h'] + self.full_heuristic(self.ActualPosition, it[0][0])
            self.UnknownNeigbours.push((it[0][0],it[0][1]), cost)



    def charge_position(self, action):
        self.ActualPosition = self.Maze[self.ActualPosition][action]
        return self.ActualPosition

    # la dejo por aca para ver si aplica luego, no esta terminada ni ahi
    def get_unknown_actions(self, position):
        # no he verificado a sus vecinos aun
        if self.Maze[position]['enqueue_unknown_actions'] == -1:
            for k in self.Maze[position]:
                if k == 'N' or k == 'S' or k == 'E' or k == 'W':
                    # no ha probado la opcion
                    if self.Maze[position][k] == -1:
                        self.UnknownNeigbours

    def set_initial_maze(self):
        for v in range(100):
            manhattan_distance = self.charge_heuristic(v)
            if v == 0:
                self.Maze[v] = {'N': v, 'S': -1, 'E': -1, 'W': v, 'From': -1, 'Visited': -1, 'h': manhattan_distance, 'enqueue_unknown_actions': -1}
            elif v == 9:
                self.Maze[v] = {'N': v, 'S': -1, 'E': v, 'W': -1, 'From': -1, 'Visited': -1, 'h': manhattan_distance, 'enqueue_unknown_actions': -1}
            elif v == 90:
                self.Maze[v] = {'N': -1, 'S': v, 'E': -1, 'W': v, 'From': -1, 'Visited': -1, 'h': manhattan_distance, 'enqueue_unknown_actions': -1}
            elif v == 99:
                self.Maze[v] = {'N': -1, 'S': v, 'E': v, 'W': -1, 'From': -1, 'Visited': -1, 'h': manhattan_distance, 'enqueue_unknown_actions': -1}
            else:
                if v < 9:
                    self.Maze[v] = {'N': v, 'S': -1, 'E': -1, 'W': -1, 'From': -1, 'Visited': -1, 'h': manhattan_distance, 'enqueue_unknown_actions': -1}
                elif v > 90:
                    self.Maze[v] = {'N': -1, 'S': v, 'E': -1, 'W': -1, 'From': -1, 'Visited': -1, 'h': manhattan_distance, 'enqueue_unknown_actions': -1}
                elif v % 10 == 0:
                    self.Maze[v] = {'N': -1, 'S': -1, 'E': -1, 'W': v, 'From': -1, 'Visited': -1, 'h': manhattan_distance, 'enqueue_unknown_actions': -1}
                elif (v + 1) % 10 == 0:
                    self.Maze[v] = {'N': -1, 'S': -1, 'E': v, 'W': -1, 'From': -1, 'Visited': -1, 'h': manhattan_distance, 'enqueue_unknown_actions': -1}
                else:
                    self.Maze[v] = {'N': -1, 'S': -1, 'E': -1, 'W': -1, 'From': -1, 'Visited': -1, 'h': manhattan_distance, 'enqueue_unknown_actions': -1}

    def charge_heuristic(self, position):
        goal_y = math.floor(self.GoalPosition / 10)
        goal_x = self.GoalPosition - (goal_y * 10)
        it_y = math.floor(position / 10)
        it_x = position - (it_y * 10)
        dx = abs(goal_x - it_x)
        dy = abs(goal_y - it_y)
        # Manhattan distance is ok because never over estimate, always underestimate or its ok
        # it is the shortest path if not walls exists
        manhattan_distance = abs(dx + dy)
        return manhattan_distance

    def full_heuristic(self, position, dest):
        goal_y = math.floor(dest / 10)
        goal_x = dest - (goal_y * 10)
        it_y = math.floor(position / 10)
        it_x = position - (it_y * 10)
        dx = abs(goal_x - it_x)
        dy = abs(goal_y - it_y)
        # Manhattan distance is ok because never over estimate, always underestimate or its ok
        # it is the shortest path if not walls exists
        manhattan_distance = abs(dx + dy)
        return manhattan_distance

    def goal_is_reacheable(self):
        pos = self.GoalPosition
        if pos == 0:
            return self.Maze[pos + 1]['W'] != -1 or self.Maze[pos + 10]['N'] != -1
        elif pos == 9:
            return self.Maze[pos - 1]['E'] != -1 or self.Maze[pos + 10]['N'] != -1
        elif pos == 90:
            return self.Maze[pos + 1]['W'] != -1 or self.Maze[pos - 10]['S'] != -1
        elif pos == 99:
            return self.Maze[pos - 1]['E'] != -1 or self.Maze[pos - 10]['S'] != -1
        else:
            if pos < 9:
                return self.Maze[pos + 1]['W'] != -1 or self.Maze[pos + 10]['N'] != -1 or self.Maze[pos - 1]['E'] != -1
            elif pos > 90:
                return self.Maze[pos + 1]['W'] != -1 or self.Maze[pos - 10]['S'] != -1 or self.Maze[pos - 1]['E'] != -1
            elif pos % 10 == 0:
                return self.Maze[pos - 10]['S'] != -1 or self.Maze[pos + 10]['N'] != -1 or self.Maze[pos + 1]['W'] != -1
            elif (pos + 1) % 10 == 0:
                return self.Maze[pos - 10]['S'] != -1 or self.Maze[pos + 10]['N'] != -1 or self.Maze[pos - 1]['E'] != -1
            else:
                return self.Maze[pos - 10]['S'] != -1 or self.Maze[pos + 10]['N'] != -1 or self.Maze[pos - 1]['E'] != -1 or self.Maze[pos + 1]['W'] != -1






    def next_actions(self, goal):
        reached = self.ActualPosition == goal
        priorityQ = PriorityQueue()
        self.reset_maze()
        """ posicion y desde donde """
        priorityQ.push(self.ActualPosition, self.Maze[self.ActualPosition]['h'])
        self.set_visited_from(self.ActualPosition,self.ActualPosition)

        while(not reached and not priorityQ.is_empty()):
            vertex_touple = priorityQ.pop()
            vertex = vertex_touple[0]
            self.set_visited(vertex)
            neighbours = self.get_neighbour(vertex)

            for v in neighbours:
                if not self.was_visited(v):
                    self.set_visited_from(v, vertex)
                    if(v != goal):
                        priorityQ.push(v, self.Maze[v]['h'])
                    else:
                        reached = True

        actions = self.get_path(goal)
        return actions

    def check_action(self, action):
        if action not in ["N", "E", "S", "W"]:
            raise ValueError("Run Ended - Invalid Action")




    def get_neighbour(self, vertex):
        neighbour = []
        for v in self.Maze[vertex]:
            if v == 'N' or v == 'S' or v == 'E' or v == 'W':
                if (self.Maze[vertex][v] != vertex) and (self.Maze[vertex][v] != -1):
                    neighbour.append(self.Maze[vertex][v])
        return neighbour

    def reset_maze(self):
        self.reset_from()
        self.reset_visited()
        #self.reset_heuristic(self.Steps)

    def reset_visited(self):
        for v in self.Maze:
            self.Maze[v]['Visited'] = -1

    def reset_from(self):
        for v in self.Maze:
            self.Maze[v]['From'] = -1

    def reset_heuristic(self, step):
        for v in self.Maze:
            manhattan_distance = self.charge_heuristic(v, steps=step)
            self.Maze[v]['h'] = manhattan_distance

    def set_visited(self, vertex):
        self.Maze[vertex]['Visited'] = 1
    
    def set_visited_from(self, vertex, v_from):
        self.Maze[vertex]['From'] = v_from

    def was_visited(self, vertex):
        return self.Maze[vertex]['Visited'] == 1
    
    def get_path(self, destination):
        # si llega a -1 o a la misma posicion termina
        actions = []
        not_done = True
        while not_done:
        # me fijo el from
            v_from = self.Maze[destination]['From']
            if v_from == -1 or v_from == destination:
                not_done = False
            else:
                if self.Maze[v_from]['N'] == destination:
                    actions = ['N'] + actions
                    destination = v_from
                elif self.Maze[v_from]['S'] == destination:
                    actions = ['S'] + actions
                    destination = v_from
                elif self.Maze[v_from]['E'] == destination:
                    actions = ['E'] + actions
                    destination = v_from
                elif self.Maze[v_from]['W'] == destination:
                    actions = ['W'] + actions
                    destination = v_from
                else:
                    not_done = False
        # voy hasta el from y me fijo que accion lleva a el
        # si ninguna termino
        # si alguna, la agrego al principio
        return actions