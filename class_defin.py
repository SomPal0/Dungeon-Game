# ALL CLASS DEFINITIONS
import pygame
pygame.init()



"""For collision detection"""
class collisions():
    def __init__(self) -> None:
        self.walls_list = []
        self.enemy_list = []


    # To check if a collision has occured between any rectangle, and any walll on the map
    def collide_check(self, rect):
        #print(len(self.walls_list))
        list_of_collisions = [] # Where all the walls will go if they collide with the player
        for tile in self.walls_list:
            if rect.colliderect(tile):
                list_of_collisions.append(tile)
        return list_of_collisions
    
    # To check if the player has collided with any enemies
    def hit_check(self, rect):
        list_of_collisions = []
        for enemy in self.enemy_list:
            if rect.colliderect(enemy):
                list_of_collisions.append(enemy)
        return list_of_collisions

    def addWall(self, wall):
        self.walls_list.append(wall)

    def reset(self):
        self.walls_list = []
    
    def addEnemy(self, enemy):
        self.enemy_list.append(enemy)

collide = collisions()


""" For items"""


class DamageItems():
    def __init__(self, type: bool, damage: int):
        """Only 2 types. Radial and Projectile
            radial = True
            projectile = False"""
        self.type = type
        self.damage = damage
        self.ammo = int

    def attack(self):
        pass  # Deal with this later


baseGun = DamageItems(False, 20)
pulseField = DamageItems(True, 10)


class Melee():
    def __init__(self):
        self.damage = 10
        self.model = pygame.image.load('Textures/Items/Melee.png')
        self.delay = 500  # Delay between swings in-game measured in ms (?)

    def attack():
        pass
        """In later versions, this will be defined, however the essense
        is that damage is dealt, and a small animation is displayed"""


hammer = Melee()  # Making Class instance in this document to avoid clutter.


class ItemProjectile():
    def __init__(self, damage: int, PosX: int, PosY: int):
        self.speed = int
        self.damage = damage
        self.X = PosX
        self.Y = PosY

    def move(self, PosX, PosY):
        """This will be decided on later on. Not sure about the exact implementation"""
        self.X = PosX
        self.Y = PosY


class OtherItems():
    def __init__(self):
        pass


"""Class for the Main Player"""


class Player():
    def __init__(self):
        self.health = 100  # Define the players health later
        self.melee_damage = 10
        self.player_items = [hammer]

        # Number of pixels moved each frame
        self.speed = 1
        self.normal_speed = 1 # Normal speed
        self.dash_speed = 5 # Speed when dashing

        self.dash_timer = 29 # 20 frames of motion
        self.dash_timer_constant = 29
        self.dash_cool_timer = 0 # Cool down after a dash
        self.cooldown_constant = 120



        self.itemIndex = int  # Index of the self.player_items list, for inventory management
        # Image of player
        self.sprite = pygame.image.load('Textures/Entities/Player.png').convert()
        # Coordinates of Player
        self.X = 50 #350
        self.Y = 50 # 200
        self.sprite_rect = self.sprite.get_rect(topleft=(self.X, self.Y))
        # For player movement. Helps identify which direction collision has occured from such that respective movment can be stopped 
        self.collision_type = {'top': False,
                               'bottom': False, 'right': False, 'left': False}
        # Rectangle that adds the players health to the screen
        self.health_rect = pygame.Rect(50, 750, self.health*3, 25)


    def item_add(self, item):
        weapon = item
        if len(self.player_items) <= 3:
            self.player_items.append(weapon)
        else:
            pass  # For now, pass through this line of code. In later versions, will output a message

    

    def meleeUpdate(self, newDamage):
        self.melee_damage = newDamage

    def move(self, keys):  # For moving the player image
        # Variable for the type of collision 
        self.collision_type = {'top': False,
                               'bottom': False, 'right': False, 'left': False}
        
        if keys[pygame.K_LSHIFT]:
            # When both the cool downs are finished, you can dash
            if self.dash_timer <= 0 and self.dash_cool_timer <= 0:
                self.speed = self.dash_speed
                self.dash_timer = self.dash_timer_constant
                self.dash_cool_timer = self.cooldown_constant

        # To cound down and reset the speed
        if self.dash_timer > 0:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.speed = self.normal_speed
                self.dash_cool_timer == 600
        # Counting down the cooldown
        if self.dash_cool_timer > 0:
            self.dash_cool_timer -= 1

        movement = [0, 0]
        if keys[pygame.K_a]:   # A
            movement[0] = -self.speed
        if keys[pygame.K_d]:   # D
            movement[0] = self.speed

        self.sprite_rect.x += movement[0]
        hitlist = collide.collide_check(self.sprite_rect)

        for tile in hitlist:
            if movement[0] > 0:
                self.sprite_rect.right = tile.left
                self.collision_type['right'] = True
            if movement[0] < 0:
                self.sprite_rect.left = tile.right
                self.collision_type['left'] = True

        if keys[pygame.K_s]:   # S
            movement[1] = self.speed
        if keys[pygame.K_w]:   # W
            movement[1] = -self.speed
        
        self.sprite_rect.y += movement[1]
        hitlist = collide.collide_check(self.sprite_rect)

        for tile in hitlist:
            if movement[1] > 0:
                self.sprite_rect.bottom = tile.top
                self.collision_type['bottom'] = True
            if movement[1] < 0:
                self.sprite_rect.top = tile.bottom
                self.collision_type['top'] = True
    def healthUpdate(self):
        hitlist = collide.hit_check(self.sprite_rect)
        for enemy in hitlist:
            self.health -= enemy.damage
        self.health_rect = pygame.Rect(50, 750, self.health*3, 25)

    # Display the sprite onto the screen resize screen, as well as the 
    # health bar to the big screen
    def draw(self, small_screen, scroll, big_screen):
        small_screen.blit(self.sprite, (self.sprite_rect.x - scroll[0], self.sprite_rect.y - scroll[1]))
        #pygame.draw(big_screen, (255, 0, 0), self.health_rect)
        
    def speedUpdate(self, newSpeed):
        # To update both dash speed, and normal speed, with just one input. This will change depending
        self.dash_speed = (newSpeed/self.speed) * self.dash_speed
        self.speed = newSpeed

    # Different to above, in that it adds speed rather than changing the base stat.
    def speedAdd(self, speedAdd):
        self.speed += speedAdd
        self.dash_speed += 4 * speedAdd
    

    # General code for updating the player
    def update(self, keys, small_screen, scroll, big_screen):
        player.move(keys)
        player.draw(small_screen, scroll, big_screen)



# Makes the class for the main document
player = Player()

""" For the enemy"""


class Enemy():
    def __init__(self, health, type, tick, speed, damage, model, pos):
        self.health = health
        """Specifics will be decided later, on what string is what. I know its bad coding."""
        self.damageType = type
        self.damageTick = tick
        self.speed = speed
        self.damage = damage
        # Coordinates of enemy
        self.X = pos[0]
        self.Y = pos[1]
        self.enemy_model = 0  # Should be an image from pygame

    def move(self, PosX, PosY):
        self.X += PosX
        self.Y += PosY

    def setHealth(self, newHealth):
        self.health = newHealth

    def setDamageType(self, newType):
        self.damageType(self, newType)

    def setSpeed(self, newSpeed):
        self.speed = newSpeed

    def setDamageValue(self, newDamage):
        self.damage = newDamage

    def setEnemyModel(self, model):
        self.enemy_model = model

    def attack(self):
        pass  # deal with later


class Slime():
    def __init__(self, x, y):
        self.X = x*32 # Position on the screen. 32 is the tilesize
        self.Y = y*32
        self.sprite = pygame.image.load('Textures/Entities/Slime.png').convert_alpha()
        self.sprite_rect = self.sprite.get_rect(topleft=(self.X, self.Y))
        self.speed = 1.5
        self.damage = 1
     
    def draw(self, small_screen, scroll): # To display the monster
        small_screen.blit(self.sprite, (self.X - scroll[0], self.Y - scroll[1]))
    
    # To move the monster towards the player
    def move(self, player_rect):
        vector = pygame.Vector2()
        vector.x = player_rect.centerx - self.sprite_rect.centerx
        vector.y = player_rect.centery - self.sprite_rect.centery
        print("Difference is: " + str(vector))
        vector = vector.normalize()
        print("Unit Vector: " + str(vector))
        vector = vector * self.speed
        print("speed Vector: " + str(vector))
        vector.x = int(vector.x)
        vector.y = int(vector.y)
        self.X += vector.x
        self.Y += vector.y


    def update(self, small_screen, scroll, player_rect):
        #self.move(player_rect)
        self.draw(small_screen, scroll)




        


class MonsterProjectile():
    def __init__(self):
        self.damage = int
        self.X = int
        self.Y = int

    def move(self, PosX, PosY):
        self.X = PosX
        self.Y = PosY


class Monster(Enemy):
    def __init__(self):
        super().__init__()


class Boss(Enemy):
    def __init__(self):
        super().__init__()


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

        
