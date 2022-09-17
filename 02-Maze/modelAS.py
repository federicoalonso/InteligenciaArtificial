from abc import ABC, abstractmethod
from asyncio.windows_events import NULL
import math
from operator import mod
from tabnanny import verbose
from model import Model


class ModelExample(Model):

    def __init__(self, model_file):
        super().__init__(model_file)
        self.reset()
        #relative_path = './gym_maze/envs/maze_samples/'
        relative_path = 'C:\\Users\\fnico\\OneDrive\\Documentos\\Github\\InteligenciaArtificial\\02-Maze\\gym_maze\\envs\\maze_samples\\'
        self.Maze = dict()
        self._load_model(relative_path + model_file)
        self.ActualPosition = 0

    def _load_model(self, fullpath):
        print("Load your model here with file:", fullpath)
        with open(str(fullpath), 'r') as f:
            # print(list(f))
            Lines = f.readlines()
            for line in Lines:
                step = line.split()
                start = int(step[0])
                action = step[1]
                end = int(step[2])
                if start in self.Maze:
                    self.Maze[start][action] = end
                else:
                    # Lo creo, -1 es porque no se que hay
                    manhattan_distance = self.charge_heuristic(start)
                    self.Maze[start] = {
                        'N': -1, 'S': -1, 'E': -1, 'W': -1, 'From': -1, 'Visited': -1, 'h': manhattan_distance}
                    # agrego la arista
                    self.Maze[start][action] = end
            print(len(self.Maze))

    def charge_heuristic(self, position, *args, **kwargs):
        steps = kwargs.get('steps', 0)
        goal_position = self.get_goal(steps)[0]

        goal_y = math.floor(goal_position / 10)
        goal_x = goal_position - (goal_y * 10)
        it_y = math.floor(position / 10)
        it_x = position - (it_y * 10)
        dx = abs(goal_x - it_x)
        dy = abs(goal_y - it_y)
        # Manhattan distance is ok because never over estimate, always underestimate or its ok
        # it is the shortest path if not walls exists
        manhattan_distance = abs(dx + dy)
        return manhattan_distance

    def charge_position(self, action):
        self.ActualPosition = self.Maze[self.ActualPosition][action]
        return self.ActualPosition

    def get_neighbour(self, vertex):
        neighbour = []
        for v in self.Maze[vertex]:
            if v == 'N' or v == 'S' or v == 'E' or v == 'W':
                if self.Maze[vertex][v] != vertex:
                    neighbour.append(self.Maze[vertex][v])
        return neighbour

    def reset_maze(self, *args, **kwargs):
        steps = kwargs.get('steps', 0)
        self.reset_from()
        self.reset_visited()
        self.reset_heuristic(steps)

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