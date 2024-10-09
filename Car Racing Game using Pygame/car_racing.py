import random
from time import sleep
import pygame
from pathlib import Path

class CarRacing:
    def __init__(self):  
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.root_path = str(Path(__file__).parent)

        self.initialize()

    def initialize(self):
        self.crashed = False
        self.score = 0
        self.carImg = pygame.image.load(self.root_path + "/img/car.png")
        self.car_x_coordinate = self.display_width * 0.45
        self.car_y_coordinate = self.display_height * 0.8
        self.car_width = 49
        self.enemy_car_speed = 5  # Starting speed
        self.enemy_car = pygame.image.load(self.root_path + "/img/enemy_car_1.png")
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_width = 49
        self.enemy_car_height = 100
        self.bgImg = pygame.image.load(self.root_path + "/img/back_ground.jpg")
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3

    def car(self):
        self.gameDisplay.blit(self.carImg, (self.car_x_coordinate, self.car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Race -- Anuj')
        self.run_car()

    def run_car(self):
        while not self.crashed:
            self.handle_events()
            self.update_game_state()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.car_x_coordinate = max(self.car_x_coordinate - 50, 310)  # Prevent going out of bounds
                if event.key == pygame.K_RIGHT:
                    self.car_x_coordinate = min(self.car_x_coordinate + 50, 460)  # Prevent going out of bounds

    def update_game_state(self):
        self.enemy_car_starty += self.enemy_car_speed
        if self.enemy_car_starty > self.display_height:
            self.reset_enemy_car()

        self.check_collisions()

    def reset_enemy_car(self):
        self.enemy_car_starty = 0 - self.enemy_car_height
        self.enemy_car_startx = random.randrange(310, 450)

    def check_collisions(self):
        if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
            if (self.car_x_coordinate > self.enemy_car_startx and 
                self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width) or \
               (self.car_x_coordinate + self.car_width > self.enemy_car_startx and 
                self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width):
                self.crashed = True
                self.display_message("Game Over !!!")
        
        if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
            self.crashed = True
            self.display_message("Game Over !!!")

    def render(self):
        self.gameDisplay.fill(self.black)
        self.back_ground_road()
        self.car()
        self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
        self.highscore(self.score)
        self.score += 1
        if self.score % 100 == 0:  # Increase difficulty every 100 points
            self.enemy_car_speed += 1
            self.bg_speed += 1
        pygame.display.update()

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        self.initialize()  # Reset game variables
        self.racing_window()  # Restart game

    def back_ground_road(self):
        bg_x = (self.display_width - self.bgImg.get_width()) // 2  # Calculate x position to center
        self.gameDisplay.blit(self.bgImg, (bg_x, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (bg_x, self.bg_y2))
        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -self.bgImg.get_height()

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -self.bgImg.get_height()

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        credits = [
            "Thanks & Regards,",
            "Anuj Kumar",
            "cdac.anuj@gmail.com"
        ]
        for idx, line in enumerate(credits):
            text = font.render(line, True, self.white)
            self.gameDisplay.blit(text, (600, 520 + idx * 20))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
