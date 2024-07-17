import pygame 
import os
from enum import Enum 
import random 

pygame.init() 

WINDOW_HEIGHT: int = 600
WINDOW_WIDTH: int = 1100 

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class DinosaurActions(Enum): 
    RUN = "running"
    JUMP = "jumping"
    DUCK = "ducking"

class Dinosaur: 
    X_POSITION = 80
    RUNNING_Y_POSITION = 310 
    DUCKING_Y_POSITION  = 340
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
        self.image: pygame.Surface = Dinosaur.RUNNING_SPRITES[0]

        self.sprite_rect = self.image.get_rect() 
        self.sprite_rect.x = Dinosaur.X_POSITION
        self.sprite_rect.y = Dinosaur.RUNNING_Y_POSITION 
           
        self.jump_velocity = Dinosaur.MAX_JUMP_VELOCITY         
        self.dino_jump = False 

        self.step_index: int = 0 

    def update_action(self) -> None: 
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
        
    def set_action(self, userInput) -> None: 
        if userInput[pygame.K_UP] and self.action != DinosaurActions.JUMP: 
            self.action = DinosaurActions.JUMP

        elif userInput[pygame.K_DOWN] and self.action != DinosaurActions.JUMP: 
            self.action = DinosaurActions.DUCK

        elif not (self.action == DinosaurActions.JUMP or userInput[pygame.K_DOWN]): 
            self.action = DinosaurActions.RUN 

    def jump(self) -> None: 
        self.image = Dinosaur.JUMPING_SPRITE
       
        if self.dino_jump:
            self.sprite_rect.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
       
        if self.jump_velocity < -1 * Dinosaur.MAX_JUMP_VELOCITY:            
            self.sprite_rect.y = Dinosaur.RUNNING_Y_POSITION
            self.action = DinosaurActions.RUN
            self.dino_jump = False

            self.jump_velocity = Dinosaur.MAX_JUMP_VELOCITY

    def run(self) -> None: 
        self.image = Dinosaur.RUNNING_SPRITES[self.step_index // 5]
        self.sprite_rect = self.image.get_rect() 
        self.sprite_rect.x = Dinosaur.X_POSITION
        self.sprite_rect.y = Dinosaur.RUNNING_Y_POSITION         
        self.step_index += 1

    def duck(self) -> None:
        self.image = Dinosaur.DUCKING_SPRITES[self.step_index // 5]
        self.sprite_rect = self.image.get_rect() 
        self.sprite_rect.x = Dinosaur.X_POSITION
        self.sprite_rect.y = Dinosaur.DUCKING_Y_POSITION      
        self.step_index += 1 

    def draw(self) -> None: 
        WINDOW.blit(self.image, (self.sprite_rect.x, self.sprite_rect.y))

class Cloud: 
    SPRITE = pygame.image.load(os.path.join("Cloud.png"))

    def __init__(self): 
        self.x = WINDOW_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.width = self.image.get_width() 
        self.image = Cloud.SPRITE 

    def update(self) -> None: 
        self.x -= Score.game_speed
        if self.x < -self.width: 
            self.x = WINDOW_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)
    
    def draw(self) -> None: 
        WINDOW.blit(self.image, (self.x, self.y))

class Background: 
    SPRITE = pygame.image.load(os.path.join("Track.png"))
    IMAGE_WIDTH = SPRITE.get_width()

    def __init__(self): 
        self.image = Background.SPRITE 
        self.x = 0 
        self.y = 380 

    def draw(self) -> None: 
        WINDOW.blit(self.image, (self.x, self.y))
        WINDOW.blit(self.image, (self.x + Background.IMAGE_WIDTH, self.y))
        
        if self.x <= -1 * Background.IMAGE_WIDTH: 
            WINDOW.blit(self.image, (self.x + Background.IMAGE_WIDTH, self.y))
            self.x = 0 
        
        self.x -= Score.game_speed

class Score: 
    FONT = pygame.font.Font("freesansbold.ttf", 20)
    game_speed = 10
    points = 0 

    @classmethod
    def increase_game_speed(cls):
        if Score.points % 100 == 0: 
            Score.game_speed += 1 
    
    @classmethod
    def manage_points(cls): 
        Score.points += 1
        
        text = Score.FONT.render("Points: " + str(Score.points), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        WINDOW.blit(text, text_rect)

class Obstacle: 
    def __init__(self, image, type: int): 
        self.image = image 
        self.type = type 
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WINDOW_WIDTH
    
    def update(self) -> None: 
        self.rect.x -= Score.game_speed
        if self.rect.x < -self.rect.width: 
            obstacles.remove(self)

    def draw(self) -> None: 
        WINDOW.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle): 
    SPRITES = (
        pygame.image.load(os.path.join("SmallCactus1.png")), 
        pygame.image.load(os.path.join("SmallCactus2.png")), 
        pygame.image.load(os.path.join("SmallCactus3.png"))
    )
    
    def __init__(self): 
        self.type = random.randint(0, 2)
        super().__init__(SmallCactus.SPRITES, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle): 
    SPRITES = (
        pygame.image.load(os.path.join("LargeCactus1.png")), 
        pygame.image.load(os.path.join("LargeCactus2.png")), 
        pygame.image.load(os.path.join("LargeCactus3.png"))
    )
    
    def __init__(self): 
        self.type = random.randint(0, 2)
        super().__init__(LargeCactus.SPRITES, self.type)
        self.rect.y = 300
    
class Bird(Obstacle): 
    SPRITES = (
        pygame.image.load(os.path.join("Bird1.png")), 
        pygame.image.load(os.path.join("Bird2.png"))
    )
    
    def __init__(self): 
        self.type = 0 
        super().__init__(Bird.SPRITES, self.type)
        self.rect.y = random.randint(200, 300)
        self.index = 0
    
    def draw(self) -> None: 
        if self.index >= 10: 
            self.index = 0 
        WINDOW.blit(Bird.SPRITES[self.index // 5], self.rect)
        self.index += 1 

obstacles: list[Obstacle] = []

def add_obstacles() -> None: 
    if len(obstacles) == 0 or obstacles[-1].rect.x < 0: 
        random_obstacle: int = random.randint(0, 2)

        if random_obstacle == 0: 
            obstacles.append(SmallCactus())
        
        elif random_obstacle == 1: 
            obstacles.append(LargeCactus())
        
        else: 
            obstacles.append(Bird())


FPS: int = 60 

def main() -> None: 
    run = True 
    Score.points = 0 
    death_count = 0 
    
    clock = pygame.time.Clock() 
    player = Dinosaur()
    cloud = Cloud() 
    background = Background()
    
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
        
        add_obstacles()

        for obstacle in obstacles: 
            obstacle.draw()
            obstacle.update()
            if player.sprite_rect.colliderect(obstacle.rect): 
                death_count += 1 
                menu(death_count)

        clock.tick(FPS)
        pygame.display.update() 

def menu(death_count: int): 
    run = True 
    while run: 
        WINDOW.fill((255, 255, 255))
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0: 
            text = font.render("Press any Key to Start", True, (0, 0, 0))
       
        elif death_count > 0: 
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            
            score = font.render("Your Score: " + str(Score.points), True, (0, 0, 0))
            score_rect = score.get_rect()
            score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50) 
            WINDOW.blit(score, score_rect)

        text_rect = text.get_rect() 
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        WINDOW.blit(text, text_rect)
        
        WINDOW.blit(Dinosaur.RUNNING_SPRITES[0], (WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT // 2 - 140))
        pygame.display.update() 

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
            
            if event.type == pygame.KEYDOWN: 
                main() 
                break

menu(death_count = 0)
