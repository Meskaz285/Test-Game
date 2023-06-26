import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test game")

HFONT = pygame.font.Font('Assets/font2.ttf', 40)
WFONT = pygame.font.Font('Assets/font3.ttf', 80)

SHIT = pygame.mixer.Sound('Assets/kiblast.mp3')
SFIRE = pygame.mixer.Sound('Assets/sfire.mp3')

SG = (255, 255, 255)
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
FPS = 60

CATW, CATH = 125, 142

VEL = 4
BVEL = 7

C1HIT = pygame.USEREVENT + 1
C2HIT = pygame.USEREVENT + 2

CAT1IMG = pygame.image.load(os.path.join('Assets', 'Japanese_Bob.png'))
CAT1IMG = pygame.transform.scale(CAT1IMG, (CATW, CATH))
CAT2IMG = pygame.image.load(os.path.join('Assets', 'Boots.png'))
CAT2IMG = pygame.transform.flip(pygame.transform.scale(CAT2IMG, (CATW, CATH)), True, False)
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bg.jpg')), (WIDTH, HEIGHT))


def drawWindow(cat1, cat2, c1Bul, c2Bul, c1H, c2H):
    WIN.blit(BG, (0, 0))
    # pygame.draw.rect(WIN, (0, 0, 0), BORDER)
    c1HText = HFONT.render("Health: " + str(c1H), 1, (0, 0, 0))
    c2HText = HFONT.render("Health: " + str(c2H), 1, (0, 0, 0))
    WIN.blit(c2HText, (WIDTH - c1HText.get_width() - 40, 10))
    WIN.blit(c1HText, (10, 10))

    WIN.blit(CAT1IMG, (cat1.x, cat1.y))
    WIN.blit(CAT2IMG, (cat2.x, cat2.y))

    for bullet in c1Bul:
        pygame.draw.rect(WIN, (77, 238, 234), bullet)
    for bullet in c2Bul:
        pygame.draw.rect(WIN, (116, 238, 21), bullet)
    pygame.display.update()


def movC1(keyPress, c1):
    if keyPress[pygame.K_a] and c1.x - VEL > 0:
        c1.x -= VEL
    if keyPress[pygame.K_d] and c1.x + VEL + c1.width < BORDER.x:
        c1.x += VEL
    if keyPress[pygame.K_w] and c1.y - VEL > 0:
        c1.y -= VEL
    if keyPress[pygame.K_s] and c1.y + VEL + c1.height < HEIGHT:
        c1.y += VEL


def movC2(keyPress, c2):
    if keyPress[pygame.K_LEFT] and c2.x - VEL > BORDER.x + BORDER.width:
        c2.x -= VEL
    if keyPress[pygame.K_RIGHT] and c2.x + VEL + c2.width < WIDTH:
        c2.x += VEL
    if keyPress[pygame.K_UP] and c2.y - VEL > 0:
        c2.y -= VEL
    if keyPress[pygame.K_DOWN] and c2.y + VEL + c2.height < HEIGHT:
        c2.y += VEL


def bulHand(c1Bul, c2Bul, c1, c2):
    for bullet in c1Bul:
        bullet.x += BVEL
        if c2.colliderect(bullet):
            pygame.event.post((pygame.event.Event(C2HIT)))
            c1Bul.remove(bullet)
        elif bullet.x > WIDTH:
            c1Bul.remove(bullet)
    for bullet in c2Bul:
        bullet.x -= BVEL
        if c1.colliderect(bullet):
            pygame.event.post((pygame.event.Event(C1HIT)))
            c2Bul.remove(bullet)
        elif bullet.x < 0:
            c2Bul.remove(bullet)


def drawWinner(text):
    drawText = WFONT.render(text, 1, (0, 0, 0))
    WIN.blit(drawText, (WIDTH // 2 - drawText.get_width() // 2, HEIGHT // 2 - drawText.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)


def main():
    c1 = pygame.Rect(100, 300, CATW, CATH)
    c2 = pygame.Rect(650, 300, CATW, CATH)
    c1Bul = []
    c2Bul = []
    c1Health = 10
    c2Health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(c1Bul) < 3:
                    bullet = pygame.Rect(c1.x + c1.width, c1.y + c1.height // 2 - 2, 10, 5)
                    c1Bul.append(bullet)
                    SFIRE.play()

                if event.key == pygame.K_RCTRL and len(c2Bul) < 3:
                    bullet = pygame.Rect(c2.x, c2.y + c2.height // 2 - 2, 10, 5)
                    c2Bul.append(bullet)
                    SFIRE.play()

            if event.type == C1HIT:
                c1Health -= 1
                SHIT.play()
            if event.type == C2HIT:
                c2Health -= 1
                SHIT.play()
        winner = ""
        if c1Health <= 0:
            winner = "Cat 2 Wins"
        if c2Health <= 0:
            winner = "Cat 1 Wins"
        if winner != "":
            drawWinner(winner)
            break

        keyPress = pygame.key.get_pressed()
        movC1(keyPress, c1)
        movC2(keyPress, c2)

        bulHand(c1Bul, c2Bul, c1, c2)
        drawWindow(c1, c2, c1Bul, c2Bul, c1Health, c2Health)

    pygame.quit()


if __name__ == "__main__":
    main()
