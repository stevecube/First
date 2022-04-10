import pygame, random
from time import sleep

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

class Car:
    imagecar = ['RacingCar01.png', 'RacingCar02.png', 'RacingCar03.png', 'RacingCar04.png', 'RacingCar05.png',
                'RacingCar06.png', 'RacingCar07.png', 'RacingCar08.png', 'RacingCar09.png', 'RacingCar10.png',
                'RacingCar11.png', 'RacingCar12.png', 'RacingCar13.png', 'RacingCar14.png', 'RacingCar15.png',
                'RacingCar16.png', 'RacingCar17.png', 'RacingCar18.png', 'RacingCar19.png', 'RacingCar20.png']

    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
    
    def loadimage(self):
        self.image = pygame.image.load(random.choice(self.imagecar))
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]
    
    def drawimage(self):
        screen.blit(self.image, [self.x, self.y])

    def mvoex(self):
        self.x += self.dx
    
    def movey(self):
        self.y += self.dy
    
    def checkoutofscreen(self):
        if self.x + self.width > WINDOW_WIDTH or self.x < 0:
            self.x -= self.dx
    
    def checkcrash(self, car):
        if(self.x + self.width > car.x) and (self.x < car.x + car.width) and(self.y < car.y + car.height) and (self.y + self.height < car.y):
            return True
        else:
            return False

def drawmainmenu():
    drawx = (WINDOW_WIDTH / 2) - 200
    drawy = WINDOW_HEIGHT / 2
    imageintro = pygame.image.load('PyCar.png')
    screen.blit(imageintro, [drawx, drawy - 280])
    font40 = pygame.font.SysFont('FixedSys', 40, True, False)
    font30 = pygame.font.SysFont('FixedSys', 30, True, False)
    texttitle = font40.render('PyCar: Racing Car Game', True, BLACK)
    screen.blit(texttitle, [drawx, drawy])
    textscore = font40.render('Score: ' + str(score), True, WHITE)
    screen.blit(textscore, [drawx, drawy + 70])
    textstart = font30.render('Press Space Key to Start', True, RED)
    screen.blit(textstart, [drawx, drawy + 140])
    pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PyCar: Racing Car Game")
    clock = pygame.time.Clock()
    
    pygame.mixer.music.load('race.wav')
    sound_crash = pygame.mixer.Sound('cash.wav')
    sound_engine = pygame.mixer.Sound('engine.wav')
    
    player = Car(WINDOW_WIDTH / 2), (WINDOW_HEIGHT - 150), 0, 0
    player.loadimage()

    cars = []
    carcount = 3
    for i in range(carcount):
        x = random.randrange(0, WINDOW_WIDTH - 55)
        y = random.randrange(-150, -50)
        car = Car(x, y, 0, random.randint(5, 10))
        car.loadimage()
        cars.append(car)
    
    lanes = []
    lanewidth = 10
    laneheight = 80
    lanemargin = 20
    lanecount = 20
    lanex = (WINDOW_WIDTH - lanewidth) / 2
    laney = -10
    for i in range(lanecount):
        lanes.append([lanex, laney])
        laney += laneheight + lanemargin
    
    score = 0
    crash = True
    gameon = True
    while gameon:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameon = False
            
            if crash:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for i in range(carcount):
                        cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                        cars[i].y = random.randrange(-150, -50)
                        cars[i].loadimage()

                    player.loadimage()
                    player.x = WINDOW_WIDTH / 2
                    player.dx = 0
                    score = 0
                    pygame.mouse.set_visible(False)
                    sound_engine.play()
                    sleep(2)
                    pygame.mixer.music.play(-1)
            
            if not crash:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 4
                    elif event.key == pygame.K_LEFT:
                        player.dx = -4
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 0
                    elif event.key == pygame.K_LEFT:
                        player.dx = 0

        screen.fill(GRAY)

        if not crash:
            for i in range(lanecount):
                pygame.draw.rect(screen, WHITE, [lanes[i][0], lanes[i][1], lanewidth, laneheight])
                lanes[i][1] += 10
                if lanes[i][1] > WINDOW_HEIGHT:
                    lanes[i][1] = -40 - laneheight
            
            player.drawimage()
            player.movex()
            player.checkoutofscreen()
            for i in range(carcount):
                cars[i].drawimage()
                cars[i].y += cars[1].dy
                if cars[i].y > WINDOW_HEIGHT:
                    score += 10
                    cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                    cars[i].y = random.randrange(-150, -50)
                    cars[i].dy = random.randint(5, 10)
                    cars[i].loadimage()
    
            for i in range(carcount):
                if player.checkcrash(cars[i]):
                    crash = True
                    pygame.mixer.music.stop()
                    sound_crash.play()
                    sleep(2)
                    pygame.mouse.set_visible(True)
                    break
            
            drawscore()
            pygame.display.flip()
            
        else:
            drawmainmenu()
        
        clock.tick(60)
    pygame.quit()