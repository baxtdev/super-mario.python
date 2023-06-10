import pygame
# image_path = 'data/data/org.test.xshxt/files/app/'
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 319))#, flags=pygame.NOFRAME
pygame.display.set_caption("My first Game")
icon=pygame.image.load('img/tetris.png').convert_alpha()
pygame.display.set_icon(icon)

#player
bg=pygame.image.load('img/bg_game.png').convert_alpha()
walk_left = [
    pygame.image.load('img/animation/left1.png').convert_alpha(),
    pygame.image.load('img/animation/left2.png').convert_alpha(),
    pygame.image.load('img/animation/left3.png').convert_alpha(),
    pygame.image.load('img/animation/left4.png').convert_alpha(),
    
]
walk_right = [
    pygame.image.load('img/animation/right1.png').convert_alpha(),
    pygame.image.load('img/animation/right2.png').convert_alpha(),
    pygame.image.load('img/animation/right3.png').convert_alpha(),
    pygame.image.load('img/animation/right4.png').convert_alpha(),
    ]



ghost=pygame.image.load('img/vrag1.png')
# ghost_x= 620
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed= 5
player_x = 150
player_y=250

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('music/sound_gm.mp3')

if bg_sound:
    bg_sound.play()

ghost_timer = pygame.USEREVENT+1

pygame.time.set_timer(ghost_timer,2500)

label = pygame.font.Font('fonts/RubikIso-Regular.ttf', 40)
lose_label= label.render('Вы проиграли!',False,(193,196,199))
restart_label= label.render('restart*',False,(115,132,148))
restart_label_rect = restart_label.get_rect(topleft=(180,200))

bullet_left = 5
bullet = pygame.image.load('img/bullet.png').convert_alpha()
bullets = []



gameplay =True

running = True
while running:
    screen.blit(bullet, (bg_x,0)) 
    screen.blit(bg,(bg_x,0))
    screen.blit(bg,(bg_x+618,0))
    # screen.blit(ghost,(ghost_x,250))

    if gameplay:
        
        

        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))

        if ghost_list_in_game:
            for (i,el) in enumerate(ghost_list_in_game):
                screen.blit(ghost,el)
                el.x-=10

                if el.x<-10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    # running=False
                    gameplay=False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count],(player_x,player_y))
        else:
            screen.blit(walk_right[player_anim_count],(player_x,player_y))

        
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x-=player_speed
        elif keys[pygame.K_RIGHT] and player_x<200:
            player_x+=player_speed
        
        if not is_jump:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                is_jump = True
        
        else:
            if jump_count>=-8:
                if jump_count>0:
                    player_y -= (jump_count**2)/2
                else:
                    player_y+=(jump_count**2)/2    
                jump_count-=1
            else:
                is_jump = False
                jump_count = 8           
        
        
        if player_anim_count == 3:
            player_anim_count=0
        else:
            player_anim_count+=1  
        
        bg_x-=3 
        if bg_x == -618:
            bg_x=0      
        
        # if keys[pygame.K_0]:
        #     bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            
            



        if bullets:
            for (i,el) in enumerate (bullets):
                screen.blit(bullet, (el.x, el.y))
                
                el.x += 4
                print(bullet)

                if el.x > 630:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)    

                # print('strlyal')    


    else:
        screen.fill((87,88,89))
        screen.blit(lose_label,(100,100))
        screen.blit(restart_label,restart_label_rect)
        
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullet_left = 5


    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_0 and bullet_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullet_left -=1
    clock.tick(15)
