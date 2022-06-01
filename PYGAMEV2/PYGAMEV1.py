#These 4 liness import modules and assests from pygame
import pygame
import os
pygame.font.init()
pygame.mixer.init()
 
WIDTH, HEIGHT = 1000, 650
GAME_SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HORSES V. PIRATES")
GREY = (200, 200, 200)
FONT_COLOR = (200,200,255)
BORDER = pygame.Rect(0, HEIGHT/2 - 5, WIDTH, 10)
FPS = 50
PLAYER_WIDTH, PLAYER_LENGTH = 80, 80
HORSE_PINGU_SPEED, PIRATE_CANNON_SPEED = 17, 17                  
MAX_PROJECTILES = 5
VEL = 3
BLUE = (0, 100, 255)
RED = (255, 0, 0)
#Character hits and health is registered
HORSE_HIT = pygame.USEREVENT + 1
PIRATE_HIT = pygame.USEREVENT + 2
 
#Below files in the directories are imported from the assets folder and put into variables.
 
LIVES_FONT = pygame.font.SysFont("comic", 30)
VICTORY_FONT = pygame.font.SysFont("comic", 100)
HORSE_NOISE = pygame.mixer.Sound(os.path.join("assets", "birdchirp.wav"))
PIRATE_NOISE = pygame.mixer.Sound(os.path.join("assets", "splash.wav"))
DAMAGE_NOISE = pygame.mixer.Sound(os.path.join("assets", "smack.wav"))
HORSE_CHAR_IMAGE = pygame.image.load(os.path.join("assets", "Horse_Monster.png"))
HORSE_CHAR = pygame.transform.scale(HORSE_CHAR_IMAGE, (PLAYER_WIDTH, PLAYER_LENGTH)) #Transfrom modifies size of image
CANNON_BALL_IMAGE = pygame.image.load(os.path.join("assets", "cannonball.jpeg"))
CANNON_BALL = pygame.transform.scale(CANNON_BALL_IMAGE, (PLAYER_WIDTH, PLAYER_LENGTH))
PINGU_IMAGE = pygame.image.load(os.path.join("assets", "Pingu.webp"))
PINGU = pygame.transform.scale(PINGU_IMAGE, (PLAYER_WIDTH, PLAYER_LENGTH))
PIRATE_CHAR_IMAGE = pygame.image.load(os.path.join("assets", "Pirate_ship.png"))
PIRATE_CHAR = pygame.transform.scale(PIRATE_CHAR_IMAGE, (PLAYER_WIDTH, PLAYER_LENGTH))
#The beach background is made
BEACH = pygame.transform.scale(pygame.image.load(os.path.join("assets", "beach.jpeg")), (WIDTH, HEIGHT))
 
 
def gameWindow(HORSE, PIRATE, PIRATE_bullets, HORSE_bullets, HORSE_HEALTH, PIRATE_HEALTH):
    #This is the main background image
    GAME_SCREEN.blit(BEACH, (0, 0)) #blit places image on screen
    pygame.draw.rect(GAME_SCREEN, GREY, BORDER)
 
    #this out player health on screen
    HORSE_HEALTHTxt = LIVES_FONT.render("Health: " + str(HORSE_HEALTH), 1, FONT_COLOR) #Render puts string onto screen
    PIRATE_HEALTHTxt = LIVES_FONT.render("Health: " + str(PIRATE_HEALTH), 1, FONT_COLOR)
   
    #This is what modifies player health
    GAME_SCREEN.blit(PIRATE_HEALTHTxt, (WIDTH - PIRATE_HEALTHTxt.get_width()-15, 15))
    GAME_SCREEN.blit(HORSE_HEALTHTxt, (15, HEIGHT - HORSE_HEALTHTxt.get_height()-15))
 
#Both players are put on screen at a predetermined x and y position
    GAME_SCREEN.blit(HORSE_CHAR, (HORSE.x, HORSE.y))
    GAME_SCREEN.blit(PIRATE_CHAR, (PIRATE.x, PIRATE.y))
 
#For each element in the horse bullt list, a bullet (rectanlge ) is spawned on screen
    for bullet in HORSE_bullets:
        pygame.draw.rect(GAME_SCREEN, BLUE, bullet)
        GAME_SCREEN.blit(PINGU, (bullet.x - 30, bullet.y - 10))#Adds an imagae on top of the rectanlge, making it seem like the image is the object
 
    for bullet in PIRATE_bullets:
        pygame.draw.rect(GAME_SCREEN, RED, bullet) #Draws a rectanlge which moves per fram on the screen
        GAME_SCREEN.blit(CANNON_BALL, (bullet.x, bullet.y)) #Adds an imagae on top of the rectanlge, making it seem like the image is the object
       
    pygame.display.update()
 
#modifies the pirates mosition pbased off of user input, modifiying its x and y positions
def pirate_Movement(KeysPressed, PIRATE):
    if KeysPressed[pygame.K_a] and PIRATE.x - PIRATE_CANNON_SPEED > 0: #Does not move if the adddition of speed would put it off screen
        PIRATE.x -= PIRATE_CANNON_SPEED
    if KeysPressed[pygame.K_d] and PIRATE.x + PIRATE_CANNON_SPEED + PIRATE.width < WIDTH:
        PIRATE.x += PIRATE_CANNON_SPEED
    if KeysPressed[pygame.K_w] and PIRATE.y - PIRATE_CANNON_SPEED > 0:
        PIRATE.y -= PIRATE_CANNON_SPEED
    if KeysPressed[pygame.K_s] and PIRATE.y + PIRATE_CANNON_SPEED + PIRATE.height < HEIGHT / 2:
        PIRATE.y += PIRATE_CANNON_SPEED
 
#Makes the bird (Horse monster) move
def horse_Movement(KeysPressed, HORSE):
    if KeysPressed[pygame.K_LEFT] and HORSE.x - HORSE_PINGU_SPEED > 0:
        HORSE.x -= HORSE_PINGU_SPEED
    if KeysPressed[pygame.K_RIGHT] and HORSE.x + HORSE_PINGU_SPEED + HORSE.width < WIDTH:
        HORSE.x += HORSE_PINGU_SPEED
    if KeysPressed[pygame.K_UP] and HORSE.y - HORSE_PINGU_SPEED > HEIGHT / 2:
        HORSE.y -= HORSE_PINGU_SPEED
    if KeysPressed[pygame.K_DOWN] and HORSE.y + HORSE_PINGU_SPEED + HORSE.height < HEIGHT:
        HORSE.y += HORSE_PINGU_SPEED
 
 
def handle_BULLETS(HORSE_bullets, PIRATE_bullets, HORSE, PIRATE): #A funciton which deals with bullets
    for bullet in HORSE_bullets:#goes through the list of bullets. changed thier y position
        bullet.y -= HORSE_PINGU_SPEED
        if PIRATE.colliderect(bullet): #An event occurs if rectangles collide, leads to them being deleted
            pygame.event.post(pygame.event.Event(PIRATE_HIT))
            HORSE_bullets.remove(bullet)
        elif bullet.y <= 0: #removes bullets if they go off screen
            HORSE_bullets.remove(bullet)
    for bullet in PIRATE_bullets:
        bullet.y += PIRATE_CANNON_SPEED
        if HORSE.colliderect(bullet):
            pygame.event.post(pygame.event.Event(HORSE_HIT))
            PIRATE_bullets.remove(bullet)#removes bullets if they go off screen
        elif bullet.y >= HEIGHT:
            PIRATE_bullets.remove(bullet)#removes bullets if they go off screen
 
#Text displayed to player if somone wins
def Victory(text):
    DrawText = VICTORY_FONT.render(text, 1, FONT_COLOR)
    GAME_SCREEN.blit(DrawText, (WIDTH/2 - DrawText.get_width()/2, HEIGHT/2 - DrawText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000) #A delay before the game ends
 
 
def main():
    #This is where the characters are placed on the screen
    HORSE = pygame.Rect(WIDTH / 2 - 50, HEIGHT * 0.75 - 50, PLAYER_WIDTH, PLAYER_LENGTH)
    PIRATE = pygame.Rect(WIDTH / 2 - 50, HEIGHT / 4 - 50, PLAYER_WIDTH, PLAYER_LENGTH)
 
    #A list counting character attacks
    HORSE_bullets = []
    PIRATE_bullets = []
   
    #Character _HEALTH
    HORSE_HEALTH = 20
    PIRATE_HEALTH = 20
 
    Clock = pygame.time.Clock()
    Run = True
    #This while loop runs the game until the quit function is true, which is when the game is over
    while Run:
        #The fps of the game is controlled by the clock
        Clock.tick(FPS)
        #This checks if the game should be over and ends the while loop running the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
 
            #This checks when a character pressed the attack button and creates an attack accordingly
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(HORSE_bullets) < MAX_PROJECTILES:
                    bullet = pygame.Rect(HORSE.x + HORSE.width / 2, HORSE.y, 8, 30)
                    HORSE_bullets.append(bullet)
                    #This plays a chidori sound for every attack
                    HORSE_NOISE.play()
                if event.key == pygame.K_SPACE and len(PIRATE_bullets) < MAX_PROJECTILES:
                    bullet = pygame.draw.circle(GAME_SCREEN, BLUE, (PIRATE.x + PIRATE.width / 2, PIRATE.y + 63), 11)
                    #This plays a chidori sound for every attack
                    PIRATE_bullets.append(bullet)
                    PIRATE_NOISE.play()
           
            #If a character is hit they lose health and a damage sound is played  
            if event.type == HORSE_HIT:
                HORSE_HEALTH -= 1
                DAMAGE_NOISE.play()
            if event.type == PIRATE_HIT:
                PIRATE_HEALTH -= 1
                DAMAGE_NOISE.play()
 
        #The previously defined and explained functions are called here
        handle_BULLETS(HORSE_bullets, PIRATE_bullets, HORSE, PIRATE)
        KeysPressed = pygame.key.get_pressed()
        pirate_Movement(KeysPressed, PIRATE)
        horse_Movement(KeysPressed, HORSE)
        gameWindow(HORSE, PIRATE, PIRATE_bullets, HORSE_bullets, HORSE_HEALTH, PIRATE_HEALTH)
       
        #If a character loses all their health the other character wins and a Victory text is displayed accordingly
        end_message = ""
        if HORSE_HEALTH <= 0:
            end_message = "PIRATES RULE THE WORLD!"
        if PIRATE_HEALTH <= 0:
            end_message = "THE HORSES HAVE TAKEN OVER!"
        if end_message != "":
            Victory(end_message)
            break
   
    #When the while loop ends, the game is quit and the window closes
    pygame.quit()
 
 
if __name__ == "__main__": #a Failsafe incase this file is called from elsewherr
    main()
 
