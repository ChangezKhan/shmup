# CREDITS
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

import pygame
import random
from os import path

WIDTH = 360     # Pygame window width
HEIGHT = 480	# Pygame window height
FPS = 30		# Frame-Per-Second 

# Define static colors

WHITE 	= (255, 255, 255)
BLACK 	= (0, 0, 0)
RED 	= (255, 0, 0)
GREEN 	= (0, 255, 0)
BLUE 	= (0, 0, 255)

# set up assets folder
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")
sound_folder = path.join(game_folder, "audio")

pygame.init()				# Initializes pygame
pygame.mixer.init()			# Initializes sound in pygame

screen = pygame.display.set_mode((WIDTH, HEIGHT))	# Create screen of pygame with height and width

pygame.display.set_caption("Shmup!!!")			# Set window title

clock = pygame.time.Clock()							# Set clock time

font_name = pygame.font.match_font('arial')

def show_game_over_screen():
	screen.blit(BackGround.image, BackGround.rect)
	draw_text(screen, "Shmup!!!", 64, WIDTH / 2, HEIGHT / 4)
	draw_text(screen, "Arrow key move, Space to file", 20, WIDTH / 2, HEIGHT / 2)
	draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 2)
	pygame.display.flip()
	waiting  = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def new_mob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

def draw_shield_bar(surf, percent):
	if percent < 0:
		percent = 0
	X_VALUE = 5
	Y_VALUE = 5
	BAR_LENGTH = 100
	BAR_HEIGHT = 10
	fill = (percent / 100) * BAR_LENGTH
	fill_rect = pygame.Rect(X_VALUE, Y_VALUE, fill, BAR_HEIGHT)
	pygame.draw.rect(surf, GREEN, fill_rect)
	outline_rect = pygame.Rect(X_VALUE, Y_VALUE, BAR_LENGTH, BAR_HEIGHT)
	pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img):
	X_VALUE = WIDTH - 100
	Y_VALUE = 5
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = X_VALUE + 30 * i
		img_rect.y = Y_VALUE
		surf.blit(img, img_rect)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img, (50, 45))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 25
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.shield = 100
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()

	def update(self):
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = WIDTH / 2
			self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -5
		if keystate[pygame.K_RIGHT]:
			self.speedx = 5
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		shoot_sound.play()

	def hide(self):
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(meteor_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * 0.95 / 2)
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-3, 3)
		self.rot = 0
		self.rot_speed = random.randrange(-10, 10)
		self.last_update = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pygame.transform.rotate(self.image_orig, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x,  y):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy

		# kill if it moves off the top of the screen
		if self.rect.bottom < 0:
			self.kill()

class Power(pygame.sprite.Sprite):
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.type = random.choice(['shield', 'gun'])
		self.image = powerup_images[self.type]
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 3

	def update(self):
		self.rect.y += self.speedy

		# kill if it moves off the top of the screen
		if self.rect.top > HEIGHT:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_images[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 75

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			if self.frame == len(explosion_images[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_images[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center 			
			self.frame += 1

# Load all game_foldere graphics
BackGround = Background(path.join(img_folder, "blue.png"))

player_img = pygame.image.load(path.join(img_folder, "playerShip.png")).convert()

player_mini_img = pygame.transform.scale(player_img, (25, 20))
player_mini_img.set_colorkey(BLACK)

bullet_img = pygame.image.load(path.join(img_folder, "laserBlue.png")).convert()

meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med2.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']

for img in meteor_list:
	meteor_images.append(pygame.image.load(path.join(img_folder, img)).convert())

explosion_images = {}
explosion_images['lg'] = []
explosion_images['sm'] = []
explosion_images['player'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_images['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (35, 35))
    explosion_images['sm'].append(img_sm)
    file_name = 'sonicExplosion0{}.png'.format(i)
    img_player = pygame.image.load(path.join(img_folder, file_name)).convert()
    img_player.set_colorkey(BLACK)
    explosion_images['player'].append(img_player)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_folder, 'bolt_gold.png')).convert()
# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(sound_folder, "Laser_Shoot.wav"))
shoot_sound.set_volume(0.1)
explosion_sound = []

for sound in ['Explosion1.wav', 'Explosion2.wav']:
	explosion_sound.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'Explosion3.wav'))
pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.1)

# Game loop

pygame.mixer.music.play(loops=-1)

running = True

game_over = True

while running:
	if game_over:
		show_game_over_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()		# Add sprites to group
		mobs = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		powerups = pygame.sprite.Group()

		player = Player()
		all_sprites.add(player)

		for i in range(10):
			new_mob()

		score = 0

	# keep loop running at the right speed
	clock.tick(FPS)	
	# Process input
	for event in pygame.event.get():
		# check for closing the window
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
	
	# Update
	all_sprites.update()		# Update sprites

	# check to see if a bullet hit a mob
	bullet_hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

	for hit in bullet_hits:
		score += 60 - hit.radius
		random.choice(explosion_sound).play().set_volume(0.1)
		expl = Explosion(hit.rect.center, 'lg')
		all_sprites.add(expl)
		if random.random() > 0.9: 
			power = Power(hit.rect.center)
			all_sprites.add(power)
			powerups.add(power)
		new_mob()

	# check to see if a mob hit the player
	mob_hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)

	for hit in mob_hits:
		player.shield -= hit.radius * 2
		expl = Explosion(hit.rect.center, 'sm')
		all_sprites.add(expl)
		new_mob()
		if player.shield <= 0:
			player_die_sound.play()
			death_explosion = Explosion(player.rect.center, 'player')
			all_sprites.add(death_explosion)
			player.hide()
			player.lives -= 1
			player.shield = 100

	# check to see if a power hit the player
	pow_hits = pygame.sprite.spritecollide(player, powerups, True)

	for hit in pow_hits:
		if hit.type == 'shield':
			player.shield += random.randrange(10, 30)
			if player.shield >= 100:
				player.shield = 100
		if hit.type == 'gun':
			pass
	# if player died and explosion finished playing
	if player.lives == 0 and not death_explosion.alive():
		game_over = True

	# Draw/render
	screen.fill(BLACK)		# Set color of screen
	screen.blit(BackGround.image, BackGround.rect)
	all_sprites.draw(screen)	# Draw sprites on screen
	draw_text(screen, str(score), 20, WIDTH / 2, 10)
	draw_shield_bar(screen, player.shield)
	draw_lives(screen, player.lives, player_mini_img)
	pygame.display.flip()	# After drawing everything update the entire display

pygame.quit()