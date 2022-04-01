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
