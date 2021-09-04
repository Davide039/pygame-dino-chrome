import random
import sys, pygame

pygame.init()

width, height = 1320, 460
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Dino Game")
clock = pygame.time.Clock()

ground = pygame.image.load("img/ground.jpg")
groundx = 0
speed = 6

times = [1000, 1500, 1250, 3000, 2400, 2100, 2600, 1700, 3100]
CHANGE_PLAYER_FRAMES = pygame.USEREVENT
GENERATE_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(GENERATE_OBSTACLE, random.choice(times))
pygame.time.set_timer(CHANGE_PLAYER_FRAMES, 200)

game_active = True

isJumping = False
v = 8
m = 1

class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.images = [
            pygame.image.load("dino_first.jpg"),
            pygame.image.load("dino_second.jpg")
        ]
        self.image_index = 0
        self.current = pygame.transform.scale(self.images[self.image_index % len(self.images)],
                                              (78, 84)).convert_alpha()
        self.current.set_colorkey((255, 255, 255))
        self.current_rect = self.current.get_rect()

    def do_animation(self):
        self.image_index += 1
        self.current = pygame.transform.scale(self.images[self.image_index % len(self.images)],
                                              (78, 84)).convert_alpha()
        self.current.set_colorkey((255, 255, 255))
        self.current_rect = self.current.get_rect()


player = Player(30, 345)


class Obstacles:
    def __init__(self) -> None:
        self.obstacles = []
        self.obstacle = pygame.image.load("obstacle.jpg").convert_alpha()
        self.obstacle.set_colorkey((255, 255, 255))

    def create_obstacle(self):
        self.obstacles.append(self.obstacle.get_rect(midtop=(1350, 345)))

    def move_obstacles(self):
        for obst in self.obstacles:
            obst.centerx -= speed
        return self.obstacles

    def draw_obstacles(self):
        for obst in self.obstacles:
            screen.blit(self.obstacle, obst)

    def check_collision(self):
        for obstacle in self.obstacles:
            if player.current_rect.colliderect(obstacle):
                return False
        return True


obstacles = Obstacles()

while True:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CHANGE_PLAYER_FRAMES and game_active:
            player.do_animation()
        if event.type == GENERATE_OBSTACLE:
            obstacles.create_obstacle()
            pygame.time.set_timer(GENERATE_OBSTACLE, random.choice(times))

    keys = pygame.key.get_pressed()

    if game_active:
        if not isJumping:
            if keys[pygame.K_SPACE]:
                isJumping = True

        if isJumping:
            F = (1 / 2) * m * (v ** 2)
            player.y -= F

            v -= 0.4

            if v < 0:
                m = -0.5
            if player.y >= 345:
                isJumping, v, m = False, 8, 1
    else:
        if keys[pygame.K_SPACE]:
            game_active = True
            speed = 5

    if game_active:
        game_active = obstacles.check_collision()
    else:
        obstacles.obstacles.clear()
        speed = 0
        screen.blit(pygame.image.load("restart.jpg"),
					pygame.image.load("estart.jpg").get_rect(center=(width / 2, height / 2)))

    groundx -= speed
    if groundx <= -2400:
        groundx = 0

    screen.blit(ground, (groundx, 410))
    screen.blit(ground, (groundx + 2400, 410))

    screen.blit(player.current, (player.x, player.y))

    obstacles.obstacles = obstacles.move_obstacles()
    obstacles.draw_obstacles()

    pygame.display.flip()
    pygame.display.update()
    clock.tick(120)
