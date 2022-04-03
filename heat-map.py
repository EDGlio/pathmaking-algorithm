import numpy as np
import showMaps
import pygame
from pygame.locals import *
import time


# 100 - not done (empty)
# 200 - obstacle/barrier

# Define variables
empty = 500
barrier = 1000
endPos = (6, 6)

# Sample map
map = [
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, barrier, barrier, empty, empty, empty, empty],
  [empty, empty, barrier, empty, empty, empty, empty, empty],
  [empty, empty, barrier, empty, empty, empty, empty, empty],
  [empty, empty, barrier, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, barrier, empty, 0, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty]
]

white_map = [
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, empty, empty, 0, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty],
]

HEIGHT, WIDTH = 400, 400
RECT_HEIGHT, RECT_WIDTH = 50, 50
FPS = 20

WHITE = (255, 255, 255)
BARRIER = (200, 50, 50)
PATH = (0, 0, 0) # (230, 190, 138)

# file = 'tmw_desert_spacing.png'
# image = pygame.image.load(file)
# rect = image.get_rect()
# print(image)

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
FPSCLOCK = pygame.time.Clock()


''' FUNCTIONS '''

# Renders all white tiles
def render_all_white():
  print('epic')
  m, n = 8, 8
  for i in range(m):
    for j in range(n):
      tile = pygame.Rect(j * RECT_WIDTH, i * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT)
      pygame.draw.rect(DISPLAYSURF, WHITE, tile)
      pygame.display.update()

# Renders the map
def render_map(map):
  m, n = 8, 8
  for i in range(m):
    for j in range(n):
      tile = pygame.Rect(j * RECT_WIDTH, i * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT)
      val = map[i][j]
      if val == barrier:
        col = BARRIER
      elif val == empty:
        col = WHITE
      else:
        col = (150 - (10 * val), (10 * val), (10 * val))
      pygame.draw.rect(DISPLAYSURF, col, tile)
      pygame.display.update()
  return map

# finds path using heat map
def render_tile(pos, col):
  tile = pygame.Rect(pos[1] * RECT_WIDTH, pos[0] * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT)
  pygame.draw.rect(DISPLAYSURF, col, tile)
  pygame.display.update()
  print(pos)
def find_path(heat_map, start_pos):
  run = True
  # current position
  current_pos = start_pos

  # path that will be appended to
  path = [current_pos]
  current_val = map[current_pos[0]][current_pos[1]]
  while run:
    render_tile(current_pos, PATH)
    time.sleep(0.5)
    try:
      if current_pos[0] != 7 and map[current_pos[0] + 1][current_pos[1]] == current_val - 1:
        current_pos = [current_pos[0] + 1, current_pos[1]]
        current_val = map[current_pos[0]][current_pos[1]]
      elif current_pos[0] != 0 and map[current_pos[0] - 1][current_pos[1]] == current_val - 1:
        current_pos = [current_pos[0] - 1, current_pos[1]]
        current_val = map[current_pos[0]][current_pos[1]]
      elif current_pos[1] != 7 and map[current_pos[0]][current_pos[1] + 1] == current_val - 1:
        current_pos = [current_pos[0], current_pos[1] + 1]
        current_val = map[current_pos[0]][current_pos[1]]
      elif current_pos[1] != 0 and map[current_pos[0]][current_pos[1] - 1] == current_val - 1:
        current_pos = [current_pos[0], current_pos[1] - 1]
        current_val = map[current_pos[0]][current_pos[1]]        
        
    except: pass
    path.append(current_pos)
    if current_val == 0:
      run = False
  render_tile(current_pos, PATH)
  return path

# Creates heat map
def heat_map(map, endPos):
  pairs_to_check = []
  pairs_to_check.append(endPos)
  
  run = True
  while run:
    # Pairs to check next time
    new_pairs = []
    for current in pairs_to_check:
      # Checks up, down, left, right
      for i in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        try:
          # going up, down, left, right and then changing/checking them
          changing = np.array(current) + np.array(i)
          
          # getting values at current and changing coordinates
          new_val = map[changing[1]][changing[0]]
          current_val = map[current[1]][current[0]]
          if new_val != barrier:
            # checking if empty or if there is a better way to get there
            if new_val > current_val:
              new_val = current_val + 1
              new_pairs.append(changing) # check it next time
              map[changing[1]][changing[0]] = new_val # change the value at the place
        except: pass
      # print(new_pairs, pairs_to_check)
    pairs_to_check = new_pairs.copy()
    if not any(empty in x for x in map):
      run = False
  return map

# render_map(find_path(heat_map(map, endPos), [0, 0]))
map = render_map(heat_map(map, endPos))

time.sleep(2)
print('gogogo')
find_path(map, (1, 1))


''' GAME LOOP '''

customize = False

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        customize = True
        render_all_white()
        map = white_map.copy()
      if event.key == pygame.K_RETURN:
        customize = False
        print('potato')
        render_map(heat_map(map, endPos))
        print('pot')
    if event.type == pygame.MOUSEBUTTONUP:    
      if customize == True:
        pos = [i//50 for i in pygame.mouse.get_pos()]
        map[pos[1]][pos[0]] = barrier
        pos.reverse()
        render_tile(pos, BARRIER)
  
  FPSCLOCK.tick(FPS)
  pygame.display.update()
