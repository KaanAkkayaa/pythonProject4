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
POWERUP_CHANCE = 20  # Özellik düşme olasılığı (%20)

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
explosion_anim = []
for i in range(5):
    explosion_anim.append(pygame.image.load(f"explosion0{i}.png").convert_alpha())
explosions = pygame.sprite.Group()

# Oyuncu sınıfı
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.power_up = False  # Güçlendirme özelliği aktif mi?

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
            if self.power_up:  # Güçlendirme özelliği aktifse 2'li mermi at
                bullet1 = Bullet(bullet_image, self.rect.left, self.rect.top)
                bullet2 = Bullet(bullet_image, self.rect.right, self.rect.top)
                bullets.add(bullet1, bullet2)
            else:
                bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top)
                bullets.add(bullet)
            bullet_sound.play()  # Mermi atışında ses çal

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Düşman sınıfı
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(random.choice(["enemy.png", "enemy2.png","enemy3.png","enemy4.png","enemy5.png","enemy6.png"])).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Rastgele x pozisyonu ayarlandı
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(ENEMY_SPEED // 2, ENEMY_SPEED)
        self.speedx = random.randint(-3, 3)  # Rastgele x hızı ayarlandı

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx  # x konumu güncellendi

        if self.rect.left < 0 or self.rect.right > WIDTH:  # Ekran sınırlarına çarpma kontrolü
            self.speedx = -self.speedx  # x hızını tersine çevirerek geri dönmesini sağlar

        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Yeni rastgele x pozisyonu ayarlandı
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(ENEMY_SPEED // 2, ENEMY_SPEED)
            self.speedx = random.randint(-3, 3)  # Yeni rastgele x hızı ayarlandı

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("power_up.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

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
        if self.rect.top < 0:
            self.kill()

        if random.randint(1, 100) <= POWERUP_CHANCE and self.speedy < 0:  # Özellik düşme olasılığı (sadece yukarı doğru atılan mermilerde)
            powerup = Powerup(self.rect.centerx, self.rect.centery)
            all_sprites.add(powerup)
            powerups.add(powerup)

def start_game():
    global enemy_counter, enemy_delay, game_over, game_over_timer, score
    enemy_counter = 0
    enemy_delay = ENEMY_FREQ
    game_over = False
    game_over_timer = 0
    score = 0
    player.reset()  # Oyuncuyu başlangıç konumuna getir
    powerups.empty()
    bullets.empty()  # Mermileri temizle
    enemies.empty()  # Düşmanları temizle
    explosions.empty()  # Patlamaları temizle
    all_sprites.empty()  # Tüm sprite'ları temizle
    all_sprites.add(player)  # Oyuncuyu tekrar ekle
    screen.fill(BLACK)  # Ekranı temizle
    screen.blit(background_image, (0, 0))  # Arka planı çiz

# Resimleri yükleme
player_image = pygame.image.load("player.png").convert_alpha()
bullet_image = pygame.image.load("bullet.png").convert_alpha()

player = Player(player_image)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

enemy_counter = 0
enemy_delay = ENEMY_FREQ
game_over = False
game_over_timer = 0
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    if not game_over:
        if enemy_counter >= enemy_delay:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_counter = 0
            enemy_delay = random.randint(ENEMY_FREQ // 2, ENEMY_FREQ)

        enemy_counter += 1

        # Çarpışma kontrolü
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            explosions.add(explosion)

        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            game_over = True
            game_over_timer = pygame.time.get_ticks()

        hits = pygame.sprite.spritecollide(player, powerups, True)
        if hits:
            player.power_up = True

        if game_over:
            if pygame.time.get_ticks() - game_over_timer > 2000:
                start_game()

        all_sprites.update()

    screen.fill(BLACK)
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
