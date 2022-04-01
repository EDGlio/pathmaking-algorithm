import numpy as np
import showMaps

# 100 - not done (empty)
# 200 - obstacle/barrier

# Define variables
empty = 500
barrier = 1000
endPos = (6, 6)

# Sample map
map = [
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, barrier, empty, empty, empty, empty, empty],
  [empty, empty, barrier, empty, empty, empty, empty, empty],
  [empty, empty, barrier, empty, empty, empty, empty, empty],
  [empty, empty, barrier, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty],
  [empty, empty, empty, empty, empty, empty, 0, empty],
  [empty, empty, empty, empty, empty, empty, empty, empty]
]

# finds path using heat map
def find_path(heat_map, start_pos):
  run = True
  # current position
  current_pos = start_pos

  # path that will be appended to
  path = [current_pos]
  current_val = map[current_pos[1]][current_pos[0]]
  while run:
    for i in range(1):
      try:
        if map[current_pos[0] + 1][current_pos[1]] == current_val - 1:
          current_pos = [current_pos[0] + 1, current_pos[1]]
          current_val = map[current_pos[0]][current_pos[1]]
          break

        if map[current_pos[0] - 1][current_pos[1]] == current_val - 1:
          current_pos = [current_pos[0] - 1, current_pos[1]]
          current_val = map[current_pos[0]][current_pos[1]]
          break

        if map[current_pos[0]][current_pos[1] + 1] == current_val - 1:
          current_pos = [current_pos[0], current_pos[1] + 1]
          current_val = map[current_pos[0]][current_pos[1]]
          break
        
        if map[current_pos[0]][current_pos[1] - 1] == current_val - 1:
          current_pos = [current_pos[0], current_pos[1] - 1]
          current_val = map[current_pos[0]][current_pos[1]]
          break
          
      except: pass
    path.append(current_pos)
    if current_val == 0:
      run = False
    #print(path)
  return path

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
    pairs_to_check = new_pairs.copy()
    if not any(empty in x for x in map):
      run = False
  return map
