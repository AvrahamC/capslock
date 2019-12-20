"""
Snake Eater
Made with PyGame
"""
from threading import Timer,Thread,Event
import socket
import pygame, sys, time, random
import pylab as pylab
# Create a TCP/IP socket
frame_size_x = 0
frame_size_y = 0
is_he_king = 0
block_list = 0
my_id = 0
banna_list = 0
servers_addres =("192.160.80.8", 45870)
class perpetualTimer():

   def init(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ( "192.168.42.15", 45870)
def ok(data):
    my_id = data.split(",")[1]


def start(data):

    for i in range(1, data.count("#") - 4):  # posiible bad math
         snake_body_everyone[i - 1] = data.split("#")[i]
    frame_size_x = data.split("#")[data.count("#") - 2]
    frame_size_y = data.split("#")[data.count("#") - 1]
    block_list = data.split("#")[data.count("#") - 3]


def update(data):
    for i in range(1, data.count("#") - 3):  # posiible bad math
        '''get info id and if he ate'''
        snake_pos_everyone[data.split("#")][i].split(",")[0].insert(0,data.split("#")[i].split(",")[2])
        if (data.split("#")[i].split(",")[1] == 0 ): snake_pos_everyone[data.split("#")][i].split(",")[0].pop()

    is_he_king = data.split("#")[data.count("#") - 1]
    banana_list = data.split("#")[data.count("#") - 2]


def parse(data):
    if data.split('#')[0] == "update": update(data)
    if data.split('#')[0] == "start": start(data)
    if data.split("#")[0] == "ok": ok()
    #if data.split("#")[0] == "nop":
    #if data.split("#")[0] == "join": join()


def bind_socket():
        data, address = sock.recvfrom(1024)
        parse(data )

bind_socket()#for get OK
bind_socket()#for get START GAME

is_he_growup = 0
is_in_the_game = 1



# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 30

# Window size


# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

bind_socket()bind_socket()
# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color((255,255,0))


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos_everyone = {}
snake_pos_my = snake_pos_everyone[my_id]
snake_body_everyone = {}
snake_body_my = snake_body_everyone [my_id]
block_list = []



direction = 'RIGHT'
change_to = direction

score = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED ', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(1)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


# Main logic
while True:
    is_he_growup = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos_my[1] -= 10
    if direction == 'DOWN':
        snake_pos_my[1] += 10
    if direction == 'LEFT':
        snake_pos_my[0] -= 10
    if direction == 'RIGHT':
        snake_pos_my[0] += 10

    # Snake body growing mechanism
    snake_body_my.insert(0, list(snake_pos_my))
    if snake_pos_my in banna_list:
        score += 1
        is_he_growup = 1
    else:
        snake_body_my.pop()

    if snake_pos_my in block_list:
        is_in_the_game = 0

        sock.sendto(servers_addres,my_id+"#")
        game_over()
    # Spawning food on the screen
    sock.sendto(servers_addres ,my_id,+""+snake_pos_my[0],+""+snake_pos_my[1],+"*"+is_he_growup+"#")
    bind_socket()  # for update

    # GFX
    game_window.fill(white)
    for i in range(0, 4):
       if (i == my_id):
           snake_body_my = snake_body_everyone[my_id]
           for pos in snake_body_my:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
               pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 10, 10))
       else:
           snake_body = snake_body_everyone [i]
           for pos in snake_body_my:
               # Snake body
               # .draw.rect(play_surface, color, xy-coordinate)
               # xy-coordinate -> .Rect(x, y, size_x, size_y)
               pygame.draw.rect(game_window, red, pygame.Rect(pos[0], pos[1], 10, 10))
    # Snke food


    #### pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    for i in banna_list :
        pygame.draw.rect(game_window, yellow, pygame.Rect(banna_list[i][0], banna_list[i][1], 10, 10))
    pygame.draw.rect(game_window, yellow, pygame.Rect(is_he_king[0], is_he_king[1], 10, 10))
    temp = 0
    while temp < 18:
        pygame.draw.rect(game_window, black, pygame.Rect(block_list[temp][0], block_list[temp][1], 10, 10))
        temp += 1

    # Game Over conditions
    # Getting out of bounds
    if snake_pos_my[0] < 0 or snake_pos_my[0] > frame_size_x-10:
        is_in_the_game = 0
        game_over()
    if snake_pos_my[1] < 0 or snake_pos_my[1] > frame_size_y-10:
        is_in_the_game = 0
        game_over()
    # Touching the snake body
    #for block in snake_body[1:]:
     #   if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
      #      game_over()

    show_score(1, white, 'consolas',20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(difficulty)