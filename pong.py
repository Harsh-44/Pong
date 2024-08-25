import pygame, sys, random


#setting up 

pygame.init()
clock = pygame.time.Clock()

#setting up main window

screen_width = 960
screen_height = 560

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

##################################################
# RECTANGLES/SPRITES FOR THE GAME
##################################################

ball = pygame.Rect(screen_width/2-15, screen_height/2-15,30,30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color('black')
light_grey = pygame.Color('white')

ball_speed_x = 7 * random.choice((-1,1))
ball_speed_y = 7 * random.choice((-1,1))

player_speed = 0
opponent_speed = 7

player_score = 0
opponent_score = 0

#################################
# MAKING ELEMENTS
#################################

start_img = pygame.image.load('assets/start.png').convert_alpha()
options_img = pygame.image.load('assets/options.png').convert_alpha()
exit_img = pygame.image.load('assets/exit.png').convert_alpha()

title_font = pygame.font.Font('assets/fonts/PressStart2P-Regular.ttf', 50)

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def ball_animation():
    global ball_speed_x, ball_speed_y

    #ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        update_scores(player_scored=True)
        ball_restart()
    if ball.right >= screen_width:
        update_scores(player_scored=False)
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height  

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height  


def ball_restart():
    global ball_speed_x, ball_speed_y

    ball.center = (screen_width/2, screen_height/2)
    ball_speed_y *= random.choice((1,-1))
    ball_speed_x *= random.choice((1,-1))

def update_scores(player_scored):
    global player_score, opponent_score

    if player_scored:
        player_score += 1
    else:
        opponent_score += 1

#############################
# GAME LOOP
#############################

def main_game():
    global player_speed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7

        ball_animation()
        player_animation()
        opponent_ai()

        # drawing
        screen.fill(bg_color)

        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

        # display scores
        font = pygame.font.Font(None, 74)
        text = font.render(str(player_score), True, light_grey)
        screen.blit(text, (screen_width / 2 + 20, 10))
        text = font.render(str(opponent_score), True, light_grey)
        screen.blit(text, (screen_width / 2 - 60, 10))

        pygame.display.flip()
        clock.tick(60)

############################
# MENU LOOP
############################

def menu_screen():

    button_spacing = 20

    start_button = Button(screen_width / 2 - start_img.get_width() / 2, screen_height / 2 - start_img.get_height() / 1, start_img)
    options_button = Button(screen_width / 2 - options_img.get_width() / 2, start_button.rect.bottom + button_spacing, options_img)
    exit_button = Button(screen_width / 2 - exit_img.get_width() / 2, options_button.rect.bottom + button_spacing, exit_img)

    while True:
        screen.fill(bg_color)

        # Draw title
        title_text = title_font.render("NotPONG", True, light_grey)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2 - 200))


        start_button.draw()
        options_button.draw()
        exit_button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    main_game()
                if options_button.is_clicked(event.pos):
                    print("Options button clicked!")  # Placeholder for options
                if exit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

menu_screen()