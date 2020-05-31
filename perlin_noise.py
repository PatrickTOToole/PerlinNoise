import random
import math
import sys
from sys import stderr
import datetime

import png
seed = 72323
random.seed(seed)
random_vectors = []

GRID_SIZE = 16
pixel_density = 250
magnification = 4
map_range = 200
translation = 45

WIDTH = GRID_SIZE
HEIGHT = GRID_SIZE
for i in range(WIDTH):
    random_vectors.append([])
    for j in range(HEIGHT):
        x_val = random.randint(0,360)
        y_val = random.randint(0,360)
        x_val = math.radians(x_val)
        y_val = math.radians(y_val)
        x_val = math.cos(x_val)
        y_val = math.sin(y_val)

        random_vectors[i].append([[x_val,y_val]])
def fade(input):
    return 6 * (pow(input, 5)) - 15 * (pow(input, 4)) + 10 * (pow(input, 3))
def noise(x, y, map_range):
    if x < 0 or math.ceil(x) >= WIDTH or y < 0 or math.ceil(y) >= HEIGHT:
        sys.stderr.write("Out of range")
    x_min = math.floor(x)
    x_max = math.ceil(x)
    y_min = math.floor(y)
    y_max = math.ceil(y)
    xy_min = random_vectors[x_min][y_min][0]
    xy_min_max = random_vectors[x_min][y_max][0]
    xy_max_min = random_vectors[x_max][y_min][0]
    xy_max = random_vectors[x_max][y_max][0]
    x -= x_min
    y -= y_min
    x_max = 1
    y_max = 1
    y = fade(y)
    x = fade(x)
    dA = xy_min[0] * x + xy_min[1] * y
    dB = xy_max_min[0] * (x_max - x) + xy_max_min[1] * y
    dC = xy_min_max[0] * x + xy_min_max[1] * (y_max - y)
    dD = xy_max[0] * (x_max - x) + xy_max[1] * (y_max - y)
    AB = dA + x*(dB - dA)
    CD = dC + x*(dD - dC)
    value = AB + y *(CD - AB)
    value += 1.5
    value /= 3
    value *= map_range
    return int(value)


array = []
scale = 1 / pixel_density
num_pixels = pixel_density * magnification
num_x = num_pixels
num_y = num_pixels
for y_off in range(num_y):
    array.append([])
    for x_off in range(num_x):
        array[y_off].append([])
        x_temp = x_off * scale
        y_temp = y_off * scale
        val = noise(x_temp, y_temp, map_range)
        if(val < 0 or val > map_range):
            sys.stderr.write(f"Height value of range: {map_range}")
            sys.exit(-1)
        val += translation
        array[y_off][x_off] = val
    if(y_off % 6  == 0):
        print(y_off/num_y)
name = str(magnification) + "x_Grid_" + str(GRID_SIZE) + "_Pixel_dens_" + str(pixel_density)
currentDT = datetime.datetime.now()
name += "_" + str(currentDT.hour % 12) + "-" + str(currentDT.minute) + "_" +str(seed) + ".png"
png.from_array(array, 'L').save(name)
print("Successfully created file: " + name)

sys.exit(0)