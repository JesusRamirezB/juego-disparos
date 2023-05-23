import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Crear la ventana del juego
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Naves")

# Clase para la nave del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.score = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speed_x = -5
        elif keys[pygame.K_d]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Clase para los proyectiles
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# Clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 3)

# Función principal del juego
def game():
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        if not game_over:
            all_sprites.update()

            hits = pygame.sprite.spritecollide(player, enemies, False)
            if hits:
                game_over = True

            # Crear nuevos enemigos
            if len(enemies) < 10:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

            # Detectar colisiones entre proyectiles y enemigos
            hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
            for hit in hits:
                player.score += 1

        window.fill(WHITE)

        all_sprites.draw(window)

        if game_over:
            font = pygame.font.Font(None, 48)
            text = font.render("Game Over", True, RED)
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        score_font = pygame.font.Font(None, 24)
        score_text = score_font.render(f"Score: {player.score}", True, GREEN)
        window.blit(score_text, (10, 10))

        pygame.display.flip()

# Función para mostrar el menú principal
def show_menu():
    menu_font = pygame.font.Font(None, 36)

    while True:
        window.fill(WHITE)
        title_text = menu_font.render("Juego de Naves", True, GREEN)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        window.blit(title_text, title_rect)

        start_text = menu_font.render("1. Iniciar Juego", True, RED)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(start_text, start_rect)

        quit_text = menu_font.render("2. Salir", True, RED)
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        window.blit(quit_text, quit_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game()
                elif event.key == pygame.K_2:
                    pygame.quit()
                    return

# Mostrar el menú principal
show_menu()
