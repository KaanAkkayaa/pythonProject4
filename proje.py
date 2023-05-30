import pygame
import random
import sys
import time

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
powerup_sound = pygame.mixer.Sound("powerup_sound.ogg")
explosion_images = [pygame.image.load("explosion00.png"),
                    pygame.image.load("explosion01.png"),
                    pygame.image.load("explosion02.png"),
                    pygame.image.load("explosion03.png"),
                    pygame.image.load("explosion04.png")]
explosions = pygame.sprite.Group()

# Oyuncu sınıfı
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.powerup_active = False
        self.powerup_duration = 10000  # 10 saniye (milisaniye cinsinden)
        self.powerup_start_time = 0  # Güçlendirme başlangıç zamanı
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

        if self.powerup_active:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.powerup_start_time
            if elapsed_time >= self.powerup_duration:
                self.powerup_active = False
    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.powerup_active = False
    def shoot(self):
        if not game_over:
            bullet = Bullet(bullet_image, self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            bullet_sound.play()  # Mermi atışında ses çal

            # Güçlendirme alındığında ikili atış yap
            if self.powerup_active:
                dual_bullet1 = DualBullet(bullet_image, self.rect.centerx - 15, self.rect.top)
                dual_bullet2 = DualBullet(bullet_image, self.rect.centerx + 15, self.rect.top)
                bullets.add(dual_bullet1)
                bullets.add(dual_bullet2)
                bullet_sound.play()  # İkili mermi atışında ses çal
                self.powerup_start_time = pygame.time.get_ticks()  # Güçlendirme başlangıç zamanını güncelle
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


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, duration):
        super().__init__()
        self.image = pygame.image.load("power_up.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(ENEMY_SPEED // 2, ENEMY_SPEED)
        self.duration = duration
        self.duration_timer = None
        self.active = False  # active özelliği eklendi
    def drop_powerup(self, enemy):
        if random.random() < 0.15:
            self.rect.center = enemy.rect.center
            all_sprites.add(self)
            powerup_group.add(self)
            self.active = True
            # Power-up'ın etkin kalma süresini başlat
            self.start_duration_timer()
    def update(self):
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(ENEMY_SPEED // 2, ENEMY_SPEED)

        self.check_powerup_collision()  # Çarpışmayı kontrol et

        if self.active:
            if not hasattr(self, "duration_timer"):
                self.start_duration_timer()
            elif self.duration_timer and pygame.time.get_ticks() - self.duration_timer > self.duration * 1000:
                self.active = False
                self.duration_timer = None
                self.kill()




    def check_powerup_collision(self):
        collisions = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in collisions:
            player.powerup_active = True
            powerup_sound.play()
        self.start_time = pygame.time.get_ticks()  # Güçlendirme başlangıç zamanı
        self.duration = 15

    def start_duration_timer(self):
        self.duration_timer = pygame.time.get_ticks()

    def stop_duration_timer(self):
        self.duration_timer = None

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

class DualBullet(Bullet):
        def __init__(self, image, x, y):
            super().__init__(image, x, y)
            self.speedx = 0  # İkili mermi yatay yönde hareket etmeyecek

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top < 0:
                self.kill()

            # İkili mermi hızını kontrol et
            self.speedy = -BULLET_SPEED


def start_game():
    global enemy_counter, enemy_delay, game_over, game_over_timer, score,powerup_active
    enemy_counter = 0
    enemy_delay = ENEMY_FREQ
    game_over = False
    game_over_timer = 0
    score = 0
    player.reset()  # Oyuncuyu başlangıç konumuna getir
    bullets.empty()  # Mermileri temizle
    enemies.empty()# Düşmanları temizle
    explosions.empty()  # Patlamaları temizle
    all_sprites.empty()  # Tüm sprite'ları temizle
    all_sprites.add(player)  # Oyuncuyu tekrar ekle
    screen.fill(BLACK)  # Ekranı temizle
    screen.blit(background_image, (0, 0))  # Arka planı çiz




# Oyuncu görüntüsünü yükle
player_image = pygame.image.load("player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 38))

# Düşman görüntüsünü yükle
enemy_images = ["enemy.png", "enemy2.png"]



# Mermi görüntüsünü yükle
bullet_image = pygame.image.load("bullet.png").convert_alpha()

# Düşman oluşturma fonksiyonu
def create_enemy():
    enemy = Enemy()
    enemies.add(enemy)

# Patlama animasyonunu yükle
explosion_anim = []
for i in range(9):
    filename = f"explosion0{i}.png"
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img)

# Düşmanları oluştur
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
for _ in range(8):
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)
    enemies.add(enemy)

powerups = pygame.sprite.Group()

# Oyuncu oluşturma
player = Player(player_image)

# Düşman ve mermi grupları
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
# Güçlendirme oluşturma
powerups = pygame.sprite.Group()
powerup_delay = 200  # Güçlendirme oluşturma sıklığı (200 FPS)
#yazı fontu
font = pygame.font.SysFont("Arial", 36)
score_font_size = pygame.font.SysFont("Arial", 25)

# Vurulan düşman sayacı
score = 0

# Oyun döngüsü
running = True
clock = pygame.time.Clock()
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
        # Düşmanlar ile mermi çarpışması olduğunda patlama oluştur
        for hit_enemy in enemy_list:
            explosion = Explosion(hit_enemy.rect.center)
            all_sprites.add(explosion)
            explosions.add(explosion)
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)


    powerups.update()
    for powerup in powerups:
        screen.blit(powerup.image, powerup.rect)

    # Güçlendirme oluşturma
    powerup_delay -= 1
    if powerup_delay <= 0:
        powerup = PowerUp(15)
        powerups.add(powerup)
        powerup_delay = 1000
        # 15 saniye süreyle bir PowerUp örneği oluşturuldu

    explosions.update()
    for explosion in explosions:
        screen.blit(explosion.image, explosion.rect)
        if explosion.frame == len(explosion_anim):
            explosion.kill()
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

 # Tüm sprite'ları çiz

    all_sprites.draw(screen)

    pygame.display.flip()

# Oyun döngüsünden çıkıldığında pygame'i kapat
pygame.quit()