import random
import pygame
pygame.init()
import class_defin

"""For the map generation"""


class mapBlocks():
    """pygame.image.load("graphics/ground.png").convert()"""

    def __init__(self) -> None:
        self.wall = pygame.image.load('Textures/Blocks/Wall.png').convert()
        self.dirt = pygame.image.load('Textures/Blocks/Dirt.png').convert()
        self.space = pygame.image.load('Textures/Blocks/Space.png')
        self.path_1 = pygame.image.load('Textures/Blocks/Path_1.png').convert()
        self.path_2 = pygame.image.load('Textures/Blocks/Path_2.png').convert()
surface = mapBlocks()


# Generating the Matrix for the map
def generateMap(width, height, rooms):
  map = [["."] * width for i in range(height)]
  
  # Number of rooms that are generated are listed here, for pathfinding later on
  rooms_list = [[0, 0]]
  # Initial point for generation
  initial = [1, 1]

  for y in range(1, 6):
    for x in range(1, 6):
      map[y][x] = 3

  # Counter for number of rooms generated    
  roomNumber = 0
  while roomNumber < int(rooms):
    roomHeight = random.randint(6, 15)
    roomWidth = random.randint(6, 15)
    roomX = random.randint(0, width - roomWidth - 1)
    roomY = random.randint(0, height - roomHeight - 1)


    overlaps = False
    for y in range(roomY, roomY + roomHeight):
      for x in range(roomX, roomX + roomWidth):
        if map[y][x] != ".":
          overlaps = True
          break
        if map[y+1][x] != ".":
          overlaps = True
          break
        if map[y+1][x+1] != ".":
          overlaps = True
          break        
        if map[y][x+1] != ".":
          overlaps = True
          break
        if map[y-1][x] != ".":
          overlaps = True
          break
        if map[y-1][x-1] != ".":
          overlaps = True
          break
        if map[y][x-1] != ".":
          overlaps = True
          break

    if not overlaps:
      # Adds the details of the added room with a random point in the room itself
      rooms_list.append([roomX+1 + random.randint(2, roomWidth-2)-1, roomY+1 + random.randint(2, roomHeight-2)-1])
      # Outputs all of the tiles depending on what is needed. 
      for y in range(roomY, roomY + roomHeight):
        for x in range(roomX, roomX + roomWidth):
          map[y][x] = 1 # Dirt
          if y == roomY or (y == roomY + roomHeight-1):
            map[y][x] = 2 # Wall
          if x == roomX or (x == roomX +roomWidth-1):
            map[y][x] = 2
          if map[y][x] == 1 and random.randint(1, 40) == 1:
            map[y][x] = 'S' # Slime
      roomNumber += 1

  # Puts all of the rooms in ascending order of x coordinate
  rooms_list.sort()

  # Iterates through every room
  for i in range(1, len(rooms_list)):
    # Each consecutive room is a start and end
    start = rooms_list[i-1]
    end = rooms_list[i]
    for i in range(start[0], end[0]+1):
      # Checks if the tile is dirt
      # Adds the ocrridors in the x axis
      if map[start[1]][i] != 1:
        map[start[1]][i] = 3
      # If statements to check if second room is above or below
      # the second rooms
      if start[1] < end[1]:
        # Adds the corridors in the y axis
        for i in range(start[1], end[1]+1):
          if map[i][end[0]] != 1:
            map[i][end[0]] = 3
      if start[1] > end[1]:
        for i in range(end[1], start[1]):
          if map[i][end[0]] != 1:
            map[i][end[0]] = 3
  return map


"""room = generateMap(20, 20, 2)
for row in room:
    print(' '.join([str(elem) for elem in row]))"""

def displayMap(test_map, resize, scroll):
    y = 0
    for row in test_map:
        x = 0
        for tile in row:
            if tile == 3: # Inserting a path block
                resize.blit(class_defin.surface.path_1, (x*32 - scroll[0], y*32 - scroll[1]))
            if tile == 1 or tile == 'S': # Inserting dirt
                resize.blit(class_defin.surface.dirt, (x*32 - scroll[0], y*32 - scroll[1]))
            if tile == 2: # Inserting a wall
                resize.blit(class_defin.surface.wall, (x*32 - scroll[0], y*32 - scroll[1]))
                #class_defin.collide.addWall(pygame.Rect(x*32, y*32, 32, 32))
            if tile == ".": # Inserting empty space
                resize.blit(class_defin.surface.space, (x*32 - scroll[0], y*32 - scroll[1]))
            x += 1
        y += 1
