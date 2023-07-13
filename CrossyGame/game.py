import pygame
from gameobject import GameObject
from player import Player
from enemy import Enemy

class Game:

    def __init__(self):
        self.width = 720
        self.height = 720
        self.white_colour = (255, 255, 255)

        # Game Code
        self.game_window = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.background = GameObject(0, 0, self.width, self.height, 'assets/background.png')
        self.treasure = GameObject(335, 75, 50, 50, 'assets/treasure.png')
        self.level = 1.0
        self.reset_map()

    def reset_map(self):
        default_speed = 1
        self.enemy_speed = 10
        speed = default_speed + (self.level * 2.5)
        self.player = Player(335, 640, 50, 50, 'assets/player.png', 10)
        if self.level >= 6.0:
            default_speed = 3
            speed = default_speed + (self.level * 2.5)
            self.enemies = [
                Enemy(50, 525, 50, 50, 'assets/enemy.png', speed),
                Enemy(550, 360, 50, 50, 'assets/enemy.png', speed),
                Enemy(50, 180, 50, 50, 'assets/enemy.png', speed)
            ]
        elif self.level >= 4.0:
            default_speed = 2
            speed = default_speed + (self.level * 2.5)
            self.enemies = [
                Enemy(550, 525, 50, 50, 'assets/enemy.png', speed),
                Enemy(50, 150, 50, 50, 'assets/enemy.png', speed)
            ]
        elif self.level >= 2.0:
            speed = default_speed + (self.level * 2.5)
            self.enemies = [
                Enemy(50, 525, 50, 50, 'assets/enemy.png', speed),
                Enemy(600, 360, 50, 50, 'assets/enemy.png', speed)
            ]
        else:
            self.enemies = [                 
                Enemy(50, 525, 50, 50, 'assets/enemy.png', speed) 
            ]

    def update_display(self):
        self.game_window.fill(self.white_colour)
        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        self.game_window.blit(self.treasure.image, (self.treasure.x, self.treasure.y))
        self.game_window.blit(self.player.image, (self.player.x, self.player.y))

        for enemy in self.enemies:
            self.game_window.blit(enemy.image, (enemy.x, enemy.y))
        pygame.display.update()

    def move_objects(self, player_direction):
        self.player.move(player_direction, self.height)
        for enemy in self.enemies:
            enemy.move(self.width)

    def detect_collision(self, object1, object2):
        if object1.y > (object2.y + object2.height):
            return False
        elif (object1.y + object1.height) < object2.y:
            return False
        
        if object1.x > (object2.x + object2.width):
            return False
        elif (object1.x + object1.width) < object2.x:
            return False
        
        return True
    
    def check_collisions(self):
        for enemy in self.enemies:
            if self.detect_collision(self.player, enemy):
                self.level = 1.0
                return True

        if self.detect_collision(self.player, self.treasure):
            self.level += 0.5
            return True
        
        return False

    def run_game_loop(self):
        player_direction = 0

        while True:
            # Handle events
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # move player up
                        player_direction = -1
                    elif event.key == pygame.K_DOWN:
                        # move player down
                        player_direction = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player_direction = 0
                
            # Execute logic
            self.move_objects(player_direction)

            # Update display
            self.update_display()

            # Detect collisions
            if self.check_collisions():
                self.reset_map()

            # Execute logic
            self.clock.tick(30)