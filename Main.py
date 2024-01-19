import pygame          # Imports pygame library
from sys import exit   # To quit the execution of the programme from the display itself


pygame.init()  # Initialising pygame library
clock = pygame.time.Clock()  # clock value for game ticks
pygame.display.set_caption('Dungeon Crawler')  # Sets the window caption

# Initialises a screen for the images to be displayed onto.
# It is a resizable window, meaning that it can be changed once opened.
window_size = (1500, 800)
screen = pygame.display.set_mode(window_size)
resize = pygame.Surface((750, 400)) 

# More Imports after the pygame library has been initialised with a proper display
import class_defin     # From file class_defin.py
import mapMatrixGeneration


white = (255, 255, 255)

font = pygame.font.Font('Monocraft.ttf', 16)
move_text = font.render('Use: W, A, S, D and Shift to move', True, white)
move_text_rect = move_text.get_rect()
move_text_rect.center = (4*1500/5, 30)

levelOne = True     # Initialises which game mode is being played 
test_map = mapMatrixGeneration.generateMap(50, 50, 10)

for row in test_map:
    print(' '.join([str(elem) for elem in row]))
mainMenu = True
"""test_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'S']
]   """

scroll = [0, 0]

x = 0
y = 0

# Initiates the monsters needed in the map
for row in test_map:
    x = 0
    for tile in row:
        if tile == 'S': # Adds the slime to the list of enemies
            class_defin.collide.addEnemy(class_defin.Slime(x,y))

        if tile == 2:
            class_defin.collide.addWall(pygame.Rect(x*32, y*32, 32, 32))
        
        if tile == ".":
            class_defin.collide.addWall(pygame.Rect(x*32, y*32, 32, 32))
        x += 1
    y += 1


# Main Game
while levelOne == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quits the game on pressing the cross button.
            pygame.quit()
            exit()
    resize.fill((0, 0, 0))
    scroll[0] += (class_defin.player.sprite_rect.x - scroll[0] - 325 - 9)/40
    scroll[1] += (class_defin.player.sprite_rect.y - scroll[1] - 200 - 10)/25
    
    keys = pygame.key.get_pressed()

    mapMatrixGeneration.displayMap(test_map, resize, scroll)


    # Updating all the classes

    
    for object in class_defin.collide.enemy_list: # Enemies
        object.update(resize, scroll, class_defin.player.sprite_rect)
    class_defin.player.update(keys, resize, scroll, screen) # Player
    temp_surf = pygame.transform.scale(resize, window_size)
    screen.blit(temp_surf, (0, 0))
    screen.blit(move_text, move_text_rect)

    pygame.display.update()
    clock.tick(120)




