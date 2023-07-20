import pygame
import random
import os.path
from dataclasses import dataclass
colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]
figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]
gmx=25
gmy=12
resolutionx=1920
resolutiony=1080
@dataclass
class PlayerData:
    playername:str="dummy"
    playerscore:int=0
    def __lt__(self,other):
        if self.playerscore!=other.playerscore:
            return self.playerscore>other.playerscore
        else: return self.playername>other.playername
def chartoint(x):
    return {
        '0':0,
        '1':1,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9
    }[x]
class Figure:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(figures[self.type])


class Tetris:
    level = 1
    score = 0
    state = "startscreen"
    field = []
    height = 0
    width = 0
    x = resolutionx/2.3
    y = resolutiony/5
    xx = resolutionx/2*1.125
    yy = resolutiony/5*1.1
    zoom = 20
    figure = None
    next_figure =None
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.level = 1
        self.state = "startscreen"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(4,0)
    def new_next_figure(self):
        self.next_figure=Figure(4,0)
    def swap_figure(self):
        aux=self.figure
        #print(True)
        self.figure=self.next_figure
        self.next_figure=aux
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2 *1200

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.swap_figure()
        self.new_next_figure()
        if self.intersects():
            self.state = "recordscore"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation
pygame.init()

# culori
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0,0,255)
BRONZE=(205,127,50)
SILVER= (192,192,192)
GOLD =(255,215,0)
RED=(255,0,0)
size = (resolutionx, resolutiony)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
#print(clock)
fps = 15


difficulty = [13,11,7,5,3,2]
pressing_down = False
game = Tetris(gmx, gmy)
counter = 0
file_exists=os.path.exists("scoreboard.txt")
if (file_exists==False):
    scoreboard=open("scoreboard.txt","w")
    scoreboard.close()
print (file_exists)
with open("scoreboard.txt","r+") as file:
    scoreboard=iter(file.read().split())
#scoreboard.txt=open("scoreboard.txt","r+")
#scoreboard=iter(scoreboard.txt.split())
counter=0
quitgame=0
scoreboard_data=[PlayerData() for i in range(12)]
playername=""
input_rect=pygame.Rect(resolutionx/3*1.4,resolutiony/2,200,50)
#fonts
titlefont=pygame.font.SysFont('goudy stout',45,True,False)
authorfont=pygame.font.SysFont('goudy stout',20,True,False)
#print (pygame.font.get_fonts())
fontbegin=pygame.font.SysFont('Calibri',65,True,False)
startfont=pygame.font.SysFont('Calibri',45,True,False)
scoreboardfont = pygame.font.SysFont('Calibri',20,True, False)
BIGscoreboardfont=pygame.font.SysFont('Calibri',30,True,False)
font = pygame.font.SysFont('Calibri', 25, True, False)
font1 = pygame.font.SysFont('Calibri', 65, True, False)
pausefont=pygame.font.SysFont('Calibri',45,True,False)
while True:
    try:
        scoreboard_data[counter].playername = next(scoreboard)
        number=next(scoreboard)
        #p:int=1
        scoreboard_data[counter].playerscore=0
        for char in number:
            if (char>='0' and char<='9'):
                scoreboard_data[counter].playerscore=scoreboard_data[counter].playerscore*10+(chartoint(char))
                #p=p*10
        #scoreboarddata[counter].playerscore:int = next(scoreboard)
        #print(scoreboarddata[counter].playername,scoreboarddata[counter].playerscore)
        #print(scoreboarddata[1].playername,scoreboarddata[1].playerscore,counter)
        counter = counter + 1
    except StopIteration:
        break
if (game.state=="startscreen"):
    while not done:
        #print(game.state)
        screen.fill(BLACK)
        if game.figure is None:
            game.new_figure()
            #game.swap_figure()
            game.new_next_figure()
        #print(counter)
        #print (game.figure.type,game.figure.color,game.next_figure.type,game.next_figure.color)
        counter += 1
        if counter > 100000:
            counter = 0
        if counter % (difficulty[game.level]) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN and (game.state=="startscreen" or game.state=="break")):
                    game.state="start"
                elif (event.key == pygame.K_RETURN and game.state=="start"):
                    game.state="break"
                elif (event.key == pygame.K_ESCAPE and (game.state=="break" or game.state=="startscreen")):
                    quitgame=1
                elif (event.key == pygame.K_r and game.state!="recordscore"):
                    game.figure=None
                    game.next_figure=None
                    game.__init__(gmx,gmy)
                    game.state="start"
                #if event.key == pygame.K_h and game.state == "start":
                #    game.swap_figure()
                #    print (game.intersects())
                #    if game.intersects() is True:
                #        game.swap_figure()
                #        print(True)
                if event.key == pygame.K_UP and game.state == "start":
                    game.rotate()
                if event.key == pygame.K_DOWN and game.state=="start":
                    pressing_down = True
                if event.key == pygame.K_LEFT and game.state=="start":
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT and game.state=="start":
                    game.go_side(1)
                if event.key == pygame.K_SPACE and game.state=="start":
                    game.go_space()
                if game.state=="recordscore":
                    if (event.type == pygame.KEYDOWN):
                        if event.key == pygame.K_BACKSPACE:
                            playername = playername[:-1]
                        else:
                            playername += event.unicode
                    if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
                        if playername == "":
                            playername = "dummy"
                        newcontender = PlayerData(playername, game.score)
                        game.state="gameover"
                        playername=""

                if game.state == "gameover" and (event.key == pygame.K_SPACE or event.key==pygame.K_RETURN):
                    # aici trebuie salvate scorurile
                    it=0
                    scoreboard_data[10]=newcontender
                    scoreboard_data.sort()
                    scoreboard=open("scoreboard.txt","r+")
                    scoreboard.truncate(0)
                    scoreboard=open("scoreboard.txt","w")
                    for it in range(10):
                        scoreboard.write(str(scoreboard_data[it].playername)+" "+str(scoreboard_data[it].playerscore)+" ")
                    scoreboard.close()
                    game.__init__(gmx, gmy)
                if event.key == pygame.K_ESCAPE:
                    quitgame=1
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN and game.state=="start":
                    pressing_down = False
        if (game.state=="startscreen"):
            starttext=startfont.render("Press ENTER to start the game",True, GOLD)
            screen.blit(starttext,[resolutionx/3*1.07,resolutiony/12])
        if (game.state=="break"):
            pausetext=pausefont.render("The game is paused",True,GOLD)
            screen.blit(pausetext,[resolutionx/3*1.2,resolutiony/13])
        pygame.draw.rect(screen, GRAY, [resolutionx/2.3, resolutiony/5, game.zoom * game.width, game.height * game.zoom], 1)
        for i in range(game.height):
            for j in range(game.width):

                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
        pygame.draw.rect(screen,GRAY,[resolutionx/2*1.15,resolutiony/5,game.zoom*7,game.zoom*7],1)
        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                    [game.x + game.zoom * (j + game.figure.x) + 1,
                                    game.y + game.zoom * (i + game.figure.y) + 1,
                                    game.zoom - 2, game.zoom - 2])
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.next_figure.image():
                        pygame.draw.rect(screen, colors[game.next_figure.color],
                                     [game.xx + game.zoom * (j + game.next_figure.x) + 1,
                                      game.yy + game.zoom * (i + game.next_figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])
        title=titlefont.render("TETRISMANIA",True,WHITE)
        author=authorfont.render("DE RAZVAN DIACONESCU",True,WHITE)
        screen.blit(author,[resolutionx*0.14,resolutiony*.30])
        screen.blit(title,[resolutionx*.05,resolutiony*.25])
        controls1=font.render ("CONTROLS", True ,(255,125,0))
        screen.blit(controls1,[resolutionx*.75,resolutiony*0.20])
        controls1=font.render("\u2191 = rotate the figure anticlockwise",True,(255,125,0))
        screen.blit(controls1,[resolutionx*.70,resolutiony*0.23])
        controls1=font.render("\u2190 = move the figure one space to the left",True,(255,125,0))
        screen.blit(controls1,[resolutionx*.70,resolutiony*0.26])
        controls1=font.render("\u2192 = move the figure one space to the right",True,(255,125,0))
        screen.blit(controls1,[resolutionx*.70,resolutiony*0.29])
        controls1=font.render(	"\u2193 = soft drop the current figure",True,(255,125,0))
        screen.blit(controls1,[resolutionx*.70,resolutiony*.32])
        controls1=font.render("SPACE = hard drop the current figure",True,(255,125,0))
        screen.blit(controls1,[resolutionx*.70,resolutiony*.35])
        controls1=font.render("ENTER = pause the game",True,(255,125,0))
        screen.blit(controls1,[resolutionx*.70,resolutiony*.38])
        controls1=font.render("ESC = quit the game to desktop",True,(255,125,0))
        screen.blit(controls1,[resolutionx*.70,resolutiony*.41])
        controls1=font.render("R = restart the game",True,(255,125,0))
        screen.blit(controls1,[resolutionx*.70,resolutiony*.44])
        text = font.render("Score: " + str(game.score), True, WHITE)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        #text_game_over1 = font.render("Press SPACE to start again", True, (255, 215, 0))
        #text_game_over2 = font.render("Press ESCAPE to quit", True, (255,215,0))
        text2 = font.render("Level: " + str(game.level), True, WHITE)
        screen.blit(text, [resolutionx/2.75, resolutiony/7])
        screen.blit(text2,[resolutionx/2.75,resolutiony/7*1.2])
        textfig=font.render("Next piece",True, WHITE)
        screen.blit(textfig,[resolutionx/2*1.15,resolutiony/7*1.2])
        thisisascoreboard=BIGscoreboardfont.render("Scoreboard", True, RED)
        screen.blit(thisisascoreboard,[resolutionx/2*1.14,resolutiony/3*1.03])
        #pygame.draw.rect(screen,(0,0,255),[resolutionx/2*1.15,resolutiony/3*1.1,game.zoom*7,game.zoom*16],2)
        scoreboarditerator=0
        for scoreboarditerator in range(10):
            scoreboardplayer=scoreboardfont.render(str(scoreboarditerator+1)+". "+str(scoreboard_data[scoreboarditerator].playername)+" : "+str(scoreboard_data[scoreboarditerator].playerscore),True,RED)
            screen.blit(scoreboardplayer,[resolutionx/2*1.15,resolutiony/3*1.07+(scoreboarditerator+1)*25])
            scoreboarditerator=scoreboarditerator+1
        if game.state == "gameover":
            screen.blit(text_game_over, [resolutionx/2.3, resolutiony/4])
            #screen.blit(text_game_over1, [resolutionx/2.3, resolutiony/4*1.25])
            #screen.blit(text_game_over2,[resolutionx/2.3,resolutiony/4*1.35])
            game.level=1
        if (game.state=="recordscore"):
            #pygame.draw.rect(screen,GRAY,input_rect)
            newrecord=fontbegin.render("What is your name?",True, GOLD)
            screen.blit(newrecord,[resolutionx/3*1.2,resolutiony/3*0.8])
            write = startfont.render(playername, True, GOLD)
            pygame.draw.rect(screen,BLACK,[resolutionx/3*1.2,resolutiony/3,500,60])
            pygame.draw.rect(screen,GOLD,[resolutionx/3*1.2,resolutiony/3,500,60],1)
            screen.blit(write,[resolutionx/3*1.2,resolutiony/3])
        #schimbare dificultate
        if game.score>20000:
            game.level=2
        if game.score>50000:
            game.level=3
        if game.score>900000:
            game.level=4
        if game.score>150000:
            game.level=5
        if game.score>200000:
            game.level=6
        pygame.display.flip()
        clock.tick(fps)
        if (quitgame):
            pygame.quit()
            break

pygame.quit()