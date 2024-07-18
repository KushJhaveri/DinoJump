import pygame
import os
from enum import Enum
import random

pygame.init()

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1100

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dinosaur Game")

class DinosaurActions(Enum):
    RUN = "running"
    JUMP = "jumping"
    DUCK = "ducking"

class Dinosaur:
    X_POSITION = 80
    RUNNING_Y_POSITION = 310
    DUCKING_Y_POSITION = 340
    MAX_JUMP_VELOCITY = 8.5
    
    JUMPING_SPRITE = pygame.image.load(os.path.join("DinoJump.png"))

    RUNNING_SPRITES = (
        pygame.image.load(os.path.join("DinoRun1.png")),
        pygame.image.load(os.path.join("DinoRun2.png"))
    )

    DUCKING_SPRITES = (
        pygame.image.load(os.path.join("DinoDuck1.png")),
        pygame.image.load(os.path.join("DinoDuck2.png"))
    )

    def __init__(self):
        self.action = DinosaurActions.RUN
        self.image = Dinosaur.RUNNING_SPRITES[0]

        self.sprite_rect = self.image.get_rect()
        self.sprite_rect.x = Dinosaur.X_POSITION
        self.sprite_rect.y = Dinosaur.RUNNING_Y_POSITION
           
        self.jump_velocity = Dinosaur.MAX_JUMP_VELOCITY         
        self.dino_jump = False

        self.step_index = 0

    def update_action(self):
        if self.action == DinosaurActions.RUN:
            self.dino_jump = False
            self.run()
       
        elif self.action == DinosaurActions.JUMP:
            self.dino_jump = True
            self.jump()
        
        elif self.action == DinosaurActions.DUCK:
            self.dino_jump = False
            self.duck()

        if self.step_index >= 10:
            self.step_index = 0
        
    def set_action(self, userInput):
        if userInput[pygame.K_UP] and self.action != DinosaurActions.JUMP:
            self.action = DinosaurActions.JUMP

        elif userInput[pygame.K_DOWN] and self.action != DinosaurActions.JUMP:
            self.action = DinosaurActions.DUCK

        elif not (self.action == DinosaurActions.JUMP or userInput[pygame.K_DOWN]):
            self.action = DinosaurActions.RUN

    def jump(self):
        self.image = Dinosaur.JUMPING_SPRITE
       
        if self.dino_jump:
            self.sprite_rect.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
       
        if self.jump_velocity < -1 * Dinosaur.MAX_JUMP_VELOCITY:
            self.sprite_rect.y = Dinosaur.RUNNING_Y_POSITION
            self.action = DinosaurActions.RUN
            self.dino_jump = False

            self.jump_velocity = Dinosaur.MAX_JUMP_VELOCITY
            
    def run(self):
        self.image = Dinosaur.RUNNING_SPRITES[self.step_index // 5]
        self.sprite_rect = self.image.get_rect()
        self.sprite_rect.x = Dinosaur.X_POSITION
        self.sprite_rect.y = Dinosaur.RUNNING_Y_POSITION
        self.step_index += 1

    def duck(self):
        self.image = Dinosaur.DUCKING_SPRITES[self.step_index // 5]
        self.sprite_rect = self.image.get_rect()
        self.sprite_rect.x = Dinosaur.X_POSITION
        self.sprite_rect.y = Dinosaur.DUCKING_Y_POSITION
        self.step_index += 1

    def draw(self):
        WINDOW.blit(self.image, (self.sprite_rect.x, self.sprite_rect.y))

class Cloud:
    SPRITE = pygame.image.load(os.path.join("Cloud.png"))

    def __init__(self):
        self.x = WINDOW_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = Cloud.SPRITE
        self.width = self.image.get_width()

    def update(self):
        self.x -= Score.game_speed
        if self.x < -self.width:
            self.x = WINDOW_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
    
    def draw(self):
        WINDOW.blit(self.image, (self.x, self.y))

class Background:
    SPRITE = pygame.image.load(os.path.join("Track.png"))
    IMAGE_WIDTH = SPRITE.get_width()

    def __init__(self):
        self.image = Background.SPRITE
        self.x = 0
        self.y = 380

    def draw(self):
        WINDOW.blit(self.image, (self.x, self.y))
        WINDOW.blit(self.image, (self.x + Background.IMAGE_WIDTH, self.y))
        
        if self.x <= -1 * Background.IMAGE_WIDTH:
            WINDOW.blit(self.image, (self.x + Background.IMAGE_WIDTH, self.y))
            self.x = 0
        
        self.x -= Score.game_speed

class Score:
    FONT = pygame.font.Font("freesansbold.ttf", 20)
    STARTING_GAME_SPEED = 10
    game_speed = STARTING_GAME_SPEED
    MAXIMUM_GAME_SPEED = 15
    points = 0

    @classmethod
    def reset(cls):
        cls.game_speed = 10
        cls.points = 0

    @classmethod
    def increase_game_speed(cls):
        if Score.points % 100 == 0 and Score.game_speed < Score.MAXIMUM_GAME_SPEED:
            Score.game_speed += 1
    
    @classmethod
    def manage_points(cls):
        Score.points += 1
        
        text = Score.FONT.render("Points: " + str(Score.points), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        WINDOW.blit(text, text_rect)

class Obstacle:
    def __init__(self, image, type):
        self.image = image[self.type]
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH
    
    def update(self):
        self.rect.x -= Score.game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self):
        WINDOW.blit(self.image, self.rect)
        pygame.draw.rect(WINDOW, (255, 0, 0), self.rect, 2)

class SmallCactus(Obstacle):
    HIT_BOX_SCALING = 0.85

    SPRITES = (
        pygame.image.load(os.path.join("SmallCactus1.png")),
        pygame.image.load(os.path.join("SmallCactus2.png")),
        pygame.image.load(os.path.join("SmallCactus3.png"))
    )
    
    def __init__(self):
        self.type = random.randint(0, 2)
        super().__init__(SmallCactus.SPRITES, self.type)
        self.rect.y = 325
        self.rect.width = int(self.rect.width * SmallCactus.HIT_BOX_SCALING)
        self.rect.height = int(self.rect.height * SmallCactus.HIT_BOX_SCALING)
        
class LargeCactus(Obstacle):
    HIT_BOX_SCALING = 0.7

    SPRITES = (
        pygame.image.load(os.path.join("LargeCactus1.png")),
        pygame.image.load(os.path.join("LargeCactus2.png")),
        pygame.image.load(os.path.join("LargeCactus3.png"))
    )
    
    def __init__(self):
        self.type = random.randint(0, 2)
        super().__init__(LargeCactus.SPRITES, self.type)
        self.rect.y = 300
        self.rect.width = int(self.rect.width * LargeCactus.HIT_BOX_SCALING)
        self.rect.height = int(self.rect.height * LargeCactus.HIT_BOX_SCALING)
        
class Bird(Obstacle):
    HIT_BOX_SCALING = 0.85

    SPRITES = (
        pygame.image.load(os.path.join("Bird1.png")),
        pygame.image.load(os.path.join("Bird2.png"))
    )
    
    def __init__(self):
        self.type = 0
        super().__init__(Bird.SPRITES, self.type)
        self.rect.y = random.randint(200, 300)
        self.rect.width = int(self.rect.width * Bird.HIT_BOX_SCALING)
        self.rect.height = int(self.rect.height * Bird.HIT_BOX_SCALING)
        self.index = 0
    
    def draw(self):
        if self.index >= 10:
            self.index = 0
        WINDOW.blit(Bird.SPRITES[self.index // 5], self.rect)
        self.index += 1

obstacles = []
    
def add_obstacles():
    global obstacles
    min_distance = max(400, 700 - Score.points) 

    # Ensure there are at most 3 obstacles on the field
    if len(obstacles) < 3:
        # Check spacing between last obstacle and right edge of window
        if len(obstacles) == 0 or obstacles[-1].rect.x < WINDOW_WIDTH - min_distance:
            random_obstacle = random.randint(0, 2)

            if random_obstacle == 0:
                obstacles.append(SmallCactus())
            
            elif random_obstacle == 1:
                obstacles.append(LargeCactus())
            
            else:
                obstacles.append(Bird())

FPS = 60

def reset_enviorment() -> None: 
    global clock, player, cloud, background, game_data
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    background = Background()
    Score.reset()
    game_data = GameData()

def main() -> None:
    run = True
    death_count = 0
    
    clock = pygame.time.Clock() 
    player.__init__() 
    cloud.__init__() 
    background.__init__()
    Score.reset()
    obstacles = []
    game_data.__init__()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        WINDOW.fill((255, 255, 255))
        
        player.draw()
        player.update_action()
        player.set_action(pygame.key.get_pressed())

        cloud.draw()
        cloud.update()

        background.draw()

        Score.increase_game_speed()
        Score.manage_points()
        game_data.update()

        add_obstacles()

        for obstacle in obstacles:
            obstacle.draw()
            obstacle.update()
            if player.sprite_rect.colliderect(obstacle.rect):
                death_count += 1
                game_data.normalize_data()
                run = False 

        clock.tick(FPS)
        pygame.display.update()
