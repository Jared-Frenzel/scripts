import numpy as np
from tkinter import *
import threading
import time
from itertools import combinations

class Board():
    def __init__(self, size, pixel_size=1, draw_speed=1):
        self.size = size
        self.pixel_size = pixel_size
        self.sleep_duration = draw_speed**-1

        self.master = Tk()
        self.canvas = Canvas(self.master, width=pixel_size * size[0],
                             height=pixel_size * size[1])
        self.canvas.pack()

        self.board_matrix = \
                np.array([np.array(['white' for _ in
                                    range(size[0]*pixel_size)]) for _ in
                          range(size[1]*pixel_size)])
        self._reset_board()

    def draw(self, image, draw_speed):
        visited_map = np.array([[False]*image.shape[1]]*image.shape[0], dtype=bool)

        polygons = {}

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i,j] != 'white' and not visited_map[i,j]:
                    new_poly = [(i,j)]
                    visited_map[i,j] = True
                    index = 0
                    while len(new_poly) > index:
                        for offset in combinations([-1,0,1], 2):
                            x = min(max(offset[0] + i, 0), image.shape[0]-1)
                            y = min(max(offset[1] + j, 0), image.shape[1]-1)
                            if image[x,y] != 'white' and not visited_map[x,y]:
                                new_poly.append((x,y))
                                visited_map[x,y] = True
                        index += 1
                    print(new_poly)
        pass

    def draw_polgon(self, polygon, draw_speed):
        pass

    def mark(self, coordinates):
        self.move(coordinates)
        self._set(coordinates, 'black')

    def erase(self, coordinates):
        self.move(coordinates)
        self._set(coordinates, 'white')

    def move(self, coordinates):
        while self.cursor['x'] != coordinates[0] and self.cursor['y'] != coordinates[1]:
            if abs(self.cursor['x'] - coordinates[0]) > abs(self.cursor['y'] -
                                                            coordinates[1]):
                new_x = self.cursor['x'] + (self.cursor['x'] -
                                               coordinates[0]) / abs(self.cursor['x'] - coordinates[0])
                self._set((new_x, self.cursor['y']), None)
            else:
                new_y = self.cursor['y'] + (self.cursor['y'] -
                                               coordinates[1]) / abs(self.cursor['y'] - coordinates[1])
                self._set((self.cursor['x'], new_y), None)
            time.sleep(self.sleep_duration)


    def _set(self, coordinates, color):
        if color: self.board_matrix[coordinates[0] * self.pixel_size,
                                    coordinates[1] * self.pixel_size] = color
        x = self.cursor['x']
        y = self.cursor['y']
        self.cursor['x'] = coordinates[0]
        self.cursor['y'] = coordinates[1]

        #print(x,y)

        self.canvas.create_rectangle(x * self.pixel_size,
                                     y * self.pixel_size,
                                     (x+1)*self.pixel_size,
                                     (y+1)*self.pixel_size,
                                     width=0, fill=self.board_matrix[x,y])

        self.canvas.create_rectangle(self.cursor['x'] * self.pixel_size,
                                     self.cursor['y'] * self.pixel_size,
                                     (self.cursor['x']+1)*self.pixel_size,
                                     (self.cursor['y']+1)*self.pixel_size,
                                     width=0, fill='#ff0000')

    def _reset_board(self):
        self.board_matrix = \
                np.array([np.array(['white' for _ in range(self.size[0] *
                                    self.pixel_size)]) for _ in
                          range(self.size[1] * self.pixel_size)])
        self.canvas.create_rectangle(0,0,*(np.array(self.size)*self.pixel_size), width=0, fill='white')
        self.cursor = dict([('x', 0), ('y', 0)])
        print('board reset')


    def __repr__(self):
        return str(self.board_matrix)


b = Board((100,90), pixel_size=7)

image = np.array([[np.random.choice(['white','black']) for j in range (90)] for i in
         range(100)])

b.draw(image, 5)
b.master.mainloop()
