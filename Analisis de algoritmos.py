import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 250)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (34, 139, 34)

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Clase para el jugador (círculo)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 25
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.speed_x = 0

    def update(self):
        self.speed_x = 5 * (pygame.key.get_pressed()[pygame.K_RIGHT] - pygame.key.get_pressed()[pygame.K_LEFT])
        self.rect.x += self.speed_x
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

# Clase para los obstáculos (rectángulos)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = random.randint(50, 100)
        self.height = random.randint(20, 50)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(x=random.randrange(SCREEN_WIDTH - self.width), y=random.randrange(-100, -40))
        self.speed_y = random.uniform(1, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y += 0.05

# Función para la detección de colisión
def collision_check(player, obstacles):
    return pygame.sprite.spritecollideany(player, obstacles)

# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Evitar Obstáculos")

# Creación del fondo
background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
for y in range(SCREEN_HEIGHT // 2):
    gradient_color = [int(SKY_BLUE[c] + (LIGHT_GREEN[c] - SKY_BLUE[c]) * (y / (SCREEN_HEIGHT / 2))) for c in range(3)]
    pygame.draw.line(background, gradient_color, (0, y), (SCREEN_WIDTH, y))
for y in range(SCREEN_HEIGHT // 2, SCREEN_HEIGHT):
    gradient_color = [int(LIGHT_GREEN[c] + (DARK_GREEN[c] - LIGHT_GREEN[c]) * ((y - SCREEN_HEIGHT / 2) / (SCREEN_HEIGHT / 2))) for c in range(3)]
    pygame.draw.line(background, gradient_color, (0, y), (SCREEN_WIDTH, y))

# Creación de los sprites
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for _ in range(8):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# Reloj para controlar la velocidad de actualización
clock = pygame.time.Clock()

# Bucle principal del juego
running = True
while running:
    # Mantener el bucle funcionando a la velocidad correcta
    clock.tick(30)

    # Procesamiento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar
    all_sprites.update()

    # Detección de colisión
    if collision_check(player, obstacles):
        running = False

    # Dibujar / Renderizar
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

# Salida del juego
pygame.quit()
sys.exit()


