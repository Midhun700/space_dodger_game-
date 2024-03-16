import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT=1000,800
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Bullet Dodge")
BG=pygame.transform.scale((pygame.image.load("space.jpg")),(WIDTH,HEIGHT))

PLAYER_WIDTH=40
PLAYER_HEIGHT=60
PLAYER_VEL=5

STAR_WIDTH=10
STAR_HEIGHT=20
STAR_VEL=3

FONT=pygame.font.SysFont("comicsans",30)
hit_sound=pygame.mixer.Sound("hit.wav")
intro_sound=pygame.mixer.Sound("intro.wav")

def draw(player,elapsed_time,stars):

    WIN.blit(BG,(0,0))
    time_text=FONT.render(f"Time:{round(elapsed_time)}s",1,"white")
    WIN.blit(time_text,(10,10))
    pygame.draw.rect(WIN,"red",player)
    for star in stars:
        pygame.draw.rect(WIN,"white",star)

    pygame.display.update()

def main():
    intro_sound.play()
    game_name_text = FONT.render("BULLET DODGE", 4, "yellow")
    WIN.blit(game_name_text, (WIDTH/2 - game_name_text.get_width()/2, HEIGHT/3))
    pygame.display.update()
    pygame.time.delay(3000)
    while True:  # Outer loop for restarting the game
        run=True
        clock=pygame.time.Clock()
        player=pygame.Rect(200,HEIGHT-PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT)
        start_time=time.time()
        elapsed_time=0

        star_add_increment=2000
        star_count=0
        stars=[]

        while run:
            star_count+=clock.tick(60)
            elapsed_time=time.time()-start_time

            if star_count>star_add_increment:
                for _ in range(3):
                    star_x=random.randint(0,WIDTH-STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)
                star_add_increment=max(200,star_add_increment-50)
                star_count=0

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and run == False:
                        main()

            keys=pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x-PLAYER_VEL>=0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and player.x+PLAYER_VEL+PLAYER_WIDTH<=WIDTH:
                player.x += PLAYER_VEL
            for star in stars[:]:
                star.y+=STAR_VEL
                if star.y>HEIGHT:
                    stars.remove(star)
                elif star.y+star.height>=player.y and star.colliderect(player):
                    run=False
                    hit_sound.play()
                    break

            draw(player,elapsed_time,stars)
        
        lost_text=FONT.render("YOU LOST!! Press SPACE to restart",1, "yellow")
        WIN.blit(lost_text,(WIDTH/2-lost_text.get_width()/2,HEIGHT/2-lost_text.get_height()/2))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main()
                if event.type==pygame.QUIT:
                    pygame.quit()
                    return

if __name__=="__main__":
    main()