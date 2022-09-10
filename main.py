import pygame
import math

from pygame import mixer
from random import randint
from secrets import randbits

from setInterval import setInterval

# Initialize the pygame and the mixer
pygame.init()
mixer.init()

# Songs
mixer.music.load("./audios/background.wav")
bulletSound = mixer.Sound("./audios/laser.wav")
explosionSound = mixer.Sound("./audios/explosion.wav")
bulletSound.set_volume(0.1)
explosionSound.set_volume(0.1)

# Play the song
mixer.music.play(-1)
mixer.music.set_volume(0.1)

# Play background song

# Background
background = pygame.image.load("./images/background.png")

# Set the screen display
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

# Title and Icon
pygame.display.set_caption("Space Invaders")
gameIcon = pygame.image.load("./images/icon.png")
pygame.display.set_icon(gameIcon)


# Entities


class Entity():
    def __init__(self, X, Y, speed, icon):
        self.id = randbits(10)
        self.X = X
        self.Y = Y
        self.speed = speed
        self.movementDirection = ""
        self.icon = pygame.image.load(f"./images/{icon}")
        self.isMoving = False
        self.isBullet = False
        self.isDead = False

    # Render
    def render(self):
        # Check if entity is alive
        if (self.isDead):
            return

        # Check if the entity is not being hit by a bullet right now
        if (not self.isBullet):
            for bullet in bullets:
                if (bullet.shooterID != self.id and not bullet.isDead):
                    getBulletDistanceFromEntity = math.sqrt(
                        math.pow(self.X - bullet.X, 2) + math.pow(self.Y - bullet.Y, 2))
                    if (getBulletDistanceFromEntity < 32):
                        self.kill()
                        bullet.isDead = True
                        if (bullet.shooterID == player.id):
                            player.score += 1

        screen.blit(self.icon, (self.X, self.Y))

    # Actions
    def move(self, keyCode):
        def moveLeft():
            if (self.X > 20):
                self.X += self.speed * -0.10

        def moveRight():
            if (self.X < 700):
                self.X += self.speed * 0.10

        movements = {
            1073741903: moveRight,
            "right": moveRight,
            1073741904: moveLeft,
            "left": moveLeft
        }

        try:
            movements[keyCode]()
            self.lockMovement(keyCode)
        except Exception:
            pass

    def shoot(self):
        bullet = Bullet(self.X + 15, self.Y, 10, "bullet.png", "up", self.id)
        bullets.append(bullet)
        bulletSound.play()

    def kill(self):
        explosionSound.play()
        self.isDead = True

    # Movement lockers
    def lockMovement(self, movementDirection):
        self.movementDirection = movementDirection
        self.isMoving = True

    def unlockMovement(self, movementDirection):
        if (self.movementDirection == movementDirection):
            self.isMoving = False


class Player(Entity):
    def __init__(self, X, Y, speed, icon):
        super().__init__(X, Y, speed, icon)
        self.score = 0

    def kill(self):
        mixer.music.pause()
        return super().kill()


class Enemy(Entity):
    def automaticAnimation(self):
        if (self.movementDirection == "left"):
            self.move("left")
            if (self.X <= 20):
                self.movementDirection = "right"
                self.Y += 50
        else:
            self.move("right")
            if (self.X >= 700):
                self.movementDirection = "left"
                self.Y += 50

    def checkCollisionWithPlayer(self):
        getDistanceWithPlayer = math.sqrt(
            math.pow(self.X - player.X, 2) + math.pow(self.Y - player.Y, 2))
        if (getDistanceWithPlayer < 32):
            player.kill()


class Bullet(Entity):
    def __init__(self, X, Y, speed, icon, direction, shooterID):
        super().__init__(X, Y, speed, icon)
        self.isBullet = True
        self.direction = direction
        self.shooterID = shooterID

    def automaticAnimation(self):
        if (self.Y < 0 or self.Y > 800):
            del bullets[0]
            return
        if (self.direction == "up"):
            self.Y -= self.speed
        else:
            self.Y += self.speed


# Player
player = Player(370, 480, 40, "player.png")

# Enemy Spawning
enemies = []


def createEnemy():
    newEnemy = Enemy(randint(100, 800), randint(50, 150), 40, "enemy.png")
    enemies.append(newEnemy)


# Spawn 6 enemies when the game begins
for i in range(6):
    createEnemy()

enemySpawner = setInterval(createEnemy, 5)

# Bullets
bullets = []

# Score
title = pygame.font.Font("freesansbold.ttf", 72)
subtitle = pygame.font.Font("freesansbold.ttf", 32)


def renderScore():
    score = subtitle.render(f"SCORE: {player.score}", True, (255, 255, 255))
    screen.blit(score, (10, 10))

# Game Over Screen


def renderGameOverScreen():
    gameOver = title.render("GAME OVER!", True, (255, 0, 0))
    scoreLabel = subtitle.render(
        f"Your score: {player.score}", True, (255, 255, 0))
    screen.blit(gameOver, (180, 250))
    screen.blit(scoreLabel, (300, 320))


# Game Loop
running = True
while running:
    screen.blit(background, (0, 0))

    # Events Listener
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            running = False
            enemySpawner.cancel()

        # Keystroke event
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_LSHIFT):
                player.shoot()
            player.move(event.key)

        if event.type == pygame.KEYUP:
            player.unlockMovement(event.key)

    if (player.isDead):
        renderGameOverScreen()
    else:
        # Draw the player
        player.render()
        if (player.isMoving):
            player.move(player.movementDirection)

        # Draw the enemy
        for enemy in enemies:
            enemy.render()
            enemy.automaticAnimation()
            enemy.checkCollisionWithPlayer()

        # Draw the bullets
        for bullet in bullets:
            bullet.render()
            bullet.automaticAnimation()

        # Draw the score
        renderScore()

    # Update the game while running
    pygame.display.update()
