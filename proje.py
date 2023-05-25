import pygame
import random
import sys

# Ekran boyutları
WIDTH = 800
HEIGHT = 600

# Oyun ayarları
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 3
ENEMY_FREQ = 60  # Düşman oluşturma sıklığı (60 FPS)

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Pygame başlatma
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Arka plan görüntüsünü yükle
background_image = pygame.image.load("background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
bullet_sound = pygame.mixer.Sound("laser1.ogg")

# Oyuncu sınıfı
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Ekran sınırlarını kontrol etme
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
    def shoot(self):
        if not game_over:
            bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            bullet_sound.play()  # Mermi atışında ses çal

# Düşman sınıfı
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(ENEMY_SPEED // 2, ENEMY_SPEED)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(ENEMY_SPEED // 2, ENEMY_SPEED)


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(ENEMY_SPEED // 2, ENEMY_SPEED)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(ENEMY_SPEED // 2, ENEMY_SPEED)
# Mermi sınıfı
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -BULLET_SPEED

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(ENEMY_SPEED // 2, ENEMY_SPEED)

def start_game():
    global enemy_counter, enemy_delay, game_over, game_over_timer,score
    enemy_counter = 0
    enemy_delay = ENEMY_FREQ
    game_over = False
    game_over_timer = 0
    score = 0
    player.reset()  # Oyuncuyu başlangıç konumuna getir
    bullets.empty()  # Mermileri temizle
    enemies.empty()  # Düşmanları temizle

# Oyuncu görüntüsünü yükle
player_image = pygame.image.load("player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 38))

# Düşman görüntüsünü yükle
enemy_image = [pygame.image.load("enemy.png").convert_alpha()

]

# Mermi görüntüsünü yükle
bullet_image = pygame.image.load("bullet.png").convert_alpha()

# Düşman oluşturma fonksiyonu
def create_enemy():
    enemy = Enemy(enemy_image)
    enemies.add(enemy)

# Oyuncu oluşturma
player = Player(player_image)

# Düşman ve mermi grupları
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
#yazı fontu
font = pygame.font.SysFont("Arial", 36)
score_font_size = pygame.font.SysFont("Arial", 25)

# Vurulan düşman sayacı
score = 0

# Oyun döngüsü
running = True
enemy_counter = 0
enemy_delay = ENEMY_FREQ
game_over = False  # Oyun bitiş durumu
game_over_timer = 0  # Oyun bitiş zamanlayıcısı
game_over_duration = 5  # Oyun bitiş süresi (saniye)
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            elif event.key == pygame.K_RETURN:
                if game_over:
                    start_game()
    screen.blit(background_image, (0, 0))

    # Oyuncuyu güncelleme ve çizme
    if not game_over:
        player.update()
        screen.blit(player.image, player.rect)

    # Düşmanları güncelleme, çizme ve oluşturma
    enemies.update()
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)

        # Düşmanın oyuncuyu çaptığını kontrol etme
        if not game_over and pygame.sprite.collide_rect(enemy, player):
            game_over = True
            game_over_timer = pygame.time.get_ticks()  # Oyun bitiş zamanlayıcısını başlatma

    # Mermileri güncelleme ve çizme
    bullets.update()
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)

    # Düşman oluşturma
    if not game_over:
        enemy_delay -= 1
        if enemy_delay <= 0:
            create_enemy()
            enemy_delay = ENEMY_FREQ

    # Çarpışmaları kontrol etme
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for bullet, enemy_list in collisions.items():
        score += len(enemy_list)

    # Vurulan düşman sayısını görüntüleme
    score_text = score_font_size.render("Vurulan Düşmanlar: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))  # Sol üst köşeye yerleştirme

    # Oyunun bitiş süresini kontrol etme
    if game_over:
        if game_over:
            score_text = score_font_size.render("Vurulan Düşmanlar: {}".format(score), True, WHITE)  # Score'u ekrana yazdırma
            score_rect = score_text.get_rect(topleft=(10, 10))
            screen.blit(score_text, score_rect)
        if pygame.time.get_ticks() - game_over_timer <= game_over_duration * 1000:
            game_over_text = font.render("Oyun Bitti", True, (255, 255, 255))  # Yazıyı oluşturma
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Yazının konumunu belirleme
            screen.blit(game_over_text, game_over_rect)  # Yazıyı ekrana çizme

            restart_font = pygame.font.Font(None, 25)
            restart_text = restart_font.render("Tekrar oynamak için lütfen enter tuşuna basın", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)

    pygame.display.flip()

# Oyun döngüsünden çıkıldığında pygame'i kapat
pygame.quit()