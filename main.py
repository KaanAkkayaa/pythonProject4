import pygame
import random

# Oyun penceresi boyutları
WIDTH = 800
HEIGHT = 600

# Renkler
WHITE = (255, 255, 255)

# Oyun hızı
FPS = 60

# Pygame başlangıç
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Oyundaki sprite'lar için gruplar oluşturuluyor
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Boss sınıfı
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.health = 10

    def update(self):
        pass

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()

# Boss oluşturuluyor
boss = None
boss_active = False

# Düşman oluşturma fonksiyonu
def create_enemy():
    global boss_active
    if boss_active:
        return

    enemy_counter += 1
    if score % 20 == 0 and score != 0:
        boss_active = True
        boss = Boss()
        all_sprites.add(boss)
        enemies.add(boss)
    else:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

# Oyun döngüsü
running = True
while running:
    clock.tick(FPS)

    # Olaylar kontrol ediliyor
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Oyuncu güncelleniyor
    all_sprites.update()

    # Düşmanların oluşturulması
    if len(enemies) < 10:
        create_enemy()

    # Kurşun-düşman çarpışması kontrolü
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)

    # Eğer bir düşman vurulduysa skor arttırılıyor
    for hit in hits:
        player.score += 1

    # Boss'un sağlığı kontrol ediliyor
    if boss_active and boss.health <= 0:
        boss_active = False

    # Oyun ekranı temizleniyor
    screen.fill(WHITE)

    # Tüm sprite'lar yeniden çiziliyor
    all_sprites.draw(screen)

    # Ekran güncelleniyor
    pygame.display.flip()

# Oyun döngüsünden çıkıldığında pygame kapatılıyor
pygame.quit()

