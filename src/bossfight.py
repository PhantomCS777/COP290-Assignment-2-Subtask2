import pygame,sys
from pygame import mixer
from combatant import Combatant 

mixer.init()


#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 0.5
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 0.5
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load music and sounds
# pygame.mixer.music.load("assets/audio/music.mp3")
# pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(-1, 0.0, 5000)
# sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
# sword_fx.set_volume(0.5)
# magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
# magic_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("../graphics/background.png").convert_alpha()

#load spritesheets
warrior_sheet = pygame.image.load("../graphics/player.png").convert_alpha()
wizard_sheet = pygame.image.load("../graphics/garbage.png").convert_alpha()

#load vicory image
victory_img = pygame.image.load("../graphics/loot.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

count_font = pygame.font.Font(None, 80)
score_font = pygame.font.Font(None, 30)



#create two instances of fighters



class BossFight:
    def __init__(self):
        self.fighter_1 = Combatant(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
        self.fighter_2 = Combatant(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)
        self.last_count_update = pygame.time.get_ticks()
        self.intro_count = 3 
        self.round_over = False
        self.round_over_time = 0
        pass
    def draw_text(self,text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    #function for drawing background
    def draw_bg(self):
        scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    #function for drawing fighter health bars
    def draw_health_bar(self,health, x, y):
        ratio = health / 100
        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

    def run(self):
        running = True
        while running:

            clock.tick(FPS)

            #draw background
            self.draw_bg()

            #show player stats
            self.draw_health_bar(self.fighter_1.health, 20, 20)
            self.draw_health_bar(self.fighter_2.health, 580, 20)
            self.draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
            self.draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

            #update countdown
            if self.intro_count <= 0:
                #move fighters
                self.fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, self.fighter_2, self.round_over)
                self.fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, self.fighter_1, self.round_over)
            else:
                #display count timer
                self.draw_text(str(self.intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                #update count timer
                if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                    self.intro_count -= 1
                    self.last_count_update = pygame.time.get_ticks()

            #update fighters
            self.fighter_1.update()
            self.fighter_2.update()

            #draw fighters
            self.fighter_1.draw(screen)
            self.fighter_2.draw(screen)

            #check for player defeat
            if self.round_over == False:
                if self.fighter_1.alive == False:
                    score[1] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                elif self.fighter_2.alive == False:
                    score[0] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                #display victory image
                screen.blit(victory_img, (360, 150))
                if pygame.time.get_ticks() - self.round_over_time > ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    self.intro_count = 3
                    self.fighter_1 = Combatant(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
                    self.fighter_2 = Combatant(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()


            #update display
            pygame.display.update()

            
