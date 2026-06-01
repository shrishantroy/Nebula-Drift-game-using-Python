import pygame as pg
from sys import exit
from random import randint, choice

def rotate(speedx, speedy):
    if speedx == 0 and speedy < 0:
        direction = 180
    if speedx < 0 and speedy == 0:
        direction = 90
    if speedx == 0 and speedy > 0:
        direction = 0
    if speedx > 0 and speedy == 0:
        direction = -90
    if speedx > 0 and speedy > 0:
        direction = -45
    if speedx < 0 and speedy < 0:
        direction = 135
    if speedx > 0 and speedy < 0:
        direction = -135
    if speedx < 0 and speedy > 0:
        direction = 45
    if speedx == 0 and speedy == 0:
        direction = 0
    return direction
def shoot(bullet_list):
    global bullet_speed, bullet_speedx

    for bullet in bullet_list:
        if bullet['direction'] == 0:
            bullet['rect'].top -= bullet_speed
        elif bullet['direction'] == 180:
            bullet['rect'].top += bullet_speed
        elif bullet['direction'] == 90:
            bullet['rect'].left -= (bullet_speedx+5)
        elif bullet['direction'] == -90:
            bullet['rect'].left += (bullet_speedx+5)
        elif bullet['direction'] == 45:
            bullet['rect'].left -= bullet_speedx
            bullet['rect'].top -= bullet_speed
        elif bullet['direction'] == -45:
            bullet['rect'].left += bullet_speedx
            bullet['rect'].top -= bullet_speed
        elif bullet['direction'] == 135:
            bullet['rect'].left -= bullet_speedx
            bullet['rect'].top += bullet_speed
        elif bullet['direction'] == -135:
            bullet['rect'].left += bullet_speedx
            bullet['rect'].top += bullet_speed
    bullet_list = [bul for bul in bullet_list if bul['rect'].top <= 600 and bul['rect'].bottom >=
                   0 and bul['rect'].right >= 0 and bul['rect'].left <= 1200 and bul['Hit'] == False]
    return bullet_list
pg.init()

screen = pg.display.set_mode((1200, 600))
space_surf = pg.image.load('backgrounds/space.jpg').convert_alpha()
space_surf1 = pg.transform.scale(space_surf, (1200, 600))
space_surf2 = space_surf1
space_rect1 = space_surf1.get_rect(center=(600, 300))
space_rect2 = space_surf2.get_rect(bottom=space_rect1.top)

intro_surf = pg.image.load('backgrounds/intro.jpg')
intro_surf = pg.transform.scale(intro_surf,(1200,600))
intro_surf_rect = intro_surf.get_rect(center = (600,300))

player_surf = pg.image.load('player/player.png').convert_alpha()
player_surf = pg.transform.scale(player_surf, (72, 84))
player_original = player_surf
player_rect = player_surf.get_rect(center=space_rect1.center)

bullet_surf = pg.image.load('obstacles/turpedo.png').convert_alpha()
bullet_surf = pg.transform.scale(bullet_surf, (16, 40))
bullet_rect = bullet_surf.get_rect(center=player_rect.center)
bullet_original_surf = bullet_surf

ufo1_surf = pg.image.load("enemies/ufo1.png")
ufo1_surf = pg.transform.scale(ufo1_surf, (90, 84))
ufo2_surf = pg.image.load("enemies/ufo2.png")
ufo2_surf = pg.transform.scale(ufo2_surf, (90, 84))

damage1_surf = pg.image.load("damage/damage1.png")
damage1_surf = pg.transform.scale(damage1_surf, (90, 84))
damage2_surf = pg.image.load("damage/damage2.png")
damage2_surf = pg.transform.scale(damage2_surf, (90, 84))
damage3_surf = pg.image.load("damage/damage3.png")
damage3_surf = pg.transform.scale(damage3_surf, (90, 84))

planet1_surf = pg.image.load('obstacles/planet1.png')
planet1_surf = pg.transform.scale(planet1_surf, (100, 100))
planet2_surf = pg.image.load('obstacles/planet2.png')
planet2_surf = pg.transform.scale(planet2_surf, (85, 85))
planet3_surf = pg.image.load('obstacles/planet3.png')
planet3_surf = pg.transform.scale(planet3_surf, (85, 85))

score_font = pg.font.Font('Font/Asteroid Blaster.ttf', 32)
score_top = space_rect1.top + 10
score_right = space_rect1.right - 10

intro_font = pg.font.Font('Font/Endgame.otf',108)
intro_text_surf = intro_font.render("Nebula Drift",False,(0,255,230))
intro_text_rect = intro_text_surf.get_rect(center = (600,100))

sub_font = pg.font.Font('Font/ShootVector.otf',50)
sub_text = ["Welcome aboard Captain!",
            "The ship has been intercepted by unknown aliens",
            "You must neutralize them",
            "Use arrows to move and Z to shoot",
            "Press Space to take control"]

sub_text_surf1 = sub_font.render(sub_text[0],False,(0,255,230))
sub_text_rect1 = sub_text_surf1.get_rect(center = (600,300))
sub_text_surf2 = sub_font.render(sub_text[1],False,(0,255,230))
sub_text_rect2 = sub_text_surf2.get_rect(center = (600,352))
sub_text_surf3 = sub_font.render(sub_text[2],False,(0,255,230))
sub_text_rect3 = sub_text_surf3.get_rect(center = (600,404))
sub_text_surf4 = sub_font.render(sub_text[3],False,(0,255,230))
sub_text_rect4 = sub_text_surf4.get_rect(center = (600,456))
sub_text_surf5 = sub_font.render(sub_text[4],False,(0,255,230))
sub_text_rect5 = sub_text_surf5.get_rect(center = (600,508))

GameOver_surf = pg.image.load('damage/GameOver.jfif')
GameOver_surf = pg.transform.scale(GameOver_surf,(1200,600))
GameOver_rect = GameOver_surf.get_rect(center = (600,300))

GameOverFont = pg.font.Font('Font/Horror.ttf',150)
GameOverText = GameOverFont.render("Game Over",False,(0,255,230))
GameOverText_rect = GameOverText.get_rect(center = (600,100))

health_surf = pg.image.load('player/life.png')
health_surf = pg.transform.scale(health_surf,(36,42))

final_score_font = pg.font.Font('Font/ShootVector.otf',100)

fps = 60
clock = pg.time.Clock()

obstacle_timer = pg.USEREVENT + 1
spawn_time = 800

enemy_timer = pg.USEREVENT + 2
enemy_move_timer = pg.USEREVENT + 3

pg.time.set_timer(enemy_move_timer, 600)

damage_timer = pg.USEREVENT + 4
pg.time.set_timer(damage_timer, 1000)

health_timer = pg.USEREVENT + 5

intro_sound = pg.mixer.Sound('Sound/destroyed.wav')
game_sound = pg.mixer.Sound('Sound/Orbital Colossus.mp3')
game_over_sound = pg.mixer.Sound('Sound/Laugh.mp3')
shoot_sound = pg.mixer.Sound('Sound/tir.mp3')
enemy_death_sound = pg.mixer.Sound('Sound/rumble.wav')
sound_list = [{
    'sound' : intro_sound,
    'started' : False
},{
    'sound' : game_sound,
    'started' : False
},{
    'sound': game_over_sound,
    'started': False
}]

game_state = 0
while True:
    if game_state == 0:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    sound_list[0]['sound'].stop()
                    sound_list[2]['started'] = False
                    game_state = 1
        
        if sound_list[0]['started'] == False:
            sound_list[0]['sound'].play(-1)
            sound_list[0]['started'] = True
            
        
        back_speed = 6
        bspeed = 0
        rocket_speed = 7
        speedx = 0
        direction = 0
        life = 5

        obstacle_list = []

        enemy_list = []
        dx_enemy = 2
        dy_enemy = 2
        enemy_speed_x = 0
        enemy_speed_y = 0
        enemy_spawn = 600

        spawn_up_y = [-515, -43]
        spawn_down_y = [643, 1157]
        spawny = spawn_up_y

        is_going_up = True
        bullet_speed = 9
        bullet_speedx = 10
        bullet_list = []
        score = 0

        health_list = []
        health_spawn = 1500

        screen.blit(intro_surf,intro_surf_rect)
        screen.blit(intro_text_surf,intro_text_rect)
        screen.blit(sub_text_surf1,sub_text_rect1)
        screen.blit(sub_text_surf2,sub_text_rect2)
        screen.blit(sub_text_surf3,sub_text_rect3)
        screen.blit(sub_text_surf4,sub_text_rect4)
        screen.blit(sub_text_surf5,sub_text_rect5)

    if game_state == 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    speedx = rocket_speed
                if event.key == pg.K_LEFT:
                    speedx = -rocket_speed
                if event.key == pg.K_UP:
                    pg.time.set_timer(obstacle_timer, spawn_time)
                    pg.time.set_timer(enemy_timer, enemy_spawn)
                    pg.time.set_timer(health_timer,health_spawn)
                    bspeed = back_speed
                    spawny = spawn_up_y
                    is_going_up = True

                if event.key == pg.K_DOWN:
                    bspeed = -back_speed
                    pg.time.set_timer(obstacle_timer, spawn_time)
                    pg.time.set_timer(enemy_timer, enemy_spawn)
                    pg.time.set_timer(health_timer,health_spawn)
                    spawny = spawn_down_y
                    is_going_up = False

                if event.key == pg.K_z:
                    shoot_sound.play()
                    bullet_direction = direction
                    bullet_surf = pg.transform.rotozoom(bullet_original_surf, bullet_direction, 1)
                    bullet_rect = bullet_surf.get_rect(center=player_rect.center)
                    bullet_list.append({
                        'rect': bullet_rect,
                        'surface': bullet_surf,
                        'direction': bullet_direction,
                        'Hit': False
                    })

            if event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    pg.time.set_timer(obstacle_timer, 0)
                    pg.time.set_timer(enemy_timer, 0)
                    pg.time.set_timer(health_timer,0)
                    bspeed = 0
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    speedx = 0
            if event.type == obstacle_timer:

                planet_type = randint(1, 3)

                if planet_type == 1:
                    obstacle_list.append({
                        'rect': planet1_surf.get_rect(center=(randint(43, 1157), randint(spawny[0], spawny[1]))),
                        'surface': planet1_surf,
                        'state' : 'alive',
                        'collide' : False
                    })
                elif planet_type == 2:
                    obstacle_list.append({
                        'rect': planet2_surf.get_rect(center=((randint(43, 1157), randint(spawny[0], spawny[1])))),
                        'surface': planet2_surf,
                        'state' : 'alive',
                        'collide' : False
                    })
                else:
                    obstacle_list.append({
                        'rect': planet3_surf.get_rect(center=(randint(43, 1157), randint(spawny[0], spawny[1]))),
                        'surface': planet3_surf,
                        'state' : 'alive',
                        'collide' : False
                    })

            if event.type == enemy_timer:
                enemy_type = randint(1, 2)

                if enemy_type == 1:
                    enemy_list.append({
                        'rect': ufo1_surf.get_rect(center=(randint(43, 1157), randint(spawny[0], spawny[1]))),
                        'surface': ufo1_surf,
                        'vx': enemy_speed_x,
                        'vy': enemy_speed_y,
                        'state': 'alive',
                        'collide' : False
                    })
                else:
                    enemy_list.append({
                        'rect': ufo2_surf.get_rect(center=(randint(43, 1157), randint(spawny[0], spawny[1]))),
                        'surface': ufo2_surf,
                        'vx': enemy_speed_x,
                        'vy': enemy_speed_y,
                        'state': 'alive',
                        'collide' : False
                    })
            if event.type == enemy_move_timer:
                enemy_speed_x = choice([dx_enemy, -dx_enemy])
                enemy_speed_y = choice([dy_enemy, -dy_enemy])

            if event.type == damage_timer:
                enemy_list = [enemy for enemy in enemy_list if enemy['state'] == 'alive']
                obstacle_list = [obstacle for obstacle in obstacle_list if obstacle['state'] == 'alive']

            if event.type == health_timer:
                health_list.append({
                    'rect': health_surf.get_rect(center = (randint(43, 1157), randint(spawny[0], spawny[1]))),
                    'surface': health_surf,
                    'collected' : False
                })


        if sound_list[1]['started'] == False:
            sound_list[1]['sound'].play(-1)
            sound_list[1]['started'] = True

        if is_going_up:
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle['rect'].top <= 600]
            enemy_list = [enemy for enemy in enemy_list if enemy['rect'].top <= 600]
            health_list = [health for health in health_list if health['rect'].top<=600 and health['collected'] == False]

        else:
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle['rect'].bottom >= 0]
            enemy_list = [enemy for enemy in enemy_list if enemy['rect'].bottom >= 0]
            health_list = [health for health in health_list if health['rect'].bottom>=0 and health['collected'] == False]

        player_rect.right += speedx
        space_rect1.top += bspeed
        space_rect2.bottom += bspeed

        if player_rect.right >= space_rect1.right or player_rect.right >= space_rect2.right:
            speedx = 0
        if player_rect.left < space_rect1.left or player_rect.left < space_rect2.left:
            speedx = 0

        direction = rotate(speedx, bspeed)
        player_surf = pg.transform.rotozoom(player_original, direction, 1)
        player_rect = player_surf.get_rect(center=player_rect.center)

        if space_rect1.top >= 0:
            space_rect2.bottom = space_rect1.top
        if space_rect2.top >= 0:
            space_rect1.bottom = space_rect2.top
        if space_rect1.bottom <= 600:
            space_rect2.top = space_rect1.bottom
        if space_rect2.bottom <= 600:
            space_rect1.top = space_rect2.bottom

        screen.blit(space_surf2, space_rect2)
        screen.blit(space_surf1, space_rect1)

        for obs_rect_dic in obstacle_list:
            obs_rect_dic['rect'].top += bspeed
            screen.blit(obs_rect_dic['surface'], obs_rect_dic['rect'])

        for enemy_rect_dic in enemy_list:
            enemy_rect_dic['rect'].top += bspeed

            if enemy_rect_dic['rect'].top <= 600 and enemy_rect_dic['rect'].bottom >= 0:

                if enemy_rect_dic['rect'].right >= 1200 or enemy_rect_dic['rect'].left <= 0:
                    enemy_rect_dic['vx'] = -enemy_rect_dic['vx']
                if enemy_rect_dic['rect'].top <= 0 or enemy_rect_dic['rect'].bottom >= 600:
                    enemy_rect_dic['vy'] = -enemy_rect_dic['vy']

                enemy_rect_dic['rect'].right += enemy_rect_dic['vx']
                enemy_rect_dic['rect'].top += enemy_rect_dic['vy']

            screen.blit(enemy_rect_dic['surface'], enemy_rect_dic['rect'])
        
        for health in health_list:
            health['rect'].top += bspeed
            screen.blit(health['surface'],health['rect']) 

        bullet_list = shoot(bullet_list)
        enemy_check = [enemy for enemy in enemy_list if enemy['rect'].bottom >=0 and enemy['rect'].top <= 600 and enemy['state'] == 'alive']

        for bullet_spawn in bullet_list:
            screen.blit(bullet_spawn['surface'], bullet_spawn['rect'])

            for enemy_rect in enemy_check:

                if bullet_spawn['rect'].colliderect(enemy_rect['rect']):
                    enemy_death_sound.play()
                    damage_surf = choice([damage1_surf, damage2_surf, damage3_surf])
                    bullet_spawn['Hit'] = True
                    enemy_rect['state'] = 'dead'
                    enemy_rect['rect'] = damage_surf.get_rect(center=enemy_rect['rect'].center)
                    enemy_rect['surface'] = damage_surf
                    score += 1

        score_val_surf = score_font.render(f"Score: {score}", False, (0, 255, 255))
        score_val_rect = score_val_surf.get_rect(top=score_top, right=score_right)

        enemy_spawn = max(200, 600 - 5*score)
        dx_enemy = min(7, 2 + score//20)
        dy_enemy = min(7, 2 + score//20)

        obstacle_check = [obs for obs in obstacle_list if obs['rect'].top<=600 and obs['rect'].bottom>=0 and obs['state'] == 'alive']

        for obs_check in obstacle_check:
            if player_rect.colliderect(obs_check['rect']):
                if obs_check['collide'] == False:
                    enemy_death_sound.play()
                    life -= 1
                    obs_check['collide'] = True
                    obs_check['state'] = 'dead'
                    damage_surf_planet = choice([damage1_surf, damage2_surf, damage3_surf])
                    obs_check['rect'] = damage_surf_planet.get_rect(center = obs_check['rect'].center)
                    obs_check['surface'] = damage_surf_planet
            else:
                obs_check['collide'] = False
            
        for enemy_rect in enemy_check:
            if player_rect.colliderect(enemy_rect['rect']):
                if enemy_rect['collide'] == False:
                    enemy_death_sound.play()
                    life -= 1
                    enemy_rect['collide'] = True
                    enemy_rect['state'] = 'dead'
                    damage_surf_enemy = choice([damage1_surf, damage2_surf, damage3_surf])
                    enemy_rect['rect'] = damage_surf_enemy.get_rect(center = enemy_rect['rect'].center)
                    enemy_rect['surface'] = damage_surf_enemy
            else:
                enemy_rect['collide'] = False
        
        if life <= 0:
            game_state = 2
            sound_list[1]['sound'].stop()
        
        health_check = [health for health in health_list if health['rect'].top<=600 and health['rect'].bottom>=0 and health['collected'] == False]

        for health in health_list:
            if player_rect.colliderect(health['rect']):
                health['collected'] = True
                life += 1

        life_text = score_font.render(f"Health: {life}",False,(0,255,255))
        life_rect = life_text.get_rect(top = score_val_rect.bottom + 10, right = score_val_rect.right)

        screen.blit(score_val_surf, score_val_rect)
        screen.blit(life_text,life_rect)
        screen.blit(player_surf, player_rect)
    
    if game_state == 2:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    sound_list[0]['started'] = False
                    sound_list[1]['started'] = False
                    sound_list[2]['sound'].stop()
                    game_state = 0
        
        if sound_list[2]['started'] == False:
            sound_list[2]['sound'].play(-1)
            sound_list[2]['started'] = True


        final_score_text = final_score_font.render(f"Score: {score}",False,(0,255,255))
        final_score_rect = final_score_text.get_rect(center = (600,500))
        redirect_text = sub_font.render("Press Space",False,(0,255,255))
        redirect_text_rect = redirect_text.get_rect(center = (600,580))

        screen.blit(GameOver_surf,GameOver_rect)
        screen.blit(GameOverText,GameOverText_rect)
        screen.blit(final_score_text,final_score_rect)
        screen.blit(redirect_text,redirect_text_rect)


    pg.display.update()
    clock.tick(fps)
