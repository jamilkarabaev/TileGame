import pygame
import random
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
pygame.init()
 
size = (600, 800)
screen = pygame.display.set_mode(size)

all_sprites_list = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
inner_walls_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()

pygame.display.set_caption("Tile Game")

mario = pygame.image.load('mario.png').convert_alpha()
ghost = pygame.image.load('ghost.png').convert_alpha()
wallimg = pygame.image.load('wall2.png')
pipe = pygame.image.load('pipe.png').convert_alpha()




class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = mario
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.health = 300
        self.money = 0
        self.keys = 0
        self.score = 0
        self.damage = random.randrange(5,17,1)
        self.enemy_collision = False
        self.collided_enemy_list = []


    def update(self):
        self.rect.x += self.speed_x
        self.collide_x(walls_group)
        self.collide_x(inner_walls_group)
        self.collide_x(enemy_group)
        self.rect.y += self.speed_y
        self.collide_y(walls_group)
        self.collide_y(inner_walls_group)
        self.collide_y(enemy_group)
        if self.enemy_collision == True:
            self.react_to_enemy()   
        self.display_variables()

    def collide_x(self, spritegroup):

        block_hit_list = pygame.sprite.spritecollide(self, spritegroup, False)
        for block in block_hit_list:
            if self.speed_x > 0:
                self.rect.right = block.rect.left
            elif self.speed_x < 0:
                self.rect.left = block.rect.right

        
        if spritegroup == enemy_group and len(block_hit_list) > 0:
            self.enemy_collision = True
            for obj in block_hit_list:
                if obj in enemy_group:
                    if obj not in self.collided_enemy_list:
                        self.collided_enemy_list.append(obj)

    def collide_y(self, spritegroup):

        block_hit_list = pygame.sprite.spritecollide(self, spritegroup, False)
        for block in block_hit_list:
            if self.speed_y > 0:
                self.rect.bottom = block.rect.top
            elif self.speed_y < 0:
                self.rect.top = block.rect.bottom


        if spritegroup == enemy_group and len(block_hit_list) > 0:
            self.enemy_collision = True
            for obj in block_hit_list:
                if obj in enemy_group:
                    if obj not in self.collided_enemy_list:
                        self.collided_enemy_list.append(obj)

    def react_to_enemy(self):
        for obj in self.collided_enemy_list:
            self.health = self.health - obj.damage
            obj.health = obj.health - self.damage
            print(obj.health)
        if self.health <= 0:
            self.kill()
            player_group.remove(self)
        self.enemy_collision = False

    
    def display_variables(self):
        font = pygame.font.SysFont("serif", 25)
        health = font.render("health: " + str(self.health), True, BLACK)
        screen.blit(health, [20, 600])
        money = font.render("money: " + str(self.money), True, BLACK)
        screen.blit(money, [160, 600])
        keys = font.render("keys: " + str(self.keys), True, BLACK)
        screen.blit(keys, [300, 600])
        score = font.render("score: " + str(self.score), True, BLACK)
        screen.blit(score, [440, 600])

        

playerobject = Player(0,0)
player_group.add(playerobject)
 
ENEMY_COLOUR_ARRAY = [(0, 255, 255), (200, 100, 100), (255, 255, 000)]
r = random.randrange(0, 2, 1)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ghost
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 20
        self.damage = 2

    def update(self):
        self.collide_player(playerobject)

    def collide_player(self, sprite):
        if self.rect.colliderect(sprite.rect):
            self.health = self.health - sprite.damage
        if self.health <= 0:
            all_sprites_list.remove(self)
            enemy_group.remove(self)
            sprite.keys = sprite.keys + 1
        


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = wallimg
        self.rect = self.image.get_rect()
        self.rect.y = x
        self.rect.x = y
        

class InnerWall(Wall):
    def __init__(self, x, y):
        Wall.__init__(self, x , y)



class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe
        self.rect = self.image.get_rect()
        self.rect.y = x
        self.rect.x = y
        self.collided = False
        self.newlevel = False

    def collide_player(self):
        if self.rect.colliderect(playerobject) and self.collided == False:
            self.kill()
            playerobject.score = playerobject.score + 1
            playerobject.keys = 0
            self.collided = True
            self.newlevel = True





Maps = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

FreeSpots = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


def TakeSpots(i, j):


    FreeSpots[i][j] = 1

    if j == 0 and i == 0:
        FreeSpots[i][j+1] = 1
        FreeSpots[i+1][j+1] = 1
        FreeSpots[i+1][j] = 1


    elif j == 14 and i == 0:
        FreeSpots[i][j-1] = 1
        FreeSpots[i+1][j-1] = 1
        FreeSpots[i+1][j] = 1

    elif j == 0 and i == 14:
        FreeSpots[i-1][j] = 1
        FreeSpots[i-1][j+1] = 1
        FreeSpots[i][j+1] = 1
        
        

    elif j == 14 and i == 14:
        FreeSpots[i-1][j] = 1
        FreeSpots[i-1][j-1]
        FreeSpots[i][j-1] = 1 

    elif j == 0:
        FreeSpots[i-1][j] = 1
        FreeSpots[i-1][j+1] = 1
        FreeSpots[i][j+1] = 1
        FreeSpots[i+1][j+1] = 1
        FreeSpots[i+1][j] = 1


    elif j == 14:
        FreeSpots[i-1][j] = 1
        FreeSpots[i-1][j-1] = 1
        FreeSpots[i][j-1] = 1
        FreeSpots[i+1][j-1] = 1
        FreeSpots[i+1][j] = 1
    
    elif i == 0:
        #side
        FreeSpots[i][j+1] = 1
        FreeSpots[i][j-1] = 1

        #bottom
        FreeSpots[i+1][j+1] = 1
        FreeSpots[i+1][j] = 1
        FreeSpots[i+1][j-1] = 1


    elif i == 14:
        #top
        FreeSpots[i-1][j+1] = 1
        FreeSpots[i-1][j] = 1
        FreeSpots[i-1][j-1] = 1

        #side
        FreeSpots[i][j+1] = 1
        FreeSpots[i][j-1] = 1

    else:
        #top
        FreeSpots[i-1][j+1] = 1
        FreeSpots[i-1][j] = 1
        FreeSpots[i-1][j-1] = 1

        #side
        FreeSpots[i][j+1] = 1
        FreeSpots[i][j-1] = 1

        #bottom
        FreeSpots[i+1][j+1] = 1
        FreeSpots[i+1][j] = 1
        FreeSpots[i+1][j-1] = 1

for i in range(len(Maps)):
    for j in range(len(Maps)):
        if Maps[i][j] == 1:
            TakeSpots(i, j)
            wall = Wall(i*40,j*40)
            walls_group.add(wall)

        


def coord_picker():
    Free_x_and_y = []
    for i in range(len(FreeSpots)):
        for j in range(len(FreeSpots)):
            if FreeSpots[i][j] == 0 and FreeSpots[i-1][j+1] == 0 and FreeSpots[i-1][j] == 0 and FreeSpots[i-1][j-1] == 0 and FreeSpots[i][j+1] == 0 and FreeSpots[i][j-1] == 0 and FreeSpots[i+1][j+1] == 0 and FreeSpots[i+1][j] == 0 and FreeSpots[i+1][j-1] == 0:
                Free_x_and_y.append([i,j])
    current_range = len(Free_x_and_y) - 1
    picked_index = random.randrange(0, current_range, 1)
    picked_coordinates = Free_x_and_y[picked_index]
    return picked_coordinates


picked_coords = coord_picker()
inner_wall = InnerWall(picked_coords[1]*40, picked_coords[0]*40)
TakeSpots(picked_coords[0], picked_coords[1])
inner_walls_group.add(inner_wall)

picked_coords2 = coord_picker()
inner_wall2 = InnerWall(picked_coords2[1]*40, picked_coords2[0]*40)
TakeSpots(picked_coords2[0], picked_coords2[1])
inner_walls_group.add(inner_wall2)

player_coords = coord_picker()
playerobject.rect.x = player_coords[1]*40
playerobject.rect.y = player_coords[0]*40
TakeSpots(player_coords[0], player_coords[1])


enemycoord1 = coord_picker()
enemyobject1 = Enemy(enemycoord1[1]*40, enemycoord1[0]*40)
TakeSpots(enemycoord1[0], enemycoord1[1])
enemycoord2 = coord_picker()
enemyobject2 = Enemy(enemycoord2[1]*40, enemycoord2[0]*40)
TakeSpots(enemycoord2[0], enemycoord2[1])
enemycoord3 = coord_picker()
enemyobject3 = Enemy(enemycoord3[1]*40, enemycoord3[0]*40)
TakeSpots(enemycoord3[0], enemycoord3[1])
all_sprites_list.add(enemyobject1, enemyobject2, enemyobject3)
enemy_group.add(enemyobject1, enemyobject2, enemyobject3)


for i in range(len(FreeSpots)):
    for j in range(len(FreeSpots)):
        print(FreeSpots[i][j], end=" ")
    print("")

portalcoords = coord_picker()
portalobject = Portal(portalcoords[1]*40, portalcoords[0]*40)
TakeSpots(portalcoords[0], portalcoords[1])
portal_group.add(portalobject)

 
done = False
clock = pygame.time.Clock()
 
while not done:

    #keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerobject.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                playerobject.speed_x = 5
            elif event.key == pygame.K_UP:
                playerobject.speed_y = -5
            elif event.key == pygame.K_DOWN:
                playerobject.speed_y = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerobject.speed_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerobject.speed_y = 0
    
    screen.fill(WHITE)
    all_sprites_list.draw(screen)
    inner_walls_group.draw(screen)
    walls_group.draw(screen)
    player_group.draw(screen)


    playerobject.update()
    for enemy in enemy_group:
        enemy.update()
    if playerobject.keys >= 2:
        portalobject.collide_player()
        portal_group.draw(screen)
    if portalobject.newlevel == True:
        all_sprites_list.empty()
        portal_group.empty()
        inner_walls_group.empty()

        FreeSpots = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


        picked_coords = coord_picker()
        inner_wall = InnerWall(picked_coords[0]*40, picked_coords[1]*40)
        TakeSpots(picked_coords[0], picked_coords[1])
        inner_walls_group.add(inner_wall)

        picked_coords2 = coord_picker()
        inner_wall2 = InnerWall(picked_coords2[0]*40, picked_coords2[1]*40)
        TakeSpots(picked_coords2[0], picked_coords2[1])
        inner_walls_group.add(inner_wall2)

        player_coords = coord_picker()
        playerobject.rect.x = player_coords[1]*40
        playerobject.rect.y = player_coords[0]*40
        TakeSpots(player_coords[0], player_coords[1])


        
        enemycoord1 = coord_picker()
        enemyobject1 = Enemy(enemycoord1[1]*40, enemycoord1[0]*40)
        TakeSpots(enemycoord1[0], enemycoord1[1])
        enemycoord2 = coord_picker()
        enemyobject2 = Enemy(enemycoord2[1]*40, enemycoord2[0]*40)
        TakeSpots(enemycoord2[0], enemycoord2[1])
        enemycoord3 = coord_picker()
        enemyobject3 = Enemy(enemycoord3[1]*40, enemycoord3[0]*40)
        TakeSpots(enemycoord3[0], enemycoord3[1])
        all_sprites_list.add(enemyobject1, enemyobject2, enemyobject3)
        enemy_group.add(enemyobject1, enemyobject2, enemyobject3)


        portalcoords = coord_picker()
        portalobject = Portal(portalcoords[1]*40, portalcoords[0]*40)
        TakeSpots(portalcoords[0], portalcoords[1])
        portal_group.add(portalobject)

        portalobject.newlevel = False

    if playerobject.health <= 0:
        done = True
        
        



    pygame.display.flip()
    clock.tick(60)
pygame.quit()